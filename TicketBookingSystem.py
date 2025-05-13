# Import all needed libraries
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime
import pickle
import hashlib
import os

# Import our custom classes
from Models.user import User
from Models.ticket import Ticket
from Models.ticket_type import TicketType, SingleRacePass, WeekendPackage, SeasonMembership, GroupDiscount
from Models.order import Order
from Models.payment import Payment
from Models.admin import Admin
from Models.sales_report import SalesReport

# Files where we save data
USERS_FILE = "users.pickle"
ORDERS_FILE = "orders.pickle"

# Helper functions for file operations
def load_data(filename):
   """Load data from a pickle file"""
   try:
       with open(filename, "rb") as f:
           return pickle.load(f)
   except (FileNotFoundError, EOFError):
       return []

def save_data(filename, data):
   """Save data to a pickle file"""
   with open(filename, "wb") as f:
       pickle.dump(data, f)

def hash_password(password):
   """Make password secure by hashing it"""
   salt = os.urandom(16)
   hashed = hashlib.sha256(salt + password.encode()).hexdigest()
   return salt, hashed

def verify_password(stored_salt, stored_hash, password):
    """Verify password using stored salt and hash"""
    return stored_hash == hashlib.sha256(stored_salt + password.encode()).hexdigest()

# Create different types of tickets
def get_ticket_types():
    race_pass = SingleRacePass("Single Race", 120, "Access to one race day", "Friday", "Main Grandstand")
    weekend = WeekendPackage("Weekend Pass", 300, "All weekend events", "2025-11-10", "2025-11-12", ["Practice", "Qualifying", "Race"])
    season = SeasonMembership("Season Ticket", 1000, "All-season access", "2025", "Gold", ["VIP Lounge", "Pit Access", "Free Merch"])
    group = GroupDiscount("Group Deal", 0, "Discounted for groups", 5, 15,
                          SingleRacePass("Group Race", 120, "Group race day", "Friday", "South Zone"))

    return {
        "RacePass": race_pass,
        "Weekend": weekend,
        "Season": season,
        "Group": group
    }


# Create the ticket types once at startup
TICKET_TYPES = get_ticket_types()

