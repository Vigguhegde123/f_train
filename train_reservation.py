# train_reservation.py

class TrainReservationSystem:
    def __init__(self):
        self.bookings = []

    def book_ticket(self, data):
        self.bookings.append(data)
        return {"status": "success", "message": "Ticket booked successfully"}

    def get_bookings(self):
        return self.bookings

    def cancel_ticket(self, index):
        if 0 <= index < len(self.bookings):
            self.bookings.pop(index)
            return {"status": "success", "message": "Booking canceled"}
        else:
            return {"status": "error", "message": "Invalid booking index"}
