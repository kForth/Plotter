# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/TextEntryDialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_EnterTextDialog(object):
    def setupUi(self, EnterTextDialog):
        EnterTextDialog.setObjectName("EnterTextDialog")
        EnterTextDialog.resize(197, 99)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(EnterTextDialog.sizePolicy().hasHeightForWidth())
        EnterTextDialog.setSizePolicy(sizePolicy)
        self.label = QtWidgets.QLabel(EnterTextDialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 180, 20))
        self.label.setObjectName("label")
        self.text_input = QtWidgets.QLineEdit(EnterTextDialog)
        self.text_input.setGeometry(QtCore.QRect(10, 30, 180, 21))
        self.text_input.setObjectName("text_input")
        self.done_button = QtWidgets.QPushButton(EnterTextDialog)
        self.done_button.setGeometry(QtCore.QRect(10, 60, 80, 32))
        self.done_button.setObjectName("done_button")
        self.cancel_button = QtWidgets.QPushButton(EnterTextDialog)
        self.cancel_button.setGeometry(QtCore.QRect(110, 60, 80, 32))
        self.cancel_button.setObjectName("cancel_button")

        self.retranslateUi(EnterTextDialog)
        QtCore.QMetaObject.connectSlotsByName(EnterTextDialog)

    def retranslateUi(self, EnterTextDialog):
        _translate = QtCore.QCoreApplication.translate
        EnterTextDialog.setWindowTitle(_translate("EnterTextDialog", "Enter Text"))
        self.label.setText(_translate("EnterTextDialog", "Enter Text:"))
        self.done_button.setText(_translate("EnterTextDialog", "Done"))
        self.cancel_button.setText(_translate("EnterTextDialog", "Cancel"))

