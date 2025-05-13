from flask import Flask, request, jsonify, send_from_directory
import heapq
from flask_cors import CORS
import os

app = Flask(__name__, static_folder="static")
CORS(app)

# Your Passenger and TrainReservationSystem classes remain unchanged

system = TrainReservationSystem()

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/reserve", methods=["POST"])
def reserve():
    data = request.get_json()
    name = data.get("name")
    pid = data.get("id")
    age = data.get("age")
    priority = data.get("priority", 0)
    passenger = Passenger(name, pid, age, priority)
    result = system.reserve(passenger)
    return jsonify(result)

@app.route("/cancel", methods=["POST"])
def cancel():
    data = request.get_json()
    pid = data.get("id")
    result = system.cancel(pid)
    return jsonify(result)

@app.route("/status", methods=["GET"])
def status():
    return jsonify(system.status())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
