import unittest
from datetime import date
from Models.user import User
from Models.ticket import Ticket
from Models.ticket_type import SingleRacePass, WeekendPackage, SeasonMembership, GroupDiscount
from Models.event import Event
from Models.order import Order
from Models.payment import Payment
from Models.admin import Admin
from Models.sales_report import SalesReport


class TestUser(unittest.TestCase):

    def setUp(self):
        self.user = User(1, "johndoe", "secure123", "s@lt", "John Doe", "john@example.com", "123456789", "123 Main St")

    def test_getters(self):
        self.assertEqual(self.user.get_user_id(), 1)
        self.assertEqual(self.user.get_username(), "johndoe")
        self.assertEqual(self.user.get_password(), "secure123")
        self.assertEqual(self.user.get_salt(), "s@lt")
        self.assertEqual(self.user.get_full_name(), "John Doe")
        self.assertEqual(self.user.get_email(), "john@example.com")
        self.assertEqual(self.user.get_phone_number(), "123456789")
        self.assertEqual(self.user.get_address(), "123 Main St")

    def test_setters(self):
        self.user.set_username("janedoe")
        self.assertEqual(self.user.get_username(), "janedoe")

        self.user.set_password("newpass")
        self.assertEqual(self.user.get_password(), "newpass")

        self.user.set_full_name("Jane Doe")
        self.assertEqual(self.user.get_full_name(), "Jane Doe")

        self.user.set_email("jane@example.com")
        self.assertEqual(self.user.get_email(), "jane@example.com")

        self.user.set_phone_number("987654321")
        self.assertEqual(self.user.get_phone_number(), "987654321")

        self.user.set_address("456 Main St")
        self.assertEqual(self.user.get_address(), "456 Main St")

    def test_login_success(self):
        self.assertTrue(self.user.login("johndoe", "secure123"))

    def test_login_failure(self):
        self.assertFalse(self.user.login("wrong", "wrong"))

    def test_purchase_history(self):
        self.assertEqual(len(self.user.get_purchase_history()), 0)
        self.user.add_purchase("Order1")
        self.assertEqual(len(self.user.get_purchase_history()), 1)
        self.assertIn("Order1", self.user.get_purchase_history())

    def test_update_profile(self):
        self.user.update_profile(full_name="Johnny", email="johnny@example.com", phone_number="111222333", address="New Place")
        self.assertEqual(self.user.get_full_name(), "Johnny")
        self.assertEqual(self.user.get_email(), "johnny@example.com")
        self.assertEqual(self.user.get_phone_number(), "111222333")
        self.assertEqual(self.user.get_address(), "New Place")
class TestTicket(unittest.TestCase):

    def setUp(self):
        self.ticket = Ticket("T001", 100.0, "2025-01-01", "2025-01-05")

    def test_getters(self):
        self.assertEqual(self.ticket.get_ticket_id(), "T001")
        self.assertEqual(self.ticket.get_price(), 100.0)
        self.assertEqual(self.ticket.get_validity_period(), ("2025-01-01", "2025-01-05"))
        self.assertTrue(self.ticket.is_available())
        self.assertEqual(self.ticket.get_type_name(), "Ticket")
        self.assertIsNone(self.ticket.get_event())

    def test_setters(self):
        self.ticket.set_price(120.0)
        self.assertEqual(self.ticket.get_price(), 120.0)

        self.ticket.set_validity_period("2025-02-01", "2025-02-05")
        self.assertEqual(self.ticket.get_validity_period(), ("2025-02-01", "2025-02-05"))

        self.ticket.update_availability(False)
        self.assertFalse(self.ticket.is_available())

    def test_display_details(self):
        detail = self.ticket.display_details()
        self.assertIn("Ticket ID: T001", detail)

class DummyTicket:
    def calculate_price(self, quantity):
        return 100 * quantity

class TestTicketTypes(unittest.TestCase):

    def test_single_race_pass(self):
        t = SingleRacePass("SinglePass", 50, "One race only", "2025-03-15", "A1")
        self.assertEqual(t.calculate_price(2), 120)

    def test_weekend_package(self):
        t = WeekendPackage("Weekend", 150, "All races", "2025-03-10", "2025-03-12", ["Qualifiers", "Main Race"])
        self.assertEqual(t.calculate_price(1), 190)

    def test_season_membership(self):
        t = SeasonMembership("Season", 300, "Full season", 2025, "Gold", ["Lounge", "Merch", "VIP Parking"])
        self.assertEqual(t.calculate_price(1), 345)

    def test_group_discount(self):
        base = DummyTicket()
        t = GroupDiscount("Group", 100, "Group deal", 5, 20, base)
        self.assertEqual(t.calculate_price(4), 400)  # No discount
        self.assertEqual(t.calculate_price(5), 400)  # Discount applied

