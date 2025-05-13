# Creates a new user with personal information
class User:
    def __init__(self, user_id, username, password, salt, full_name, email, phone_number, address):
        # Store all user details privately
        self._user_id = user_id
        self._username = username
        self._password = password
        self._salt = salt  # Store salt
        self._full_name = full_name
        self._email = email
        self._phone_number = phone_number
        self._address = address
        self._purchase_history = []  # Keep track of orders

    # Get the user's ID
    def get_user_id(self):
        return self._user_id

    # Get the username
    def get_username(self):
        return self._username

    # Get the password
    def get_password(self):
        return self._password
    #Get the salt used for hashing the user's password
    def get_salt(self):
        return self._salt

    # Get the full name
    def get_full_name(self):
        return self._full_name

    # Get the email address
    def get_email(self):
        return self._email

    # Get the phone number
    def get_phone_number(self):
        return self._phone_number

    # Get the address
    def get_address(self):
        return self._address

    # Get the list of past orders
    def get_purchase_history(self):
        return self._purchase_history

    # Update the username
    def set_username(self, username):
        self._username = username

    # Update the password
    def set_password(self, password):
        self._password = password

    # Update the full name
    def set_full_name(self, full_name):
        self._full_name = full_name

    # Update the email address
    def set_email(self, email):
        self._email = email

    # Update the phone number
    def set_phone_number(self, phone_number):
        self._phone_number = phone_number

    # Update the address
    def set_address(self, address):
        self._address = address

    # Register a new user in the system
    def register(self):
        return True

    # Check if login details are correct
    def login(self, username, password):
        return self._username == username and self._password == password

    # Update user's personal information
    def update_profile(self, full_name=None, email=None, phone_number=None, address=None):
        if full_name:
            self._full_name = full_name
        if email:
            self._email = email
        if phone_number:
            self._phone_number = phone_number
        if address:
            self._address = address

    # Add an order to the user's purchase history
    def add_purchase(self, order):
        self._purchase_history.append(order)

    # Show all previous purchases
    def view_purchase_history(self):
        return self._purchase_history