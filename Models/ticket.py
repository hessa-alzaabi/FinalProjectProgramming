class Ticket:
    def __init__(self, ticket_id, price, validity_start, validity_end, is_available=True):
        self._ticket_id = ticket_id
        self._price = price
        self._validity_period = (validity_start, validity_end)
        self._is_available = is_available
    def get_ticket_id(self):
        return self._ticket_id
    def get_price(self):
        return self._price
    def get_validity_period(self):
        return self._validity_period
    def is_available(self):
        return self._is_available
    def set_price(self, price):
        self._price = price
    def set_validity_period(self, start, end):
        self._validity_period = (start, end)
    def update_availability(self, available):
        self._is_available = available
    def display_details(self):
        start, end = self._validity_period
        return (
            f"Ticket ID: {self._ticket_id}, "
            f"Price: ${self._price:.2f}, "
            f"Validity: {start} to {end}, "
            f"Available: {'Yes' if self._is_available else 'No'}"
        )
    def get_type_name(self):
        return "Ticket"
    def get_event(self):
        return None