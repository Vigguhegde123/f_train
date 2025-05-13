from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory storage for reservations
reservations = []

@app.route('/reserve', methods=['POST'])
def reserve():
    data = request.get_json()
    # Basic validation
    if not all(k in data for k in ('name', 'id', 'age')):
        return jsonify({'error': 'Missing required fields'}), 400
    # Check for duplicate ID
    if any(r['id'] == data['id'] for r in reservations):
        return jsonify({'error': 'Reservation with this ID already exists'}), 400
    reservations.append(data)
    return jsonify({'message': 'Reservation successful', 'data': data}), 200

@app.route('/cancel', methods=['POST'])
def cancel():
    data = request.get_json()
    pid = data.get('id')
    global reservations
    reservations = [r for r in reservations if r['id'] != pid]
    return jsonify({'message': f'Reservation for ID {pid} cancelled'}), 200

@app.route('/status', methods=['GET'])
def status():
    return jsonify({'reservations': reservations}), 200

if __name__ == '__main__':
    app.run(debug=True)
