from abc import ABC, abstractmethod
class TicketType(ABC):
   # Base class for different types of tickets
   def __init__(self, type_name, base_price, description=""):
       self._type_name = type_name  # Name of this ticket type
       self._base_price = base_price  # Starting price
       self._description = description  # What this ticket includes

   # Get the name of this ticket type
   def get_type_name(self):
       return self._type_name

   # Get the base price
   def get_base_price(self):
       return self._base_price

   # Get the description
   def get_description(self):
       return self._description

   # Change the ticket type name
   def set_type_name(self, name):
       self._type_name = name

   # Change the base price
   def set_base_price(self, price):
       self._base_price = price

   # Change the description
   def set_description(self, description):
       self._description = description

   # Calculate the final price
   @abstractmethod
   def calculate_price(self, quantity=1):
       raise NotImplementedError("Must override in subclass")


class SingleRacePass(TicketType):
   # Ticket for just one race day
   def __init__(self, type_name, base_price, description, race_day, seat_section):
       super().__init__(type_name, base_price, description)
       self._race_day = race_day  # Which day is the race
       self._seat_section = seat_section  # Where you sit

   # Get the race day
   def get_race_day(self):
       return self._race_day

   # Get the seat section
   def get_seat_section(self):
       return self._seat_section

   # Change the race day
   def set_race_day(self, day):
       self._race_day = day

   # Change the seat section
   def set_seat_section(self, section):
       self._seat_section = section

   # Calculate price for single race
   def calculate_price(self, quantity=1):
       return (self._base_price + 10) * quantity


class WeekendPackage(TicketType):
   # Ticket for the whole weekend with multiple events
   def __init__(self, type_name, base_price, description, start_date, end_date, included_events):
       super().__init__(type_name, base_price, description)
       self._start_date = start_date  # Weekend starts
       self._end_date = end_date  # Weekend ends
       self._included_events = included_events  # What events are included

   # Get weekend start date
   def get_start_date(self):
       return self._start_date

   # Get weekend end date
   def get_end_date(self):
       return self._end_date

   # Get list of included events
   def get_included_events(self):
       return self._included_events

   # Calculate price
   def calculate_price(self, quantity=1):
        return (self._base_price + len(self._included_events) * 20) * quantity


class SeasonMembership(TicketType):
   # Membership for the entire racing season
   def __init__(self, type_name, base_price, description, season, membership_level, perks):
       super().__init__(type_name, base_price, description)
       self._season = season  # Which season
       self._membership_level = membership_level  # Bronze, Silver, Gold, etc.
       self._perks = perks  # Extra benefits included

   # Get the season year
   def get_season(self):
       return self._season

   # Get membership level
   def get_membership_level(self):
       return self._membership_level

   # Get list of perks
   def get_perks(self):
       return self._perks

   # Calculate price
   def calculate_price(self, quantity=1):
       return (self._base_price + len(self._perks) * 15) * quantity


class GroupDiscount(TicketType):
    def __init__(self, type_name, base_price, description, group_size, discount_percentage, base_ticket_type):
        super().__init__(type_name, base_price, description)
        self._group_size = group_size
        self._discount_percentage = discount_percentage
        self._base_ticket_type = base_ticket_type


    def get_group_size(self):
        return self._group_size
    

    def get_discount_percentage(self):
        return self._discount_percentage
    

    def get_base_ticket_type(self):
        return self._base_ticket_type
    

    def calculate_price(self, quantity=1):
        base_price = self._base_ticket_type.calculate_price(quantity)
        if quantity >= self._group_size:
            return base_price * (1 - self._discount_percentage / 100)
        return base_price
    
    
    def set_discount_percentage(self, percentage):  # Added method
        self._discount_percentage = percentage

