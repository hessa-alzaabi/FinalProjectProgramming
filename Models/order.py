class Order:
   # Creates a new order for ticket purchases
   def __init__(self, order_id, order_date, status="pending", user=None):
       self._order_id = order_id        # Unique ID for this order
       self._order_date = order_date    # When the order was made
       self._tickets = []               # List of tickets in this order
       self._status = status            # Current order status
       self._user = user                # Who placed this order

   # Get the order ID
   def get_order_id(self):
       return self._order_id

   # Get when the order was placed
   def get_order_date(self):
       return self._order_date

   # Get all tickets in this order
   def get_tickets(self):
       return self._tickets
   
   def get_user_id(self):
        return self._user.get_user_id() if self._user else None

   def get_total(self):
        return sum(ticket.get_price() for ticket in self._tickets)
   
   # Get the order status
   def get_status(self):
       return self._status

   # Get who made this order
   def get_user(self):
       return self._user
   
   def get_ticket_type(self):
        return self._tickets[0].get_type_name() if self._tickets else "Unknown"

   # Change the order status
   def set_status(self, status):
       if status not in ("pending", "confirmed", "cancelled"):
           raise ValueError("Invalid order status")
       self._status = status

   # Add a ticket to this order
   def add_ticket(self, ticket):
       if hasattr(ticket, "get_price") and callable(ticket.get_price):
           self._tickets.append(ticket)
       else:
           raise TypeError("Invalid ticket object: missing get_price method")

   # Remove a ticket from the order
   def remove_ticket(self, ticket):
       if ticket in self._tickets:
           self._tickets.remove(ticket)

       # Confirm order and reduce available seats for each ticket’s event
       def process_order(self):
           if not self._tickets:
               raise ValueError("Cannot process an empty order")

           for ticket in self._tickets:
               if hasattr(ticket, "get_event") and ticket.get_event():
                   event = ticket.get_event()
                   if hasattr(event, "reduce_seats") and callable(event.reduce_seats):
                       event.reduce_seats(1)
                   else:
                       raise AttributeError("Event does not support seat reduction")
               else:
                   raise ValueError("Ticket is not associated with a valid event")

           self._status = "confirmed"
           return True
