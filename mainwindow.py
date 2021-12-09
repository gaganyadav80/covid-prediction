import sys

from PyQt6.QtCore import Qt, QCoreApplication
from PyQt6.QtWidgets import QApplication, QMainWindow

from app import Ui_MainWindow
from covidCasesFuzzy import covid_severity_predictor

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._translate = QCoreApplication.translate
        self.Spread_in_your_locality = 0.4
        self.Climate_Temp_Celsius = 30
        self.Body_Temp_Fahrenheit = 98
        self.Shortness_Of_Breath = 2

        self.covid_slider.valueChanged.connect(self.on_covid_slider_change)
        self.breadth_slider.valueChanged.connect(self.on_breadth_slider_change)
        self.area_box.valueChanged.connect(self.on_area_value_change)
        self.body_box.valueChanged.connect(self.on_body_value_change)

        self.start_button.clicked.connect(self.on_start_button)

    def print_var(self):
        print("\nSpread    : ", self.Spread_in_your_locality)
        print("Climate   : ", self.Climate_Temp_Celsius)
        print("Body      : ", self.Body_Temp_Fahrenheit)
        print("Shortness : ", self.Shortness_Of_Breath, "\n")

    def on_start_button(self):
        # self.print_var()
        covid_severity_predictor(self.Spread_in_your_locality,
            self.Climate_Temp_Celsius, self.Body_Temp_Fahrenheit, self.Shortness_Of_Breath)

    def on_covid_slider_change(self, val):
        value = (val/100)*2;
        self.covid_value_label.setText(self._translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">" + str(value) + "</span></p></body></html>"))
        self.Spread_in_your_locality = value
        
    def on_breadth_slider_change(self, val):
        self.breadth_value_label.setText(self._translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">" + str(val) + "</span></p></body></html>"))
        self.Shortness_Of_Breath = val

    def on_area_value_change(self, val):
        self.Climate_Temp_Celsius = val;

    def on_body_value_change(self, val):
        self.Body_Temp_Fahrenheit = val;


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()