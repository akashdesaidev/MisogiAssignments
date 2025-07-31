from datetime import datetime, timedelta
import re

class Employee:
    company_name = ""
    total_employees = 0
    departments = {}
    tax_rates = {}
    next_employee_id = 1

    def __init__(self, name, department, base_salary, country, email):
        if not self.is_valid_department(department):
            raise ValueError("Invalid department.")
        if not self.validate_email(email):
            raise ValueError("Invalid email.")

        self.name = name
        self.department = department
        self.base_salary = base_salary
        self.country = country
        self.email = email
        self.hire_date = datetime.now()
        self.performance_ratings = []

        self.employee_id = self.generate_employee_id()

        Employee.total_employees += 1
        Employee.departments[department] += 1

    @staticmethod
    def validate_email(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

    @staticmethod
    def calculate_tax(salary, country):
        return salary * Employee.tax_rates.get(country, 0)

    @staticmethod
    def is_valid_department(dept):
        return dept in Employee.departments

    @classmethod
    def generate_employee_id(cls):
        year = datetime.now().year
        emp_id = f"EMP-{year}-{cls.next_employee_id:04d}"
        cls.next_employee_id += 1
        return emp_id

    @classmethod
    def from_csv_data(cls, csv_line):
        parts = csv_line.split(',')
        name, department, salary, country, email = parts
        return cls(name.strip(), department.strip(), float(salary), country.strip(), email.strip())

    @classmethod
    def get_department_stats(cls):
        stats = {}
        for dept, count in cls.departments.items():
            stats[dept] = {"count": count}
        return stats

    @classmethod
    def set_tax_rate(cls, country, rate):
        cls.tax_rates[country] = rate

    @classmethod
    def hire_bulk_employees(cls, employee_list):
        for line in employee_list:
            cls.from_csv_data(line)

    def add_performance_rating(self, rating):
        if 1 <= rating <= 5:
            self.performance_ratings.append(rating)

    def get_average_performance(self):
        if not self.performance_ratings:
            return 0
        return sum(self.performance_ratings) / len(self.performance_ratings)

    def calculate_net_salary(self):
        tax = self.calculate_tax(self.base_salary, self.country)
        return self.base_salary - tax

    def get_years_of_service(self):
        return (datetime.now() - self.hire_date).days // 365

    def is_eligible_for_bonus(self):
        return self.get_average_performance() > 3.5 and self.get_years_of_service() > 1