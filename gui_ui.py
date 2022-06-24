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
        Dialog.resize(400, 320)
        self.listWidget = QListWidget(Dialog)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(10, 30, 200, 281))
        self.listWidget.setMaximumSize(QSize(18888, 18888))
        self.search_btn = QPushButton(Dialog)
        self.search_btn.setObjectName(u"search_btn")
        self.search_btn.setGeometry(QRect(220, 150, 171, 28))
        self.search_string = QLineEdit(Dialog)
        self.search_string.setObjectName(u"search_string")
        self.search_string.setGeometry(QRect(220, 100, 171, 28))
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(220, 180, 101, 16))
        self.export_pdf_btn = QPushButton(Dialog)
        self.export_pdf_btn.setObjectName(u"export_pdf_btn")
        self.export_pdf_btn.setGeometry(QRect(220, 240, 171, 28))
        self.found_vac = QLabel(Dialog)
        self.found_vac.setObjectName(u"found_vac")
        self.found_vac.setGeometry(QRect(320, 180, 71, 16))
        self.export_txt_btn = QPushButton(Dialog)
        self.export_txt_btn.setObjectName(u"export_txt_btn")
        self.export_txt_btn.setGeometry(QRect(220, 210, 171, 28))
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 10, 161, 16))
        self.update_data_btn = QPushButton(Dialog)
        self.update_data_btn.setObjectName(u"update_data_btn")
        self.update_data_btn.setGeometry(QRect(220, 30, 171, 28))
        self.total_vac = QLabel(Dialog)
        self.total_vac.setObjectName(u"total_vac")
        self.total_vac.setGeometry(QRect(320, 60, 71, 16))
        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(220, 60, 91, 16))
        self.exit_btn = QPushButton(Dialog)
        self.exit_btn.setObjectName(u"exit_btn")
        self.exit_btn.setGeometry(QRect(220, 280, 171, 28))
        self.exact_search = QCheckBox(Dialog)
        self.exact_search.setObjectName(u"exact_search")
        self.exact_search.setGeometry(QRect(220, 130, 121, 21))

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
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Table in which to search", None))
        self.update_data_btn.setText(QCoreApplication.translate("Dialog", u"Update Data", None))
        self.total_vac.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Total vacancies:", None))
        self.exit_btn.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.exact_search.setText(QCoreApplication.translate("Dialog", u"Exact Search", None))
    # retranslateUi

