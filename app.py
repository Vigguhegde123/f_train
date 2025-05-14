from flask import Flask, request, jsonify
import heapq
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- Passenger class ---
class Passenger:
    def __init__(self, name, pid, age, priority=0):
        self.name = name
        self.id = pid
        self.age = age
        self.priority = priority

    def __str__(self):
        return f"{self.name} (ID: {self.id}, Age: {self.age})"

    def to_dict(self):
        return {"name": self.name, "id": self.id, "age": self.age, "priority": self.priority}

# --- Train Reservation System ---
class TrainReservationSystem:
    def __init__(self, max_seats=3):
        self.max_seats = max_seats
        self.confirmed = []
        self.waiting_list = []
        self.counter = 0

    def reserve(self, passenger):
        if len(self.confirmed) < self.max_seats:
            self.confirmed.append(passenger)
            return {"status": "confirmed", "passenger": passenger.to_dict()}
        else:
            heapq.heappush(self.waiting_list, (-passenger.priority, self.counter, passenger))
            self.counter += 1
            return {"status": "waiting", "passenger": passenger.to_dict()}

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

# Instantiate the system
system = TrainReservationSystem()

# --- Route to serve complete HTML with success message ---
@app.route("/")
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Train Reservation System</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f9f9f9;
                padding: 20px;
                max-width: 600px;
                margin: 50px auto;
            }
            .card {
                background: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            input, button {
                padding: 10px;
                margin: 5px 0;
                width: 100%;
                box-sizing: border-box;
            }
            button {
                background-color: #007BFF;
                color: #fff;
                border: none;
                cursor: pointer;
            }
            button:hover {
                background-color: #0056b3;
            }
            #message {
                margin-top: 15px;
                font-size: 1.1em;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Train Reservation</h1>
            <input type="text" id="name" placeholder="Name">
            <input type="text" id="id" placeholder="Passenger ID">
            <input type="number" id="age" placeholder="Age">
            <input type="number" id="priority" placeholder="Priority (optional)">
            <button onclick="reserve()">Reserve Seat</button>
            <div id="message"></div>
        </div>
        <script>
            async function reserve() {
                const name = document.getElementById('name').value;
                const id = document.getElementById('id').value;
                const age = parseInt(document.getElementById('age').value);
                const priority = parseInt(document.getElementById('priority').value) || 0;

                if (!name || !id || isNaN(age)) {
                    document.getElementById('message').style.color = "red";
                    document.getElementById('message').textContent = "Please fill in all required fields.";
                    return;
                }

                const response = await fetch('/reserve', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({name: name, id: id, age: age, priority: priority})
                });
                const data = await response.json();
                const messageDiv = document.getElementById('message');
                if (data.status === "confirmed") {
                    messageDiv.style.color = "green";
                    messageDiv.textContent = "Reservation confirmed for " + data.passenger.name + ".";
                } else if (data.status === "waiting") {
                    messageDiv.style.color = "orange";
                    messageDiv.textContent = "Reservation is on waiting list for " + data.passenger.name + ".";
                } else {
                    messageDiv.style.color = "red";
                    messageDiv.textContent = "An error occurred with your reservation.";
                }
            }
        </script>
    </body>
    </html>
    '''

# --- API Endpoint to Reserve a Seat ---
@app.route("/reserve", methods=["POST"])
def reserve_endpoint():
    data = request.get_json()
    name = data.get("name")
    pid = data.get("id")
    age = data.get("age")
    priority = data.get("priority", 0)
    passenger = Passenger(name, pid, age, priority)
    result = system.reserve(passenger)
    return jsonify(result)

# --- API Endpoint for Cancellation (if needed) ---
@app.route("/cancel", methods=["POST"])
def cancel():
    data = request.get_json()
    pid = data.get("id")
    result = system.cancel(pid)
    return jsonify(result)

# --- API Endpoint to Check Reservation Status ---
@app.route("/status", methods=["GET"])
def status():
    return jsonify(system.status())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
