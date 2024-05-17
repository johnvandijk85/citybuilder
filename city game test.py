import random

class City:
    def __init__(self, name):
        self.name = name
        self.population = 1000
        self.funds = 10000
        self.buildings = ["Town Hall"]
        self.happiness = 50
        self.tax_rate = 0.1  # 10% tax rate

    def build(self, building):
        if building == "House":
            cost = 500
            if self.funds >= cost:
                self.funds -= cost
                self.population += 100
                self.buildings.append("House")
                print(f"You built a House! Population increased by 100.")
            else:
                print("Not enough funds to build a House.")

        elif building == "Factory":
            cost = 2000
            if self.funds >= cost:
                self.funds -= cost
                self.population += 200
                self.buildings.append("Factory")
                self.happiness -= 10
                print(f"You built a Factory! Population increased by 200, but happiness decreased by 10.")
            else:
                print("Not enough funds to build a Factory.")

        elif building == "Park":
            cost = 1000
            if self.funds >= cost:
                self.funds -= cost
                self.happiness += 20
                self.buildings.append("Park")
                print(f"You built a Park! Happiness increased by 20.")
            else:
                print("Not enough funds to build a Park.")

    def status(self):
        print(f"\n==== {self.name} ====")
        print(f"Population: {self.population}")
        print(f"Funds: ${self.funds}")
        print(f"Happiness: {self.happiness}%")
        print(f"Tax Rate: {self.tax_rate * 100}%")
        print("Buildings:", ", ".join(self.buildings))

        # Collect taxes
        taxes = int(self.population * self.tax_rate)
        self.funds += taxes
        print(f"Collected ${taxes} in taxes.")

def main():
    city_name = input("Enter the name of your city: ")
    city = City(city_name)

    while True:
        # Check for disasters
        disaster_chance = 0.01  # 1% chance of disaster
        if random.random() < disaster_chance:
            disaster_type = random.choice(["Fire", "Earthquake", "Tornado"])
            print(f"\n===== {disaster_type} Disaster! =====")
            population_loss = int(city.population * 0.1)
            funds_loss = int(city.funds * 0.2)
            city.population -= population_loss
            city.funds -= funds_loss
            city.happiness -= 20
            print(f"Population decreased by {population_loss}.")
            print(f"Funds decreased by ${funds_loss}.")
            print("Some buildings were destroyed.")
            print(f"Happiness decreased by 20%.")

        print("\nWhat would you like to do?")
        print("1. Build a House")
        print("2. Build a Factory")
        print("3. Build a Park")
        print("4. View City Status")
        print("5. Quit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            city.build("House")
        elif choice == "2":
            city.build("Factory")
        elif choice == "3":
            city.build("Park")
        elif choice == "4":
            city.status()
        elif choice == "5":
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()