from PySide2 import QtWidgets
from PySide2 import QtGui
from gui_ui import Ui_Dialog
from itertools import groupby


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
        # set window size
        self.setFixedSize(self.size())
        self.show()

        self.searc_data = None
        self.dialog = QtWidgets.QMessageBox()

        self.url_data = 'https://mail2.dcz.gov.ua/publikaciya/6-perelik-aktualnyh-vakansiy-stanom-na-datu'

        self.update_data_btn.clicked.connect(self.digit_pressed)    # Update Data
        self.search_btn.clicked.connect(self.digit_pressed)         # Search
        self.export_txt_btn.clicked.connect(self.digit_pressed)     # Export txt
        self.export_pdf_btn.clicked.connect(self.digit_pressed)     # Export pdf
        self.exit_btn.clicked.connect(self.digit_pressed)           # Exit
        self.tables.itemClicked.connect(self.digit_pressed)         # Table

        self.data_table.clicked.connect(lambda: self.select_data_table(self.data_table.currentIndex().row()))

        self.tables.clear()
        self.tables.addItems(listbox_columns)
        self.total_vac.setText(str(data_job.get_count_row()))

    def digit_pressed(self):
        sender = self.sender() # Получаем объект кнопки которая вызвала функцию
        if sender == self.update_data_btn: # Если нажата кнопка обновления данных
            data_job.download_data(self.url_data) # Обновляем данные
            self.total_vac.setText(str(data_job.get_count_row())) # Обновляем количество вакансий
        elif sender == self.search_btn: # Если нажата кнопка поиска
            column_number = self.tables.currentRow() # Получаем номер колонки
            search_text = self.search_string.text() # Получаем текст для поиска
            exact_search = self.exact_search.isChecked() 
            self.searc_data = data_job.search_data(
                search_text, column_number, exact_search) # Поиск данных
            self.found_vac.setText(str(len(self.searc_data))) # Обновляем количество найденных данных
        elif sender == self.export_txt_btn: # Если нажата кнопка экспорта в текстовый файл
            if self.searc_data != None: # Если данные поиска не пустые
                filename = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "Vacancies.txt") # Получаем имя файла
                data_job.export_to_txt(self.searc_data, filename[0]) # Экспорт данных в текстовый файл
                self.dialog.setText("Successfully exported to txt") # Обновляем текст в диалоговом окне
                self.dialog.setDefaultButton(self.dialog.Ok) # Устанавливаем кнопку по умолчанию
                self.dialog.exec_() # Отображаем диалоговое окно
        elif sender == self.export_pdf_btn: # Если нажата кнопка экспорта в pdf
            if self.searc_data != None: # Если данные поиска не пустые
                filename = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "Vacancies.pdf") # Получаем имя файла
                data_job.export_to_pdf(self.searc_data, filename[0]) # Экспорт данных в pdf
                self.dialog.setText("Successfully exported to pdf") # Обновляем текст в диалоговом окне
                self.dialog.setDefaultButton(self.dialog.Ok) # Устанавливаем кнопку по умолчанию
                self.dialog.exec_() # Отображаем диалоговое окно
        elif sender == self.exit_btn: # Если нажата кнопка выхода
            sys.exit() # Выход из программы
        elif sender == self.tables: # Если нажата кнопка выбора колонки
            column_number = self.tables.currentRow()
            data_colum = data_job.get_all_data_column(column_number) # Получаем данные из выбранной колонки
            data_colum = sorted(data_colum) # Сортируем данные
            sort_data_column = [el for el, _ in groupby(data_colum)] # Группируем данные 
            model = QtGui.QStandardItemModel() # Создаем модель данных
             
            for row in sort_data_column:
                model.appendRow(QtGui.QStandardItem(str(row))) # Добавляем данные в модель

            self.data_table.setModel(model) # Устанавливаем модель данных в таблицу
            self.data_table.resizeRowsToContents() # Растягиваем размер строк в таблице
            self.data_table.setColumnWidth(0, 581) # Устанавливаем ширину колонки
            self.data_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers) # Запрещаем редактирование таблицы
            self.data_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows) # Выделяем строки

    def select_data_table(self, row_id):
        #get text from table in row_id
        text = self.data_table.model().item(row_id).text()
        # get tables column number
        column_number = self.tables.currentRow()
        if column_number != 5:
            self.search_string.setText(text)

if __name__ == '__main__':
    # Новый экземпляр QApplication
    app = QtWidgets.QApplication(sys.argv)
    # Содание объекта главного окна
    aplic = App()
    # Запуск
    sys.exit(app.exec_())