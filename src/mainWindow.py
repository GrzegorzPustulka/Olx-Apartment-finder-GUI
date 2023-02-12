from PyQt6.QtWidgets import QApplication, QWidget, \
    QDialog, QLabel, QMessageBox, QComboBox, QListWidget, QAbstractItemView
from PyQt6 import uic
from PyQt6.QtGui import QPixmap, QFont
import sys
from PIL import Image


def exit_application() -> None:
    sys.exit(0)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_city = None
        self.districts = None
        self.district_list = None
        self.allOffersRbtn = None
        self.newOffersRbtn = None
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
        uic.loadUi("mainWindow.ui", self)
        self.mapBtn.clicked.connect(self.open_map_image)
        self.exitBtn.clicked.connect(exit_application)
        self.searchBtn.clicked.connect(self.search_apartments)

        self.city_combo_box = QComboBox(self)
        self.city_combo_box.setFixedHeight(30)
        self.city_combo_box.setFixedWidth(110)
        font = self.city_combo_box.font()
        font.setPointSize(11)
        self.city_combo_box.setFont(font)
        self.city_combo_box.insertItem(0, "SELECT CITY")
        self.city_combo_box.setCurrentIndex(0)
        self.city_combo_box.addItem("Warszawa")
        self.city_combo_box.addItem("Kraków")
        self.city_combo_box.addItem("Wrocław")
        self.city_combo_box.addItem("Poznań")
        self.city_combo_box.addItem("Łódź")
        self.city_combo_box.addItem("Gdańsk")
        self.city_combo_box.addItem("Białystok")
        self.city_combo_box.addItem("Sopot")
        self.city_combo_box.addItem("Katowice")
        self.city_combo_box.addItem("Gdynia")
        self.city_combo_box.addItem("Gliwice")
        self.city_combo_box.move(10, 10)

        self.district_list = QListWidget(self)
        self.district_list.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.district_list.move(10, 40)
        self.district_list.setVisible(False)
        self.city_combo_box.activated.connect(self.update_district_list)
        self.city_combo_box.currentIndexChanged.connect(self.handle_selection_change)

    def handle_selection_change(self, index):
        if self.city_combo_box.itemText(index) == "SELECT CITY":
            self.city_combo_box.setCurrentIndex(0)
            for i in range(1, self.city_combo_box.count()):
                if self.city_combo_box.itemText(i) != "SELECT CITY":
                    self.city_combo_box.setCurrentIndex(i)
                    break
                    
    def update_district_list(self, index):
        self.district_list.setVisible(True)
        city = self.city_combo_box.currentText()
        self.district_list.clear()
        font = self.district_list.font()
        font.setPointSize(12)
        self.district_list.setFont(font)
        self.district_list.setFixedHeight(460)
        self.district_list.setFixedWidth(200)
        if city == "Warszawa":
            self.selected_city = "warszawa"
            self.districts = ["All", "Bemowo", "Białołęka", "Bielany", "Mokotów", "Ochota", "Praga-Południe",
                              "Praga-Północ", "Rembertów", "Śródmieście", "Targówek", "Ursus", "Ursynów",
                              "Wawer", "Wesoła", "Wilanów", "Włochy", "Wola", "Żoliborz"]

            for district in self.districts:
                self.district_list.addItem(district)
        elif city == "Kraków":
            self.selected_city = "krakow"
            self.districts = ["All", "Bieńczyce", "Bieżanów-Prokocim", "Bronowice", "Czyżyny",
                              "Dębniki", "Grzegórzki", "Krowodrza", "Łagiewniki-Borek Fałęcki",
                              "Mistrzejowice", "Nowa Huta", "Podgórze", "Podgórze Duchackie",
                              "Prądnik Biały", "Prądnik Czerwony", "Stare Miasto", "Swoszowice",
                              "Wzgórza Krzesławickie", "Zwierzyniec"]

            for district in self.districts:
                self.district_list.addItem(district)
        elif city == "Wrocław":
            self.selected_city = "wroclaw"
            self.districts = ["All", "Fabryczna", "Psie Pole", "Stare Miasto", "Śródmieście"]
            for district in self.districts:
                self.district_list.addItem(district)
        elif city == "Gdańsk":
            self.selected_city = "gdansk"
            self.districts = ["All", "Aniołki", "Brętowo", "Brzeźno", "Chełm z dzielnicą Gdańsk Południe", "Jasień",
                              "Kokoszki", "Krakowiec - Górki Zachodnie", "Letnica", "Matarnia", "Młyniska", "Nowy Port",
                              "Oliwa", "Olszynka", "Orunia - Św. Wojciech - Lipce", "Osowa", "Piecki-Migowo",
                              "Przymorze Wielkie", "Rudniki", "Siedlce", "Stogi z Przeróbką", "Strzyża", "Suchanino",
                              "Śródmieście", "Ujeścisko - Łostowice", "VII Dwór", "Wrzeszcz", "Wyspa Sobieszewska",
                              "Wzgórze Mickiewicza", "Zaspa Młyniec", "Zaspa Roztaje",
                              "Żabianka - Wejhera - Jelitkowo - Tysiąclecia"]

            for district in self.districts:
                self.district_list.addItem(district)
        elif city == "Łódź":
            self.selected_city = "lodz"
            self.districts = ["All", "Bałuty", "Górna", "Polesie", "Śródmieście", "Widzew"]

            for district in self.districts:
                self.district_list.addItem(district)
        elif city == "Poznań":
            self.selected_city = "poznan"
            self.districts = ["All", "Chartowo", "Dębiec", "Górczyn", "Grunwald", "Jeżyce", "Junikowo", "Komandoria",
                              "Łacina", "Ławica", "Łazarz", "Naramowice", "Ogrody", "Piątkowo", "Podolany", "Rataje",
                              "Smochowice", "Sołacz", "Stare Miasto", "Starołęka", "Strzeszyn", "Szczepankowo", "Śródka",
                              "Warszawskie", "Wilda", "Winiary", "Winogrady"]

            for district in self.districts:
                self.district_list.addItem(district)
        elif city == "Gdynia":
            self.selected_city = "gdynia"
            self.districts = ["All", "Babie Doły", "Chwarzno-Wiczlino", "Chylonia", "Cisowa", "Dąbrowa", "Działki Leśne",
                              "Grabówek", "Kamienna Góra", "Karwiny", "Leszczynki", "Mały Kack", "Obłuże", "Oksywie",
                              "Orłowo", "Podgórze", "Pustki Cisowskie-Demptowo", "Redłowo", "Śródmieście", "Wielki Kack",
                              "Witomino-Leśniczówka", "Witomino-Radiostacja", "Wzgórze Świętego Maksymiliana"]

            for district in self.districts:
                self.district_list.addItem(district)
        elif city == "Sopot":
            self.selected_city = "sopot"
            self.districts = ["All", "Centrum", "Dolny Sopot", "Górny Sopot"]

            for district in self.districts:
                self.district_list.addItem(district)
        elif city == "Białystok":
            self.selected_city = "bialystok"
            self.districts = ["All", "Antoniuk", "Bacieczki", "Bema", "Białostoczek", "Bojary", "Centrum", "Dojlidy",
                              "Dojlidy Górne", "Dziesięciny I", "Dziesięciny II", "Jaroszówka", "Kawaleryjskie",
                              "Leśna Dolina", "Mickiewicza", "Młodych", "Nowe Miasto", "Piaski", "Piasta I", "Piasta II",
                              "Przydworcowe", "Sienkiewicza", "Skorupy", "Słoneczny Stok", "Starosielce", "Wygoda",
                            "Wysoki Stoczek", "Zawady", "Zielone Wzgórza"]
            for district in self.districts:
                self.district_list.addItem(district)
        elif city == "Gliwice":
            self.selected_city = "gliwice"
            self.districts = ["All", "Bojków", "Brzezinka", "Czechowice", "Kopernika", "Ligota Zabrska", "Łabędy",
                              "Obrońców Pokoju", "Ostropa", "Politechnika", "Sikornik", "Sośnica", "Stare Gliwice",
                              "Szobiszowice", "Śródmieście", "Trynek", "Wilcze Gardło", "Wojska Polskiego",
                              "Wójtowa Wieś", "Zatorze", "Żerniki"]

            for district in self.districts:
                self.district_list.addItem(district)
        elif city == "Katowice":
            self.selected_city = "katowice"
            self.districts = ["All", "Bogucice", "Brynów-cz. Wsch.-Osiedle Zgrzebioka", "Dąb", "Dąbrówka Mała", "Giszowiec",
                              "Janów-Nikiszowiec", "Kostuchna", "Koszutka", "Ligota-Panewniki", "Murcki",
                              "Osiedle Paderewskiego-Muchowiec", "Osiedle Tysiąclecia", "Osiedle Witosa",
                              "Piotrowice-Ochojec", "Podlesie", "Szopienice-Burowiec", "Śródmieście", "Wełnowiec-Józefowiec",
                              "Załęska Hałda-Brynów cz. Zach.", "Załęże", "Zarzecze", "Zawodzie"]

            for district in self.districts:
                self.district_list.addItem(district)

    def open_map_image(self) -> None:
        if self.selected_city is not None:
            path = "../images/"+self.selected_city + ".png"
            img = Image.open(path)
            width, height = img.size
            self.image_map = QDialog(self)
            self.image_map.setFixedSize(width, height)
            self.image_map.setWindowTitle("Map of districts")
            label = QLabel(self.image_map)
            pixmap = QPixmap(path)
            label.setPixmap(pixmap)
            self.image_map.exec()
        else:
            QMessageBox.information(self, "Info", "You have not selected any city")

    def search_apartments(self) -> None:
        self.selected_districts = [item.text() for item in self.district_list.selectedItems()]

        if len(self.selected_districts) == 0:
            QMessageBox.information(self, "Error", "You have not selected any district")

        self.districts.remove("All")

        for district in self.selected_districts:
            if district == "All":
                self.selected_districts = self.districts

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
            link += "https://www.olx.pl/d/nieruchomosci/mieszkania/wynajem/"+self.selected_city+"/"
        elif self.roomRbtn.isChecked():
            link += "https://www.olx.pl/d/nieruchomosci/stancje-pokoje/"+self.selected_city+"/"
        else:
            QMessageBox.information(self, "Error", "You have not chosen whether you want to\n"
                                                   "look for a room or an apartment")

        if len(self.selected_districts) > 0 and isinstance(min_price, int) and \
                isinstance(min_price, int) and len(link) > 0:
            if self.allOffersRbtn.isChecked() and self.apartmentRbtn.isChecked():
                window.close()
                from allApartmentScraping import run_all_apartments
                run_all_apartments(max_price, min_price, link, self.selected_districts)
            elif self.allOffersRbtn.isChecked() and self.roomRbtn.isChecked():
                window.close()
                from allRoomsScraping import run_all_rooms
                run_all_rooms(max_price, min_price, link, self.selected_districts)
            elif self.newOffersRbtn.isChecked() and self.apartmentRbtn.isChecked():
                window.close()
                from newApartmentScraping import new_apartments_scraping
                new_apartments_scraping(max_price, min_price, link, self.selected_districts)
            elif self.newOffersRbtn.isChecked() and self.roomRbtn.isChecked():
                window.close()
                from newRoomScraping import new_room_scraping
                new_room_scraping(max_price, min_price, link, self.selected_districts)
            else:
                QMessageBox.information(self, "Error", "You have not chosen whether you want to\n"
                                                       "look for new or all ad")


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())
