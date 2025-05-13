import datetime
class SalesReport:
   # Creates reports about ticket sales
   def __init__(self, report_id, start_date, end_date, sales_data=None):
       self._report_id = report_id  # Unique report ID
       self._start_date = start_date  # Report period starts
       self._end_date = end_date  # Report period ends
       # Initialize sales data as an empty dictionary if not passed
       self._sales_data = sales_data if sales_data is not None else {}

   # Get the report ID
   def get_report_id(self):
       return self._report_id

   # Get report start date
   def get_start_date(self):
       return self._start_date

   # Get report end date
   def get_end_date(self):
       return self._end_date

   # Get sales data
   def get_sales_data(self):
       return self._sales_data

   # Record a ticket sale on a given date
   def record_sale(self, sale_date):
        if isinstance(sale_date, datetime.date):
            sale_date = sale_date
            if sale_date not in self._sales_data:
                self._sales_data[sale_date] = 0
            self._sales_data[sale_date] += 1 

   # Generate a formatted report
   def generate_report(self):
       header = f"Sales Report: {self._report_id} from {self._start_date} to {self._end_date}"
       report_lines = [f"{date}: {count} ticket(s) sold" for date, count in sorted(self._sales_data.items())]
       return header + "\n" + "\n".join(report_lines)

   # Save report to a file
   def export_report(self):
       filename = f"{self._report_id}_sales_report.txt"
       with open(filename, "w") as file:
           file.write(self.generate_report())
       return filename