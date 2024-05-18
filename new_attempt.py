import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QInputDialog,
    QMessageBox,
)

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
            from city_test import CityBuilder
            city_builder = CityBuilder(city_name)
            city_builder.show()
        else:
            # Show an error message if the user cancels
            QMessageBox.warning(self, "Error", "Please enter a city name.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StartWindow()
    window.show()
    sys.exit(app.exec_())
