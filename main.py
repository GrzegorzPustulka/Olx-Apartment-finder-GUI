from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, \
    QDialog, QLabel, QListWidget, QMessageBox
from PyQt6 import uic
from PyQt6.QtGui import QPixmap
import sys


def exit_application() -> None:
    sys.exit(0)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.minPriceInput = None
        self.maxPriceInput = None
        self.districtsList = None
        self.selected_districts = None
        self.image_map = None
        uic.loadUi("MainWindow.ui", self)

        self.mapBtn.clicked.connect(self.open_map_image)
        self.exitBtn.clicked.connect(exit_application)
        self.searchBtn.clicked.connect(self.search_apartments)

    def open_map_image(self) -> None:
        self.image_map = QDialog(self)
        self.image_map.setFixedSize(800, 513)
        self.image_map.setWindowTitle("Map of Krakow districts")
        label = QLabel(self.image_map)
        pixmap = QPixmap('images/directs.jpg')
        label.setPixmap(pixmap)
        self.image_map.exec()

    def search_apartments(self):
        self.selected_districts = [item.text() for item in self.districtsList.selectedItems()]

        if len(self.selected_districts) == 0:
            QMessageBox.information(self, "Error", "You have not selected any district")

        for district in self.selected_districts:
            if district == "All":
                self.selected_districts = ["Bieńczyce", "Bieżanów", "Bieżanów-Prokocim", "Bronowice", "Czyżyny",
                                           "Dębniki", "Grzegórzki", "Krowodza", "Łagiewniki-Borek Fałęcki",
                                           "Mistrzejowice", "Nowa Huta", "Podgórze", "Podgórze Duchackie",
                                           "Prądnik Biały", "Prądnik Czerwony", "Stare Miasto", "Swoszowice",
                                           "Wzgórza Krzesławickie", "Zwierzyniec"]

        try:
            min_price = int(self.minPriceInput.text())
        except ValueError:
            min_price = None
            QMessageBox.information(self, "Error", "You entered the wrong minimum price.\nIt must be a integer")
        try:
            max_price = int(self.maxPriceInput.text())
        except ValueError:
            max_price = None
            QMessageBox.information(self, "Error", "You entered the wrong maximum price.\nIt must be a integer")


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())