# Main application class
class BookingSystemApp:
   def __init__(self, root):
       """Set up the main application window"""
       self.root = root
       self.root.title("Grand Prix Ticket Booking System")
       self.root.geometry("600x500")
       self.users = load_data(USERS_FILE)  # Initialize user list here
       self.current_user = None  # Track who is logged in

       # Create tabs for different functions
       self.tabs = ttk.Notebook(self.root)
       self.login_tab()      # Tab for login/register
       self.booking_tab()    # Tab for booking tickets
       self.profile_tab()    # Tab for managing profile
       self.admin_tab()      # Tab for admin functions
       self.tabs.pack(expand=True, fill="both")

       # Disable other tabs until user logs in
       for i in range(1, 4):
           self.tabs.tab(i, state="disabled")

   def login_tab(self):
       """Create the login and registration tab"""
       tab = ttk.Frame(self.tabs)
       self.tabs.add(tab, text="Login / Register")

       # Create input form
       frame = ttk.LabelFrame(tab, text="Account Access", padding=10)
       frame.pack(padx=20, pady=20)

       # Add labels and input fields
       ttk.Label(frame, text="Username:").grid(row=0, column=0)
       ttk.Label(frame, text="Email:").grid(row=1, column=0)
       ttk.Label(frame, text="Password:").grid(row=2, column=0)

       self.username_entry = ttk.Entry(frame)
       self.email_entry = ttk.Entry(frame)
       self.password_entry = ttk.Entry(frame, show="*")  # Hide password
       self.username_entry.grid(row=0, column=1)
       self.email_entry.grid(row=1, column=1)
       self.password_entry.grid(row=2, column=1)

       # Add buttons
       ttk.Button(frame, text="Register", command=self.register).grid(row=3, column=0, pady=10)
       ttk.Button(frame, text="Login", command=self.login).grid(row=3, column=1)

   def booking_tab(self):
       """Create the ticket booking tab"""
       tab = ttk.Frame(self.tabs)
       self.tabs.add(tab, text="Book Ticket")

       # Create booking form
       frame = ttk.LabelFrame(tab, text="Choose Ticket", padding=10)
       frame.pack(padx=20, pady=20)

       # Ticket type selection
       ttk.Label(frame, text="Ticket Type:").grid(row=0, column=0, sticky="e")
       self.ticket_var = tk.StringVar()
       ticket_menu = ttk.OptionMenu(frame, self.ticket_var, "RacePass", *TICKET_TYPES.keys())
       ticket_menu.grid(row=0, column=1)

       self.ticket_info_label = ttk.Label(frame, text="", wraplength=400)
       self.ticket_info_label.grid(row=1, column=0, columnspan=2, pady=5)

       self.ticket_var.trace_add("write", self.update_ticket_info)
       self.update_ticket_info()

       # Quantity selection
       ttk.Label(frame, text="Quantity:").grid(row=2, column=0)
       self.qty_entry = ttk.Entry(frame)
       self.qty_entry.grid(row=2, column=1)

       ttk.Label(frame, text="Card Number:").grid(row=3, column=0)
       self.card_entry = ttk.Entry(frame)
       self.card_entry.grid(row=3, column=1)

       # Book button
       ttk.Button(frame, text="Book Now", command=self.book_ticket).grid(row=4, columnspan=2, pady=10)


   def profile_tab(self):
       """Create the profile management tab"""
       tab = ttk.Frame(self.tabs)
       self.tabs.add(tab, text="Manage Profile")

       # Create profile form
       frame = ttk.LabelFrame(tab, text="Your Details", padding=10)
       frame.pack(padx=20, pady=10)

       # Profile fields
       ttk.Label(frame, text="Full Name:").grid(row=0, column=0)
       ttk.Label(frame, text="Phone:").grid(row=1, column=0)
       ttk.Label(frame, text="Address:").grid(row=2, column=0)

       self.fullname_entry = ttk.Entry(frame)
       self.phone_entry = ttk.Entry(frame)
       self.address_entry = ttk.Entry(frame)

       self.fullname_entry.grid(row=0, column=1)
       self.phone_entry.grid(row=1, column=1)
       self.address_entry.grid(row=2, column=1)

       # Update button
       ttk.Button(frame, text="Update Profile", command=self.update_profile).grid(row=3, columnspan=2, pady=5)

       #Delete account button
       ttk.Button(frame, text="Delete Account", command=self.delete_account).grid(row=4, columnspan=2, pady=5)

       # Order management
       order_frame = ttk.LabelFrame(tab, text="Your Orders", padding=10)
       order_frame.pack(fill="x", padx=20)

       self.orders_list = tk.Listbox(order_frame, height=5)
       self.orders_list.pack(fill="x", pady=5)

       #Refresh orders button
       ttk.Button(order_frame, text="Refresh Orders", command=self.load_user_orders).pack()

       #Delete the selected order button
       ttk.Button(order_frame, text="Delete Selected Order", command=self.delete_selected_order).pack(pady=5)

   def admin_tab(self):
       """Create the admin management tab"""
       tab = ttk.Frame(self.tabs)
       self.tabs.add(tab, text="Admin Panel")

       # Sales report button
       ttk.Button(tab, text="Generate Sales Report", command=self.generate_report).pack(pady=10)

       #Modify and apply discount
       ttk.Label(tab, text="Update Group Discount (%):").pack()
       self.discount_entry = ttk.Entry(tab)
       self.discount_entry.pack()
       ttk.Button(tab, text="Apply Discount", command=self.update_discount).pack(pady=5)
  
   def show_user_menu(self):
        for i in range(1, 4):
            self.tabs.tab(i, state="normal")

   def register(self):
    username = self.username_entry.get()
    email = self.email_entry.get()
    password = self.password_entry.get()
    if not username or not email or not password:
        messagebox.showerror("Input Error", "Please fill all fields.")
        return
    users = load_data(USERS_FILE)
    if any(u.get_email() == email for u in users):
        messagebox.showerror("Error", "Email already registered.")
        return
    salt, hashed_password = hash_password(password)
    user_id = f"U{int(datetime.now().timestamp())}"
    user = User(user_id, username, hashed_password, salt, "", email, "", "")
    users.append(user)
    save_data(USERS_FILE, users)
    self.current_user = user
    self.users = users  # Update in-memory list
    self.show_user_menu()
    messagebox.showinfo("Welcome", f"Welcome, {username}! You have been registered and logged in.") 

   def login(self):
        """Log in an existing user"""
        email = self.email_entry.get().lower()
        password = self.password_entry.get()
        for user in self.users:
            print(f"Checking user: {user.get_email().lower()}")
            if user.get_email().lower() == email:
                print("Email match found.")
                user_salt = user.get_salt()
                user_password = user.get_password()
                if user_salt and user_password:
                    if verify_password(user_salt, user_password, password):
                        self.current_user = user
                        messagebox.showinfo("Success", f"Welcome, {user.get_full_name()}!")
                        self.show_user_menu()
                        return
                    else:
                        messagebox.showerror("Error", "Incorrect password.")
                        return
                else:
                    messagebox.showerror("Error", "User data corrupted.")
                    return
        messagebox.showerror("Error", "User not found.")

   def update_profile(self):
        """Update user profile information"""
        if not self.current_user:
            messagebox.showerror("Not Logged In", "You must log in first.")
            return
        # Get all fields
        username = self.fullname_entry.get().strip()
        phone = self.phone_entry.get().strip()
        address = self.address_entry.get().strip()
        # Validate input
        if not username or not phone or not address:
            messagebox.showerror("Input Error", "Please fill all fields.")
            return
        # Update current user object
        self.current_user.set_full_name(username)  # Corrected method name
        self.current_user.set_phone_number(phone)
        self.current_user.set_address(address)
        # Update users list
        users = load_data(USERS_FILE)
        for i, user in enumerate(users):
            if user.get_user_id() == self.current_user.get_user_id():
                users[i] = self.current_user
                break
        save_data(USERS_FILE, users)
        messagebox.showinfo("Profile Updated", "Your profile has been updated.")

   #Delete the user account
   def delete_account(self):
       if not self.current_user:
           return
       confirm = messagebox.askyesno("Confirm", "Delete your account and all orders?")
       if confirm:
           users = load_data(USERS_FILE)
           users = [u for u in users if u.get_user_id() != self.current_user.get_user_id()]
           save_data(USERS_FILE, users)

           orders = load_data(ORDERS_FILE)
           orders = [o for o in orders if o.get_user_id() != self.current_user.get_user_id()]
           save_data(ORDERS_FILE, orders)

           self.current_user = None
           messagebox.showinfo("Deleted", "Account and orders deleted.")
           self.root.destroy()

   #Loads the user orders
   def load_user_orders(self):
    if not self.current_user:
        return
    orders = load_data(ORDERS_FILE)
    self.orders_list.delete(0, tk.END)
    for order in orders:
        if order.get_user().get_user_id() == self.current_user.get_user_id():
            self.orders_list.insert(tk.END, f"{order.get_order_id()} | {order.get_ticket_type()} x{len(order.get_tickets())} = ${order.get_total()}")

   #Deletes the user selected order
   def delete_selected_order(self):
       if not self.current_user:
           return
       selection = self.orders_list.curselection()
       if not selection:
           messagebox.showerror("Error", "Select an order to delete.")
           return
       order_id = self.orders_list.get(selection[0]).split("|")[0].strip()

       orders = load_data(ORDERS_FILE)
       orders = [o for o in orders if o.get_order_id() != order_id]
       save_data(ORDERS_FILE, orders)
       self.load_user_orders()
       messagebox.showinfo("Deleted", f"Order {order_id} deleted.")

   #Updates the ticket information
   def update_ticket_info(self, *args):
       ticket = TICKET_TYPES[self.ticket_var.get()]
       info = f"{ticket.get_type_name()}: {ticket.get_description()}\nPrice: ${ticket.calculate_price()}"
       self.ticket_info_label.config(text=info)


   def book_ticket(self):
    """Book tickets for a user"""
    if not self.current_user:
        return
    ticket_type = self.ticket_var.get()
    quantity = self.qty_entry.get()
    card = self.card_entry.get()
    # Validate quantity input
    try:
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid", "Enter a valid quantity.")
        return
    if len(card) != 16 or not card.isdigit():
        messagebox.showerror("Payment Error", "Enter a 16-digit card number.")
        return
    # Get the selected ticket object
    ticket_obj = TICKET_TYPES[ticket_type]
    total_price = ticket_obj.calculate_price(quantity)
    # Handle group discount dynamically
    if ticket_type == "Group" and quantity >= ticket_obj.get_group_size():
        total_price *= (1 - ticket_obj.get_discount_percentage() / 100)
    # Create payment record
    payment_id = f"P{int(datetime.now().timestamp())}"
    payment = Payment(payment_id, total_price, "credit_card", transaction_date=datetime.now().strftime("%Y-%m-%d"))
    # Create order
    order_id = f"O{int(datetime.now().timestamp())}"
    order = Order(order_id, datetime.now(), "confirmed", self.current_user)
    # Create and add Ticket objects
    for _ in range(quantity):
        ticket_id = f"T{int(datetime.now().timestamp())}"
        single_ticket_price = ticket_obj.calculate_price(1)  # Price for one ticket
        ticket = Ticket(ticket_id, single_ticket_price, datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%Y-%m-%d"))
        order.add_ticket(ticket)
    # Save order
    orders = load_data(ORDERS_FILE)
    orders.append(order)
    save_data(ORDERS_FILE, orders)
    messagebox.showinfo("Booked", f"Tickets booked!\nOrder ID: {order_id}\nTotal: ${total_price:.2f}")
    self.qty_entry.delete(0, tk.END)
    self.card_entry.delete(0, tk.END)


   def generate_report(self):
        """Generate a sales report"""
        orders = load_data(ORDERS_FILE)
        report_id = f"R{int(datetime.now().timestamp())}"
        current_date = datetime.now().date()
        report = SalesReport(report_id, current_date, current_date)
        for order in orders:
            order_date = order.get_order_date().date() if isinstance(order.get_order_date(), datetime) else order.get_order_date()
            report.record_sale(order_date)
        total_sales = sum(order.get_total() for order in orders)
        report_text = f"Total orders: {len(orders)}\nTotal Sales: ${total_sales:.2f}\n\n{report.generate_report()}"
        messagebox.showinfo("Sales Report", report_text)

   def update_discount(self):
        """Update the group discount value"""
        new_discount = self.discount_entry.get()
        try:
            new_discount = float(new_discount)
            if not (0 <= new_discount <= 100):
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid", "Enter a valid percentage between 0-100.")
            return
        group_ticket = TICKET_TYPES.get("Group")
        if isinstance(group_ticket, GroupDiscount):
            group_ticket.set_discount_percentage(new_discount)  # Corrected method name
            messagebox.showinfo("Updated", f"Group discount updated to {new_discount}%.")
        else:
            messagebox.showerror("Error", "Group ticket type not found.")


# --- Launch the app ---
if __name__ == "__main__":
    root = tk.Tk()
    app = BookingSystemApp(root)
    root.mainloop()




