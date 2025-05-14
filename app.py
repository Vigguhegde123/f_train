# app.py

from flask import Flask, request, jsonify, render_template
from train_reservation import TrainReservationSystem

app = Flask(__name__)
system = TrainReservationSystem()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book', methods=['POST'])
def book():
    data = request.json
    response = system.book_ticket(data)
    return jsonify(response)

@app.route('/bookings')
def bookings():
    return jsonify(system.get_bookings())

@app.route('/cancel/<int:index>', methods=['DELETE'])
def cancel(index):
    response = system.cancel_ticket(index)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
