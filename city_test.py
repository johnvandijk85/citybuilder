import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QMessageBox,
)
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtCore import QTimer, QDate, Qt

class City:
    def __init__(self, name):
        self.name = name
        self.population = 1000
        self.funds = 5000
        self.happiness = 70
        self.tax_rate = 0.1
        self.buildings = []

    def get_status_text(self):
        return f"""
        Population: {self.population}
        Funds: ${self.funds}
        Happiness: {self.happiness}%
        Tax Rate: {self.tax_rate * 100}%
        Buildings: {', '.join(self.buildings)}
        """

    def collect_taxes(self):
        taxes = 0
        for building in self.buildings:
            if building == "House":
                taxes += 100
            elif building == "Factory":
                taxes += 500
        self.funds += taxes
        return taxes


class CityBuilder(QWidget):
    def __init__(self, city_name):
        super().__init__()
        self.city = City(city_name)  # Create an instance of the City class
        self.setWindowTitle(f"{self.city.name} City Builder")

        # Create year and month labels
        self.year_label = QLabel("2000")
        self.month_label = QLabel("January")

        # Set starting date to January 2000
        self.current_year = 2000
        self.current_month = 1

        # Create UI elements
        self.population_label = QLabel(f"Population: {self.city.population}")
        self.funds_label = QLabel(f"Funds: ${self.city.funds}")
        self.happiness_label = QLabel(f"Happiness: {self.city.happiness}%")
        self.tax_rate_label = QLabel(f"Tax Rate: {self.city.tax_rate * 100}%")
        self.buildings_label = QLabel(f"Buildings: {', '.join(self.city.buildings)}")

        self.build_house_button = QPushButton("Build House")
        self.build_factory_button = QPushButton("Build Factory")
        self.build_park_button = QPushButton("Build Park")
        self.collect_taxes_button = QPushButton("Collect Taxes")
        self.quit_button = QPushButton("Quit")

        # Layout
        self.layout = QVBoxLayout()
        status_layout = QHBoxLayout()
        buttons_layout = QGridLayout()

        status_layout.addWidget(self.population_label)
        status_layout.addWidget(self.funds_label)
        status_layout.addWidget(self.happiness_label)
        status_layout.addWidget(self.tax_rate_label)
        status_layout.addWidget(self.buildings_label)

        buttons_layout.addWidget(self.build_house_button, 0, 0)
        buttons_layout.addWidget(self.build_factory_button, 0, 1)
        buttons_layout.addWidget(self.build_park_button, 1, 0)
        buttons_layout.addWidget(self.collect_taxes_button, 2, 0)
        buttons_layout.addWidget(self.quit_button, 2, 1, 1, 2)

        self.layout.addWidget(self.year_label, alignment=Qt.AlignRight)
        self.layout.addWidget(self.month_label, alignment=Qt.AlignRight)

        # Add year and month labels
        status_layout.addWidget(self.year_label)
        status_layout.addWidget(self.month_label)

        self.layout.addLayout(status_layout)
        self.layout.addLayout(buttons_layout)

        self.setLayout(self.layout)

        self.build_house_button.clicked.connect(lambda: self.build("House"))
        self.build_factory_button.clicked.connect(lambda: self.build("Factory"))
        self.build_park_button.clicked.connect(lambda: self.build("Park"))
        self.collect_taxes_button.clicked.connect(self.collect_taxes)
        self.quit_button.clicked.connect(self.quit)

        # Timer for updating city status
        self.timer = QTimer()
        self.timer.setInterval(60000)  # Update every minute
        self.timer.timeout.connect(self.update_status)
        self.timer.start()

    def build(self, building):
        if building == "House":
            cost = 500
            if self.city.funds >= cost:
                self.city.funds -= cost
                self.city.population += 100
                self.city.buildings.append("House")
                print(f"You built a House! Population increased by 100.")
            else:
                print("Not enough funds to build a House.")

        elif building == "Factory":
            cost = 2000
            if self.city.funds >= cost:
                self.city.funds -= cost
                self.city.population += 200
                self.city.buildings.append("Factory")
                self.city.happiness -= 10
                print(f"You built a Factory! Population increased by 200, but happiness decreased by 10.")
            else:
                print("Not enough funds to build a Factory.")

        elif building == "Park":
            cost = 1000
            if self.city.funds >= cost:
                self.city.funds -= cost
                self.city.happiness += 20
                self.city.buildings.append("Park")
                print(f"You built a Park! Happiness increased by 20.")
            else:
                print("Not enough funds to build a Park.")

    def update_status(self):
        # Update city status labels
        self.population_label.setText(f"Population: {self.city.population}")
        self.funds_label.setText(f"Funds: ${self.city.funds}")
        self.happiness_label.setText(f"Happiness: {self.city.happiness}%")
        self.tax_rate_label.setText(f"Tax Rate: {self.city.tax_rate * 100}%")

        # Collect taxes automatically
        taxes = self.city.collect_taxes()
        print(f"Collected ${taxes} in taxes.")
        self.funds_label.setText(f"Funds: ${self.city.funds}")

        # Get current date
        current_date = QDate.currentDate()

        # Update year and month labels
        self.year_label.setText(str(current_date.year()))
        self.month_label.setText(current_date.toString("MMMM"))

        # Increment month if necessary
        if current_date.month() == 12:
            self.year_label.setText(str(current_date.year() + 1))
            self.month_label.setText("January")
        else:
            self.month_label.setText(current_date.addMonths(1).toString("MMMM"))

        # Update buildings label with a new line for each building
        self.buildings_label.setText(f"Buildings:\n{', '.join(self.city.buildings)}")

    def collect_taxes(self):
        taxes = self.city.collect_taxes()
        print(f"Collected ${taxes} in taxes.")
        self.funds_label.setText(f"Funds: ${self.city.funds}")

    def quit(self):
        # Ask for confirmation before quitting
        result = QMessageBox.question(
            self,
            "Quit",
            "Are you sure you want to quit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if result == QMessageBox.Yes:
            sys.exit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    city_name = input("Enter the name of your city: ")
    print(f"City name: {city_name}") 
    print("test3") # Add a print statement to check the city name
    city_builder = CityBuilder(city_name)
    city_builder.show()
    sys.exit(app.exec_())

