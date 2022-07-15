# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(887, 319)
        self.tables = QListWidget(Dialog)
        self.tables.setObjectName(u"tables")
        self.tables.setGeometry(QRect(10, 30, 101, 281))
        self.tables.setMaximumSize(QSize(18888, 18888))
        self.search_btn = QPushButton(Dialog)
        self.search_btn.setObjectName(u"search_btn")
        self.search_btn.setGeometry(QRect(710, 140, 171, 28))
        self.search_string = QLineEdit(Dialog)
        self.search_string.setObjectName(u"search_string")
        self.search_string.setGeometry(QRect(710, 90, 171, 28))
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(710, 170, 101, 16))
        self.export_pdf_btn = QPushButton(Dialog)
        self.export_pdf_btn.setObjectName(u"export_pdf_btn")
        self.export_pdf_btn.setGeometry(QRect(710, 240, 171, 28))
        self.found_vac = QLabel(Dialog)
        self.found_vac.setObjectName(u"found_vac")
        self.found_vac.setGeometry(QRect(810, 170, 71, 16))
        self.export_txt_btn = QPushButton(Dialog)
        self.export_txt_btn.setObjectName(u"export_txt_btn")
        self.export_txt_btn.setGeometry(QRect(710, 210, 171, 28))
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 10, 121, 16))
        self.update_data_btn = QPushButton(Dialog)
        self.update_data_btn.setObjectName(u"update_data_btn")
        self.update_data_btn.setGeometry(QRect(710, 30, 171, 28))
        self.total_vac = QLabel(Dialog)
        self.total_vac.setObjectName(u"total_vac")
        self.total_vac.setGeometry(QRect(810, 60, 71, 16))
        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(710, 60, 91, 16))
        self.exit_btn = QPushButton(Dialog)
        self.exit_btn.setObjectName(u"exit_btn")
        self.exit_btn.setGeometry(QRect(710, 280, 171, 28))
        self.exact_search = QCheckBox(Dialog)
        self.exact_search.setObjectName(u"exact_search")
        self.exact_search.setGeometry(QRect(710, 120, 121, 21))
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(350, 10, 131, 20))
        self.data_table = QTableView(Dialog)
        self.data_table.setObjectName(u"data_table")
        self.data_table.setGeometry(QRect(120, 30, 581, 281))
        self.data_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.data_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.data_table.setAlternatingRowColors(False)
        self.data_table.setVerticalScrollMode(QAbstractItemView.ScrollPerItem)
        self.data_table.setWordWrap(True)
        self.data_table.setCornerButtonEnabled(True)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.search_btn.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.search_string.setInputMask("")
        self.search_string.setPlaceholderText(QCoreApplication.translate("Dialog", u"Search String", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Vacancies found:", None))
        self.export_pdf_btn.setText(QCoreApplication.translate("Dialog", u"Export to PDF", None))
        self.found_vac.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.export_txt_btn.setText(QCoreApplication.translate("Dialog", u"Export to TXT", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Select a table", None))
        self.update_data_btn.setText(QCoreApplication.translate("Dialog", u"Update Data", None))
        self.total_vac.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Total vacancies:", None))
        self.exit_btn.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.exact_search.setText(QCoreApplication.translate("Dialog", u"Exact Search", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Available data in table", None))
    # retranslateUi

