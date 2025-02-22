import json
from abc import ABC, abstractmethod
from datetime import datetime


class Vehicle(ABC):
    def __init__(self, vehicle_id, brand, model, vehicle_type, rent_per_day):
        self.__vehicle_id = vehicle_id
        self.__brand = brand
        self.__model = model
        self.__vehicle_type = vehicle_type
        self.__rent_per_day = rent_per_day
        self.__available = True
        self.__renter_info = None
    
    def get_vehicle_id(self):
        return self.__vehicle_id
    
    def get_rent_per_day(self):
        return self.__rent_per_day
    
    def get_model(self):
        return self.__model
    
    def get_vehicle_type(self):
        return self.__vehicle_type
    
    def is_available(self):
        return self.__available
    
    def rent_vehicle(self, renter_name, contact_number, num_days):
        if self.__available:
            self.__available = False
            self.__renter_info = {
                "name": renter_name,
                "contact": contact_number,
                "num_days": num_days,
                "rent_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            return True
        return False
    
    def return_vehicle(self):
        self.__available = True
        self.__renter_info = None
    
    def get_renter_info(self):
        return self.__renter_info
    
    @abstractmethod
    def vehicle_info(self):
        pass

class Car(Vehicle):
    def __init__(self, vehicle_id, brand, model, vehicle_type, rent_per_day, seats, fuel_type):
        super().__init__(vehicle_id, brand, model, vehicle_type, rent_per_day)
        self.__seats = seats
        self.__fuel_type = fuel_type
    
    def vehicle_info(self):
        return f"Car: {self.get_vehicle_id()} - {self.get_model()} ({self.get_vehicle_type()}), {self.__seats} seats, {self.__fuel_type}"


class RentalSystem:
    def __init__(self):
        self.__vehicles = []
        self.load_data()
    
    def add_vehicle(self, vehicle):
        self.__vehicles.append(vehicle)
        self.save_data()
    
    def display_available_vehicles(self):
        available = [v.vehicle_info() for v in self.__vehicles if v.is_available()]
        return available if available else ["No vehicles available"]
    
    def display_rented_vehicles(self):
        rented = [f"{v.vehicle_info()} - {v.get_renter_info()}" for v in self.__vehicles if not v.is_available()]
        return rented if rented else ["No vehicles rented"]
    
    def search_available_vehicles(self, model=None, vehicle_type=None):
        results = [
            v.vehicle_info() for v in self.__vehicles if v.is_available() and
            (model is None or v.get_model().lower() == model.lower()) and
            (vehicle_type is None or v.get_vehicle_type().lower() == vehicle_type.lower())
        ]
        return results if results else ["No matching vehicles found"]
    
    def rent_vehicle(self, vehicle_id, renter_name, contact_number, num_days):
        for vehicle in self.__vehicles:
            if vehicle.get_vehicle_id() == vehicle_id and vehicle.is_available():
                vehicle.rent_vehicle(renter_name, contact_number, num_days)
                self.save_data()
                return f"Vehicle {vehicle_id} rented successfully."
        return f"Vehicle {vehicle_id} is not available."
    
    def return_vehicle(self, vehicle_id):
        for vehicle in self.__vehicles:
            if vehicle.get_vehicle_id() == vehicle_id:
                vehicle.return_vehicle()
                self.save_data()
                return f"Vehicle {vehicle_id} returned successfully."
        return f"Vehicle {vehicle_id} not found."
    
    def calculate_rent(self, vehicle_id):
        for vehicle in self.__vehicles:
            if vehicle.get_vehicle_id() == vehicle_id and not vehicle.is_available():
                renter_info = vehicle.get_renter_info()
                total_rent = vehicle.get_rent_per_day() * int(renter_info["num_days"])
                return f"Total rent for {vehicle_id} is ${total_rent}."
        return f"Vehicle {vehicle_id} is not currently rented."
    
    def save_data(self):
        data = []
        for vehicle in self.__vehicles:
            data.append({
                "vehicle_id": vehicle.get_vehicle_id(),
                "brand": vehicle.get_model(),
                "model": vehicle.get_model(),
                "vehicle_type": vehicle.get_vehicle_type(),
                "rent_per_day": vehicle.get_rent_per_day(),
                "available": vehicle.is_available(),
                "renter_info": vehicle.get_renter_info()
            })
        with open("rental_data.json", "w") as file:
            json.dump(data, file, indent=4)
    
    def load_data(self):
        try:
            with open("rental_data.json", "r") as file:
                data = json.load(file)
                for item in data:
                    car = Car(item["vehicle_id"], item["brand"], item["model"], item["vehicle_type"], item["rent_per_day"], 5, "Petrol")
                    if not item["available"]:
                        car.rent_vehicle(item["renter_info"]["name"], item["renter_info"]["contact"], item["renter_info"]["num_days"])
                    self.__vehicles.append(car)
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    rental_system = RentalSystem()
    
    while True:
        print("\nCar Rental System")
        print("1. Add a Car")
        print("2. Rent a Car")
        print("3. Return a Car")
        print("4. Show Available Cars")
        print("5. Show Rented Cars")
        print("6. Search Available Cars")
        print("7. Calculate Rent")
        print("8. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            vehicle_id = input("Enter vehicle ID: ")
            brand = input("Enter brand: ")
            model = input("Enter model: ")
            vehicle_type = input("Enter vehicle type (Sedan, SUV, Electric, etc.): ")
            rent_per_day = float(input("Enter rent per day: "))
            car = Car(vehicle_id, brand, model, vehicle_type, rent_per_day, 5, "Petrol")
            rental_system.add_vehicle(car)
            print("Car added successfully.")
        elif choice == "2":
            vehicle_id = input("Enter vehicle ID: ")
            name = input("Enter your name: ")
            contact = input("Enter your contact number: ")
            days = int(input("Enter number of days: "))
            print(rental_system.rent_vehicle(vehicle_id, name, contact, days))
        elif choice == "3":
            vehicle_id = input("Enter vehicle ID: ")
            print(rental_system.return_vehicle(vehicle_id))
        elif choice == "4":
            print("\n".join(rental_system.display_available_vehicles()))
        elif choice == "5":
            print("\n".join(rental_system.display_rented_vehicles()))
        elif choice == "7":
            vehicle_id = input("Enter vehicle ID: ")
            print(rental_system.calculate_rent(vehicle_id))
        elif choice == "8":
            break
        else:
            print("Invalid choice. Please try again.")