from .sales_report import SalesReport
from .ticket_type import TicketType

class Admin:
   # Creates an admin user for managing the system
   def __init__(self, admin_id, username, password, access_level="full"):
       self._admin_id = admin_id  # Unique admin ID
       self._username = username  # Admin login name
       self._password = password  # Admin password
       self._access_level = access_level  # What admin can access

   # Get the admin ID
   def get_admin_id(self):
       return self._admin_id

   # Get the admin username
   def get_username(self):
       return self._username

   # Get the admin password
   def get_password(self):
       return self._password

   # Get the access level
   def get_access_level(self):
       return self._access_level

   # Change the access level
   def set_access_level(self, level):
       self._access_level = level

   # Admin login to system
   def login(self, username, password):
       return self._username == username and self._password == password #Checks admin username and password

   # Create and view sales reports
   def view_sales_report(self, report: SalesReport):
       return report.generate_report()

   # Apply and modify discount settings
   def apply_discount(self, ticket_type: TicketType, percentage: float):
       if not 0 <= percentage <= 100:
           raise ValueError("Discount must be between 0 and 100%")
       ticket_type.apply_discount(percentage)


