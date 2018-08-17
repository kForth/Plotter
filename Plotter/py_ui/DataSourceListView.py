# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/DataSourceListView.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DataSourcesDialog(object):
    def setupUi(self, DataSourcesDialog):
        DataSourcesDialog.setObjectName("DataSourcesDialog")
        DataSourcesDialog.resize(330, 360)
        self.done_button = QtWidgets.QPushButton(DataSourcesDialog)
        self.done_button.setGeometry(QtCore.QRect(250, 320, 70, 32))
        self.done_button.setObjectName("done_button")
        self.data_source_list = QtWidgets.QListWidget(DataSourcesDialog)
        self.data_source_list.setGeometry(QtCore.QRect(10, 30, 310, 280))
        self.data_source_list.setObjectName("data_source_list")
        self.add_button = QtWidgets.QPushButton(DataSourcesDialog)
        self.add_button.setGeometry(QtCore.QRect(10, 320, 70, 32))
        self.add_button.setObjectName("add_button")
        self.delete_button = QtWidgets.QPushButton(DataSourcesDialog)
        self.delete_button.setGeometry(QtCore.QRect(90, 320, 70, 32))
        self.delete_button.setObjectName("delete_button")
        self.edit_button = QtWidgets.QPushButton(DataSourcesDialog)
        self.edit_button.setGeometry(QtCore.QRect(170, 320, 70, 32))
        self.edit_button.setObjectName("edit_button")
        self.label = QtWidgets.QLabel(DataSourcesDialog)
        self.label.setGeometry(QtCore.QRect(10, 0, 310, 30))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label.setObjectName("label")

        self.retranslateUi(DataSourcesDialog)
        QtCore.QMetaObject.connectSlotsByName(DataSourcesDialog)

    def retranslateUi(self, DataSourcesDialog):
        _translate = QtCore.QCoreApplication.translate
        DataSourcesDialog.setWindowTitle(_translate("DataSourcesDialog", "Data Sources"))
        self.done_button.setText(_translate("DataSourcesDialog", "Done"))
        self.add_button.setText(_translate("DataSourcesDialog", "Add"))
        self.delete_button.setText(_translate("DataSourcesDialog", "Delete"))
        self.edit_button.setText(_translate("DataSourcesDialog", "Edit"))
        self.label.setText(_translate("DataSourcesDialog", "Data Sources:"))

