from datetime import datetime
class Payment:
    #Allows multiple payment methods
    ACCEPTED_METHODS = ["credit_card", "debit_card", "cash", "paypal"]

    # Handles payment for an order
    def __init__(self, payment_id, amount, method, status="pending", transaction_date=None):
        if method not in self.ACCEPTED_METHODS:
            raise ValueError(f"Unsupported payment method. Choose from: {', '.join(self.ACCEPTED_METHODS)}")
        self._payment_id = payment_id
        self._amount = amount
        self._method = method
        self._status = status
        self._transaction_date = transaction_date

    # Get the payment ID
    def get_payment_id(self):
       return self._payment_id

    # Get the payment amount
    def get_amount(self):
       return self._amount

    # Get the payment method
    def get_method(self):
       return self._method

    # Get the payment status
    def get_status(self):
       return self._status

    # Get when payment was made
    def get_transaction_date(self):
       return self._transaction_date

    # Change the payment status
    def set_status(self, status):
       self._status = status

    #Change the transaction date
    def set_transaction_date(self, date=None):
        self._transaction_date = datetime.now()

    # Process the payment
    def process_payment(self):
        self._status = "processed"
        if self._transaction_date is None:
            self._transaction_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return True

    # Verify if payment was successful based on the method
    def verify_payment(self):
        if self._method in ["credit_card", "debit_card", "paypal"]:
            return self._status == "processed"
        elif self._method == "cash":
            return self._status == "paid_on_delivery"
        return False


