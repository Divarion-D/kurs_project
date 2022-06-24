from PySide2 import QtWidgets
from gui_ui import Ui_Dialog
import sys

from common import Data

data_job = Data()

columns = data_job.get_columns()
listbox_columns = []
for i in columns:
    listbox_columns.append(columns[i])


class App(QtWidgets.QMainWindow, Ui_Dialog):
    def __init__(self):
        super().__init__()
        # Создание формы и Ui (наш дизайн)
        self.setupUi(self)
        self.show()

        self.searc_data = None
        self.dialog = QtWidgets.QMessageBox()

        self.url_data = 'https://mail2.dcz.gov.ua/publikaciya/6-perelik-aktualnyh-vakansiy-stanom-na-datu'

        self.update_data_btn.clicked.connect(self.digit_pressed)    # Update Data
        self.search_btn.clicked.connect(self.digit_pressed)         # Search
        self.export_txt_btn.clicked.connect(self.digit_pressed)     # Export txt
        self.export_pdf_btn.clicked.connect(self.digit_pressed)     # Export pdf
        self.exit_btn.clicked.connect(self.digit_pressed)           # Exit

        self.listWidget.clear()
        self.listWidget.addItems(listbox_columns)
        self.total_vac.setText(str(data_job.get_count_row()))

    def digit_pressed(self):
        sender = self.sender()
        if sender == self.update_data_btn:
            data_job.download_data(self.url_data)
            self.listWidget.clear()
            self.listWidget.addItems(listbox_columns)
        elif sender == self.search_btn:
            column_number = self.listWidget.currentRow()
            search_text = self.search_string.text()
            exact_search = self.exact_search.isChecked()
            self.searc_data = data_job.search_data(
                search_text, column_number, exact_search)
            self.found_vac.setText(str(len(self.searc_data)))
        elif sender == self.export_txt_btn:
            if self.searc_data != None:
                filename = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "Vacancies.txt")
                data_job.export_to_txt(self.searc_data, filename[0])
                self.dialog.setText("Successfully exported to txt")
                self.dialog.setDefaultButton(self.dialog.Ok)
                self.dialog.exec_()
        elif sender == self.export_pdf_btn:
            if self.searc_data != None:
                filename = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "Vacancies.pdf")
                data_job.export_to_pdf(self.searc_data, filename[0])
                self.dialog.setText("Successfully exported to pdf")
                self.dialog.setDefaultButton(self.dialog.Ok)
                self.dialog.exec_()
        elif sender == self.exit_btn:
            sys.exit()
        
    

if __name__ == '__main__':
    # Новый экземпляр QApplication
    app = QtWidgets.QApplication(sys.argv)
    # Сздание инстанса класса
    calc = App()
    # Запуск
    sys.exit(app.exec_())