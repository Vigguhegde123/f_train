from flask import Flask, request, jsonify
from flask_cors import CORS
import heapq
from twilio.rest import Client

# === CONFIGURATION ===
app = Flask(__name__)
CORS(app)

# Twilio Credentials (REPLACE with environment variables in production)
TWILIO_ACCOUNT_SID = 'your_account_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
TWILIO_PHONE_NUMBER = '+1234567890'

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_sms(to, message):
    try:
        twilio_client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=to
        )
    except Exception as e:
        print(f"[SMS ERROR] {e}")


# === MODELS ===
class Passenger:
    def __init__(self, name, pid, age, priority=0, phone=None):
        self.name = name
        self.id = pid
        self.age = age
        self.priority = priority
        self.phone = phone

    def to_dict(self):
        return {
            "name": self.name,
            "id": self.id,
            "age": self.age,
            "priority": self.priority,
            "phone": self.phone
        }

class TrainReservationSystem:
    def __init__(self, max_seats=3):
        self.max_seats = max_seats
        self.confirmed = []
        self.waiting_list = []
        self.counter = 0

    def reserve(self, passenger):
        if any(p.id == passenger.id for p in self.confirmed) or \
           any(p.id == passenger.id for _, _, p in self.waiting_list):
            return {"status": "duplicate", "message": "Passenger ID already exists."}

        if len(self.confirmed) < self.max_seats:
            self.confirmed.append(passenger)
            return {"status": "confirmed", "passenger": passenger.to_dict()}
        else:
            heapq.heappush(self.waiting_list, (-passenger.priority, self.counter, passenger))
            self.counter += 1
            return {"status": "waiting", "passenger": passenger.to_dict(), "queue_position": len(self.waiting_list)}

    def cancel(self, pid):
        for i, passenger in enumerate(self.confirmed):
            if passenger.id == pid:
                self.confirmed.pop(i)
                moved = None
                if self.waiting_list:
                    _, _, next_passenger = heapq.heappop(self.waiting_list)
                    self.confirmed.append(next_passenger)
                    moved = next_passenger.to_dict()
                return {"status": "cancelled", "moved_from_waiting": moved}
        return {"status": "not_found"}

    def status(self):
        return {
            "confirmed": [p.to_dict() for p in self.confirmed],
            "waiting_list": [p.to_dict() for _, _, p in self.waiting_list]
        }


# === INSTANCE ===
system = TrainReservationSystem()

# === ROUTES ===

@app.route("/")
def home():
    return "🚄 Train Reservation System is Running"

@app.route("/reserve", methods=["POST"])
def reserve():
    data = request.get_json()
    passenger = Passenger(
        name=data.get("name"),
        pid=data.get("id"),
        age=data.get("age"),
        priority=data.get("priority", 0),
        phone=data.get("phone")
    )
    result = system.reserve(passenger)

    # Send SMS Notification
    if passenger.phone:
        msg = f"Hello {passenger.name}, your reservation is {result['status']}."
        if result['status'] == "waiting":
            msg += f" You are number {result['queue_position']} on the waiting list."
        send_sms(passenger.phone, msg)

    return jsonify(result)

@app.route("/cancel", methods=["POST"])
def cancel():
    data = request.get_json()
    pid = data.get("id")
    phone = data.get("phone")  # Optional

    result = system.cancel(pid)

    if phone:
        if result["status"] == "cancelled":
            msg = f"Your reservation (ID: {pid}) has been cancelled."
            if result["moved_from_waiting"]:
                moved = result["moved_from_waiting"]
                msg += f" {moved['name']} (ID: {moved['id']}) has been moved from waiting to confirmed."
            send_sms(phone, msg)
        elif result["status"] == "not_found":
            send_sms(phone, f"No reservation found for ID {pid}.")

    return jsonify(result)

@app.route("/status", methods=["GET"])
def status():
    return jsonify(system.status())

# === MAIN ===
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000, debug=True)
