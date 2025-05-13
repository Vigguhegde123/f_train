@app.route("/reserve", methods=["POST"])
def reserve():
    data = request.get_json()
    name = data.get("name")
    pid = data.get("id")
    age = data.get("age")
    priority = data.get("priority", 0)
    phone = data.get("phone")
    passenger = Passenger(name, pid, age, priority, phone)
    result = system.reserve(passenger)
    msg = f"Hi {name}, your reservation is {result['status']}."
    if phone:
        send_sms(phone, msg)
    return jsonify(result)

@app.route("/cancel", methods=["POST"])
def cancel():
    data = request.get_json()
    pid = data.get("id")
    result = system.cancel(pid)
    if result.get("moved_from_waiting"):
        moved = result["moved_from_waiting"]
        send_sms(moved["phone"], f"Hi {moved['name']}, your reservation is now confirmed!")
    return jsonify(result)
