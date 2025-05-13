# Represents an event ticket
class Ticket:
    def __init__(self, ticket_id, price, validity_start, validity_end, is_available=True):
        self._ticket_id = ticket_id  # Unique ID for this ticket
        self._price = price  # How much the ticket costs
        self._validity_period = (validity_start, validity_end)  # When ticket is valid
        self._is_available = is_available  # Availability status

    # Get the ticket ID
    def get_ticket_id(self):
        return self._ticket_id

    # Get the ticket price
    def get_price(self):
        return self._price

    # Get when this ticket is valid
    def get_validity_period(self):
        return self._validity_period

    # Check if this ticket can be bought
    def is_available(self):
        return self._is_available

    # Change the ticket price
    def set_price(self, price):
        self._price = price

    # Change when the ticket is valid
    def set_validity_period(self, start, end):
        self._validity_period = (start, end)

    # Mark ticket as available or sold
    def update_availability(self, available):
        self._is_available = available

    # Show ticket information
    def display_details(self):
        start, end = self._validity_period
        return (
            f"Ticket ID: {self._ticket_id}, "
            f"Price: ${self._price:.2f}, "
            f"Validity: {start} to {end}, "
            f"Available: {'Yes' if self._is_available else 'No'}"
        )
    #Get the name of the Ticket type
    def get_type_name(self):
        return "Ticket"

    #Get the ticket event
    def get_event(self):
        return None