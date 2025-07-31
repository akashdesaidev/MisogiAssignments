from datetime import datetime, timedelta

class MaintenanceRecord:
    def __init__(self):
        self.last_service_date = datetime.now()
        self.maintenance_notes = []

    def add_note(self, note):
        self.maintenance_notes.append(note)
        self.last_service_date = datetime.now()

class Vehicle(MaintenanceRecord):
    def __init__(self, vehicle_id, make, model, year, daily_rate, fuel_type="Petrol"):
        super().__init__()
        self.vehicle_id = vehicle_id
        self.make = make
        self.model = model
        self.year = year
        self.daily_rate = daily_rate
        self.is_available = True
        self.mileage = 0
        self.fuel_type = fuel_type

    def rent(self):
        if self.is_available:
            self.is_available = False
            return "Rented successfully"
        return "Vehicle not available"

    def return_vehicle(self):
        self.is_available = True
        return "Returned"

    def calculate_rental_cost(self, days):
        return self.daily_rate * days

    def get_vehicle_info(self):
        return f"{self.make} {self.model} ({self.year})"

    def get_fuel_efficiency(self):
        return None

class Car(Vehicle):
    def __init__(self, vehicle_id, make, model, year, daily_rate, seating_capacity, transmission_type, has_gps):
        super().__init__(vehicle_id, make, model, year, daily_rate, fuel_type="Petrol")
        self.seating_capacity = seating_capacity
        self.transmission_type = transmission_type
        self.has_gps = has_gps

    def calculate_rental_cost(self, days):
        return self.daily_rate * days

    def get_fuel_efficiency(self):
        if self.transmission_type.lower() == "automatic":
            return {"city_mpg": 22, "highway_mpg": 30}
        else:
            return {"city_mpg": 26, "highway_mpg": 35}

class Motorcycle(Vehicle):
    def __init__(self, vehicle_id, make, model, year, daily_rate, engine_cc, bike_type):
        super().__init__(vehicle_id, make, model, year, daily_rate, fuel_type="Petrol")
        self.engine_cc = engine_cc
        self.bike_type = bike_type

    def calculate_rental_cost(self, days):
        if days < 7:
            return self.daily_rate * days * 0.8  # 20% discount
        return self.daily_rate * days

    def get_fuel_efficiency(self):
        return 45  # average MPG for motorcycle

class Truck(Vehicle):
    def __init__(self, vehicle_id, make, model, year, daily_rate, cargo_capacity, license_required, max_weight):
        super().__init__(vehicle_id, make, model, year, daily_rate, fuel_type="Diesel")
        self.cargo_capacity = cargo_capacity
        self.license_required = license_required
        self.max_weight = max_weight

    def calculate_rental_cost(self, days):
        return self.daily_rate * days * 1.5  # 50% surcharge

    def get_fuel_efficiency(self):
        return {"empty_mpg": 12, "loaded_mpg": 8}