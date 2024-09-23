import os
import pickle

# Vehicle class created to declare the variables of a 'vehicle'
class Vehicle:
    # Defining and initializing the variables needed for the base vehicle
    def __init__(self, reg_number, make, model, colour, selling_price, cost, branch):
        self.reg_number = reg_number
        self.make = make
        self.model = model
        self.colour = colour
        self.selling_price = selling_price
        self.cost = cost
        self.branch = branch

    # Method to display details of the vehicle
    def display_details(self):
        print(f"Registration Number: {self.reg_number}")
        print(f"Make: {self.make}")
        print(f"Model: {self.model}")
        print(f"Colour: {self.colour}")
        print(f"Selling Price: £{self.selling_price}")
        print(f"Branch: {self.branch}")

# Subclass representing a car, inheriting from Vehicle
class Car(Vehicle):
    def __init__(self, reg_number, make, model, colour, selling_price, cost, branch, num_doors):
        super().__init__(reg_number, make, model, colour, selling_price, cost, branch)
        self.num_doors = num_doors

    # Method to display details of the car
    def display_details(self):
        super().display_details()
        print(f"Number of Doors: {self.num_doors}")

# Subclass representing a van, inheriting from Vehicle
class Van(Vehicle):
    def __init__(self, reg_number, make, model, colour, selling_price, cost, branch, capacity_kgs):
        super().__init__(reg_number, make, model, colour, selling_price, cost, branch)
        self.capacity_kgs = capacity_kgs

    # Method to display details of the van
    def display_details(self):
        super().display_details()
        print(f"Capacity (kgs): {self.capacity_kgs}")

# Subclass representing a minibus, inheriting from Vehicle
class Minibus(Vehicle):
    def __init__(self, reg_number, make, model, colour, selling_price, cost, branch, num_seats):
        super().__init__(reg_number, make, model, colour, selling_price, cost, branch)
        self.num_seats = num_seats

    # Method to display details of the minibus
    def display_details(self):
        super().display_details()
        print(f"Number of Seats: {self.num_seats}")

# Class to manage the vehicles
class VehicleManager:
    def __init__(self):
        self.vehicles = {}

    # Method to add a vehicle to the system
    def add_vehicle(self, vehicle):
        if vehicle.selling_price <= 0 or vehicle.cost <= 0:
            print("Selling price and cost must be greater than 0.")
            return False
        if '' in [vehicle.reg_number, vehicle.make, vehicle.model, vehicle.colour, vehicle.branch]:
            print("No blank entries allowed.")
            return False
        self.vehicles[vehicle.reg_number] = vehicle
        print("Vehicle added successfully.")
        return True

    # Method to display details of all the vehicles
    def display_all_vehicles(self):
        for vehicle in self.vehicles.values():
            vehicle.display_details()
            print()

    # Method used to search for vehicles based on a given criteria
    def search_vehicle(self, **kwargs):
        results = []
        for vehicle in self.vehicles.values():
            match = True
            for key, value in kwargs.items():
                if value == '':
                    continue
                if str(getattr(vehicle, key, None)).lower() != value.lower():
                    match = False
                    break
            if match:
                results.append(vehicle)
        return results

    # Method for making an offer on a vehicle in the system
    def make_offer(self, reg_number, offer_price):
        if reg_number in self.vehicles:
            vehicle = self.vehicles[reg_number]
            if offer_price >= vehicle.cost * 1.5:
                print("Offer accepted!")
                print(f"Contact branch at {vehicle.branch} for further details.")
            else:
                print("Offer too low. Must be at least 1.5 times the cost.")

    # Method to save the data to a pickle file
    def save_data(self, filename):
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(parent_dir, filename)
        with open(file_path, 'wb') as f:
            pickle.dump(self.vehicles, f)

    # Method to load the data from a pickle file
    def load_data(self, filename):
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(parent_dir, filename)
        try:
            with open(file_path, 'rb') as f:
                self.vehicles = pickle.load(f)
        except FileNotFoundError:
            # If file doesn't exist, initialize with empty dictionary
            self.vehicles = {}

# Main function that runs the program
def main():
    # Create an instance of VehicleManager
    manager = VehicleManager()
    # Load data from the pickle file
    manager.load_data("vehicles.pickle")

    # Display the main menu for the user to use
    while True:
        print("\n--- UWS Vehicle Sales ---")
        print("1. Add Vehicle")
        print("2. Display All Vehicles")
        print("3. Search Vehicles")
        print("4. Make Offer")
        print("5. Save and Exit")

        # Get the users input as a choice
        choice = input("Enter your choice: ")

        # Handle different user choices
        if choice == "1":
            # Choice 1 adds vehicle to the system given the correct criteria
            vehicle_type = input("Enter vehicle type (car/van/minibus): ").lower()
            reg_number = input("Enter registration number: ")
            make = input("Enter make: ")
            model = input("Enter model: ")
            colour = input("Enter colour: ")
            selling_price = float(input("Enter selling price: "))
            cost = float(input("Enter cost: "))
            branch = input("Enter branch: ")

            if vehicle_type == "car":
                num_doors = int(input("Enter number of doors: "))
                vehicle = Car(reg_number, make, model, colour, selling_price, cost, branch, num_doors)
            elif vehicle_type == "van":
                capacity_kgs = float(input("Enter capacity in kgs: "))
                vehicle = Van(reg_number, make, model, colour, selling_price, cost, branch, capacity_kgs)
            elif vehicle_type == "minibus":
                num_seats = int(input("Enter number of seats: "))
                vehicle = Minibus(reg_number, make, model, colour, selling_price, cost, branch, num_seats)
            else:
                print("Invalid vehicle type.")
                continue

            if manager.add_vehicle(vehicle):
                print("Vehicle added successfully.")

        elif choice == "2":
            # Choice 2 prints all vehicles in the database to the user using display_all_details method
            print("\n--- All Vehicles ---")
            manager.display_all_vehicles()

        elif choice == "3":
            # Choice 3 Searches vehicles in the system using given criteria
            print("\n--- Search Vehicles ---")
            search_criteria = {}
            search_criteria['reg_number'] = input("Enter registration number (leave blank to skip): ")
            search_criteria['make'] = input("Enter make (leave blank to skip): ")
            search_criteria['model'] = input("Enter model (leave blank to skip): ")
            search_criteria['colour'] = input("Enter colour (leave blank to skip): ")
            search_criteria['branch'] = input("Enter branch (leave blank to skip): ")

            results = manager.search_vehicle(**search_criteria)
            print("\n--- Search Results ---")
            if results:
                for vehicle in results:
                    vehicle.display_details()
            else:
                print("No matching vehicles found.")

        elif choice == "4":
            # Choice 4 allows the user to make an offer on a car, and informs the user if successful or not
            print("\n--- Make Offer ---")
            reg_number = input("Enter registration number of the vehicle: ")
            offer_price = float(input("Enter your offer price: "))
            manager.make_offer(reg_number, offer_price)

        elif choice == "5":
            # Choice 5 saves the data from the user to the pickled file, and quits the program
            manager.save_data("vehicles.pickle")
            print("Data saved. Exiting program.")
            break

        else:
            # Else catches any invalid entries from the user
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()