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
    QInputDialog,
    QDialog,
    QRadioButton,
)
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtCore import QTimer, QDate, Qt

#just a branch test

class City:
    def __init__(self, name):
        self.name = name
        self.population = 1000
        self.funds = 5000
        self.happiness = 70
        self.tax_rate = 0.0025
        self.buildings = {}  # Use a dictionary to store building counts

    def get_status_text(self):
        building_summary = "\n".join(
            f"{building_type}: {count}"
            for building_type, count in self.buildings.items()
        )
        return f"""
        Population: {self.population}
        Funds: ${self.funds}
        Happiness: {self.happiness}%
        Tax Rate: {self.tax_rate * 100}%
        Buildings:
        {building_summary}
        """

    def collect_taxes(self):
        taxes = 0
        for building_type, count in self.buildings.items():
            if building_type == "House":
                taxes += 100 * count
            elif building_type == "Factory":
                taxes += 500 * count
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
        self.buildings_label = QLabel(f"Buildings: {self.city.get_status_text()}")

        self.build_house_button = QPushButton("Build House")
        self.build_factory_button = QPushButton("Build Factory")
        self.build_park_button = QPushButton("Build Park")
        self.collect_taxes_button = QPushButton("Collect Taxes")
        self.quit_button = QPushButton("Quit")

        # Layout
        self.layout = QVBoxLayout()
        status_layout = QHBoxLayout()
        buttons_layout = QGridLayout()

        # Add status labels to the status layout
        #status_layout.addWidget(self.population_label)
        #status_layout.addWidget(self.funds_label)
        #status_layout.addWidget(self.happiness_label)
        #status_layout.addWidget(self.tax_rate_label)
        status_layout.addWidget(self.buildings_label)

        # Add buttons to the buttons layout
        buttons_layout.addWidget(self.build_house_button, 0, 0)
        buttons_layout.addWidget(self.build_factory_button, 0, 1)
        buttons_layout.addWidget(self.build_park_button, 1, 0)
        buttons_layout.addWidget(self.collect_taxes_button, 2, 0)
        buttons_layout.addWidget(self.quit_button, 2, 1, 1, 2)

        # Add year and month labels to the top right corner
        self.layout.addWidget(self.year_label, alignment=Qt.AlignRight)
        self.layout.addWidget(self.month_label, alignment=Qt.AlignRight)

        # Add the status and buttons layouts to the main layout
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
        self.timer.setInterval(5000)  # Update every minute
        self.timer.timeout.connect(self.update_status)
        self.timer.start()

        # Create a map instance
        self.map = Map(10, 10)

        # Create a map widget
        self.map_widget = MapWidget(self.map)

        # Add the map widget to the layout
        self.layout.addWidget(self.map_widget)

    def build(self, building):
        if building == "House":
            cost = 500
            if self.city.funds >= cost:
                self.city.funds -= cost
                self.city.population += 100
                self.city.buildings.setdefault("House", 0)
                self.city.buildings["House"] += 1
                print(f"You built a House! Population increased by 100.")
            else:
                print("Not enough funds to build a House.")

        elif building == "Factory":
            cost = 2000
            if self.city.funds >= cost:
                self.city.funds -= cost
                self.city.population += 200
                self.city.buildings.setdefault("Factory", 0)
                self.city.buildings["Factory"] += 1
                self.city.happiness -= 10
                print(f"You built a Factory! Population increased by 200, but happiness decreased by 10.")
            else:
                print("Not enough funds to build a Factory.")

        elif building == "Park":
            cost = 1000
            if self.city.funds >= cost:
                self.city.funds -= cost
                self.city.happiness += 20
                self.city.buildings.setdefault("Park", 0)
                self.city.buildings["Park"] += 1
                print(f"You built a Park! Happiness increased by 20.")
            else:
                print("Not enough funds to build a Park.")

    def get_clicked_square(self):
        # Get the mouse click event information
        event = self.map_widget.mousePressEvent

        # Calculate the square coordinates based on the click position
        x = event.x() // self.map_widget.square_size
        y = event.y() // self.map_widget.square_size

        return x, y

        # Get the clicked square coordinates
        x, y = self.get_clicked_square()

        # Build the selected building on the map
        if building_type == "House":
            self.map.set_square(x, y, House())
        elif building_type == "Factory":
            self.map.set_square(x, y, Factory())
        elif building_type == "Park":
            self.map.set_square(x, y, Park())

        # Update the map display
        self.update_map_display()

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

        # Increment month and year if necessary
        if self.current_month == 12:
            self.current_year += 1
            self.current_month = 1
        else:
            self.current_month += 1

        # Update year and month labels
        self.year_label.setText(str(self.current_year))
        self.month_label.setText(QDate(self.current_year, self.current_month, 1).toString("MMMM"))

        # Update buildings label with a summary
        self.buildings_label.setText(f"Buildings:\n{self.city.get_status_text()}")

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

    def update_map_display(self):
        self.map_widget.update()  # Trigger a repaint of the map widget

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x = event.x() // self.map_widget.square_size
            y = event.y() // self.map_widget.square_size
            self.build_dialog(x, y)

    def build_dialog(self, x, y):
        dialog = QDialog(self)  # Create a QDialog instance
        dialog.setWindowTitle("Build")

        # Add radio buttons for building types
        house_button = QRadioButton("House")
        factory_button = QRadioButton("Factory")
        park_button = QRadioButton("Park")

        # Add a button to confirm the selection
        build_button = QPushButton("Build")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(house_button)
        layout.addWidget(factory_button)
        layout.addWidget(park_button)
        layout.addWidget(build_button)
        dialog.setLayout(layout)

        # Connect the button click to a function
        build_button.clicked.connect(lambda: self.build_selected(x, y, dialog))

        # Show the dialog
        dialog.exec_()

    def build_selected(self, x, y, dialog):
        # Get the selected building type
        for button in dialog.findChildren(QRadioButton):
            if button.isChecked():
                building_type = button.text()
                break

        # Build the selected building on the map
        self.build(building_type)

        # Close the dialog
        dialog.close()

class StartWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("City Builder")

        # Create UI elements
        self.start_button = QPushButton("Start")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.start_button)
        self.setLayout(layout)

        # Connect button click to a function
        self.start_button.clicked.connect(self.start_game)

    def start_game(self):
        # Get city name from user input
        city_name, ok = QInputDialog.getText(self, "City Name", "Enter the name of your city:")
        if ok:
            # Close the start window and open the city builder window
            self.close()
            #from city_game import CityBuilder
            city_builder = CityBuilder(city_name)
            city_builder.show()
        else:
            # Show an error message if the user cancels
            QMessageBox.warning(self, "Error", "Please enter a city name.")

    

class MapWidget(QWidget):
    def __init__(self, map):
        super().__init__()
        self.map = map
        self.square_size = 50  # Size of each square in pixels

    def paintEvent(self, event):
        painter = QPainter(self)
        for y in range(self.map.height):
            for x in range(self.map.width):
                building = self.map.get_square(x, y)
                if building:
                    color = building.color
                else:
                    color = Qt.blue
                painter.fillRect(x * self.square_size, y * self.square_size, self.square_size, self.square_size, color)

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]

    def get_square(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            building = self.grid[y][x]
            if not building:
                building = Building(color=Qt.blue)  # Create a default building with blue color
                self.grid[y][x] = building
            return building
        else:
            return None

    def set_square(self, x, y, building):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = building
        else:
            raise ValueError("Invalid coordinates")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StartWindow()
    window.show()
    sys.exit(app.exec_())
