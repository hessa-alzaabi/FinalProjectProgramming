class User:
    def __init__(self, user_id, username, password, salt, full_name, email, phone_number, address):
        self._user_id = user_id
        self._username = username
        self._password = password
        self._salt = salt  # Store salt
        self._full_name = full_name
        self._email = email
        self._phone_number = phone_number
        self._address = address
        self._purchase_history = []  # Changed to list
    def get_user_id(self):
        return self._user_id
    def get_username(self):
        return self._username
    def get_password(self):
        return self._password
    def get_salt(self):
        return self._salt  # Corrected to use _salt
    def get_full_name(self):
        return self._full_name
    def get_email(self):
        return self._email
    def get_phone_number(self):
        return self._phone_number
    def get_address(self):
        return self._address
    def get_purchase_history(self):
        return self._purchase_history
    def set_username(self, username):
        self._username = username
    def set_password(self, password):
        self._password = password
    def set_full_name(self, full_name):
        self._full_name = full_name
    def set_email(self, email):
        self._email = email
    def set_phone_number(self, phone_number):
        self._phone_number = phone_number
    def set_address(self, address):
        self._address = address
    def register(self):
        return True
    def login(self, username, password):
        return self._username == username and self._password == password
    def update_profile(self, full_name=None, email=None, phone_number=None, address=None):
        if full_name:
            self._full_name = full_name
        if email:
            self._email = email
        if phone_number:
            self._phone_number = phone_number
        if address:
            self._address = address
    def add_purchase(self, order):
        self._purchase_history.append(order)
    def view_purchase_history(self):
        return self._purchase_history