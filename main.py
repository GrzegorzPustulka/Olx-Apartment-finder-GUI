from PyQt6.QtWidgets import QApplication, QWidget, \
    QDialog, QLabel, QMessageBox
from PyQt6 import uic
from PyQt6.QtGui import QPixmap, QFont
import sys
from scraping import scraping_olx


def exit_application() -> None:
    sys.exit(0)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.roomRbtn = None
        self.searchLabel = None
        self.minPriceLabel = None
        self.maxPriceLabel = None
        self.kindLayout = None
        self.priceLayout = None
        self.descriptionLabel = None
        self.textDistrictsLabel = None
        self.mapBtn = None
        self.exitBtn = None
        self.searchBtn = None
        self.apartmentRbtn = None
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
                self.selected_districts = ["Bieńczyce", "Bieżanów-Prokocim", "Bronowice", "Czyżyny",
                                           "Dębniki", "Grzegórzki", "Krowodrza", "Łagiewniki-Borek Fałęcki",
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

        link = ""
        if self.apartmentRbtn.isChecked():
            link += "https://www.olx.pl/d/nieruchomosci/mieszkania/krakow/?page=1"
        elif self.roomRbtn.isChecked():
            link += "https://www.olx.pl/d/nieruchomosci/stancje-pokoje/krakow/?page=1"
        else:
            QMessageBox.information(self, "Error", "You have not chosen whether you want to\n"
                                                   "look for a room or an apartment")

        if len(self.selected_districts) > 0 and isinstance(min_price, int) and \
                isinstance(min_price, int) and len(link) > 0:
            self.searchBtn.deleteLater()
            self.districtsList.deleteLater()
            self.descriptionLabel.deleteLater()
            self.priceLayout.deleteLater()
            self.maxPriceInput.deleteLater()
            self.maxPriceLabel.deleteLater()
            self.minPriceInput.deleteLater()
            self.minPriceLabel.deleteLater()
            self.searchLabel.deleteLater()
            self.kindLayout.deleteLater()
            self.textDistrictsLabel.setText("Your filters: ")
            # change name
            self.textDistrictsLabel.setFixedSize(400, 50)
            self.textDistrictsLabel.setFont(QFont("Arial", 40))
            self.textDistrictsLabel.move(200, 30)

            scraping_olx(max_price, min_price, link, self.selected_districts)


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())
