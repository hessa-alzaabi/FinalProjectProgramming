class Event:
   # Creates a new racing event
   def __init__(self, event_id, name, date, venue, capacity):
       self._event_id = event_id  # Unique ID for this event
       self._name = name  # Name of the event
       self._date = date  # When the event happens
       self._venue = venue  # Where the event takes place
       self._capacity = capacity  # Maximum number of people
       self._available_seats = capacity  # How many seats are left

   # Get the event ID
   def get_event_id(self):
       return self._event_id

   # Get the event name
   def get_name(self):
       return self._name

   # Get the event date
   def get_date(self):
       return self._date

   # Get the venue location
   def get_venue(self):
       return self._venue

   # Get total capacity
   def get_capacity(self):
       return self._capacity

   # Get available seats left
   def get_available_seats(self):
       return self._available_seats

   # Change the event name
   def set_name(self, name):
       self._name = name

   # Change the event date
   def set_date(self, date):
       self._date = date

   # Change the venue
   def set_venue(self, venue):
       self._venue = venue

   # Change total capacity
   def set_capacity(self, capacity):
    if capacity < 0:
        raise ValueError("Capacity must be non-negative")
    self._capacity = capacity
    if self._available_seats > capacity:
        self._available_seats = capacity  # Adjust available seats down

   # Update available seats
   def set_available_seats(self, seats):
    if not 0 <= seats <= self._capacity:
        raise ValueError("Available seats must be between 0 and capacity")
    self._available_seats = seats

   # Check how many seats are still available
   def check_availability(self):
       return self._available_seats

   # Update the number of available seats
   def reduce_seats(self, quantity):
       if quantity > self._available_seats:
           raise ValueError("Not enough seats available")
       self._available_seats -= quantity

   def increase_seats(self, quantity):
       if self._available_seats + quantity > self._capacity:
           raise ValueError("Exceeds maximum capacity")
       self._available_seats += quantity