class TestEvent(unittest.TestCase):

    def setUp(self):
        self.event = Event("E001", "Grand Prix", "2025-05-01", "Yas Marina", 100)

    def test_getters(self):
        self.assertEqual(self.event.get_event_id(), "E001")
        self.assertEqual(self.event.get_name(), "Grand Prix")
        self.assertEqual(self.event.get_date(), "2025-05-01")
        self.assertEqual(self.event.get_venue(), "Yas Marina")
        self.assertEqual(self.event.get_capacity(), 100)
        self.assertEqual(self.event.get_available_seats(), 100)

    def test_setters(self):
        self.event.set_name("New GP")
        self.assertEqual(self.event.get_name(), "New GP")

        self.event.set_date("2025-06-01")
        self.assertEqual(self.event.get_date(), "2025-06-01")

        self.event.set_venue("New Venue")
        self.assertEqual(self.event.get_venue(), "New Venue")

        self.event.set_capacity(80)
        self.assertEqual(self.event.get_capacity(), 80)

        with self.assertRaises(ValueError):
            self.event.set_capacity(-5)

        with self.assertRaises(ValueError):
            self.event.set_available_seats(200)

    def test_seat_management(self):
        self.assertEqual(self.event.check_availability(), 100)

        self.event.reduce_seats(10)
        self.assertEqual(self.event.check_availability(), 90)

        with self.assertRaises(ValueError):
            self.event.reduce_seats(100)

        self.event.increase_seats(5)
        self.assertEqual(self.event.check_availability(), 95)

class TestOrder(unittest.TestCase):
    def setUp(self):
        ticket1 = Ticket(1, 100.0, "2025-01-01", "2025-01-05")
        ticket2 = Ticket(2, 150.0, "2025-01-02", "2025-01-06")
        self.user = User(1, "testuser", "password123", "salt123", "Test User", "test@example.com", "1234567890",
                         "123 Test St")

        self.order = Order(101, "2025-05-13", "pending", self.user)
        self.order.add_ticket(ticket1)
        self.order.add_ticket(ticket2)

class TestPayment(unittest.TestCase):

    def setUp(self):
        self.payment = Payment(payment_id=201, amount=250.0, method="credit_card")

    def test_payment_fields(self):
        self.assertEqual(self.payment.get_payment_id(), 201)
        self.assertEqual(self.payment.get_amount(), 250.0)
        self.assertEqual(self.payment.get_method(), "credit_card")
        self.assertEqual(self.payment.get_status(), "pending")
        self.assertIsNone(self.payment.get_transaction_date())

    def test_status_setter(self):
        self.payment.set_status("processed")
        self.assertEqual(self.payment.get_status(), "processed")

    def test_process_payment(self):
        result = self.payment.process_payment()
        self.assertTrue(result)
        self.assertEqual(self.payment.get_status(), "processed")
        self.assertIsNotNone(self.payment.get_transaction_date())

    def test_verify_payment(self):
        self.payment.process_payment()
        self.assertTrue(self.payment.verify_payment())


class TestAdmin(unittest.TestCase):

    def setUp(self):
        self.admin = Admin(admin_id=1, username="admin", password="admin123", access_level="full")

    def test_admin_fields(self):
        self.assertEqual(self.admin.get_admin_id(), 1)
        self.assertEqual(self.admin.get_username(), "admin")
        self.assertEqual(self.admin.get_password(), "admin123")
        self.assertEqual(self.admin.get_access_level(), "full")

    def test_login_success_and_fail(self):
        self.assertTrue(self.admin.login("admin", "admin123"))
        self.assertFalse(self.admin.login("admin", "wrongpass"))

    def test_access_level_change(self):
        self.admin.set_access_level("limited")
        self.assertEqual(self.admin.get_access_level(), "limited")


class TestSalesReport(unittest.TestCase):

    def setUp(self):
        self.report = SalesReport(report_id=1, start_date="2025-05-01", end_date="2025-05-31")
        self.report.record_sale(date(2025, 5, 1))
        self.report.record_sale(date(2025, 5, 1))
        self.report.record_sale(date(2025, 5, 2))

    def test_sales_data(self):
        sales = self.report.get_sales_data()
        self.assertEqual(sales[date(2025, 5, 1)], 2)
        self.assertEqual(sales[date(2025, 5, 2)], 1)

    def test_generate_report(self):
        summary = self.report.generate_report()
        self.assertIn("2025-05-01: 2 ticket(s) sold", summary)
        self.assertIn("2025-05-02: 1 ticket(s) sold", summary)
        self.assertIn("Sales Report: 1 from 2025-05-01 to 2025-05-31", summary)


if __name__ == '__main__':
    unittest.main()