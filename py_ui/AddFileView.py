# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/AddFileView.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AddFileDialog(object):
    def setupUi(self, AddFileDialog):
        AddFileDialog.setObjectName("AddFileDialog")
        AddFileDialog.resize(668, 550)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AddFileDialog.sizePolicy().hasHeightForWidth())
        AddFileDialog.setSizePolicy(sizePolicy)
        AddFileDialog.setMaximumSize(QtCore.QSize(16777215, 550))
        self.verticalLayout = QtWidgets.QVBoxLayout(AddFileDialog)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalWidget = QtWidgets.QWidget(AddFileDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalWidget.sizePolicy().hasHeightForWidth())
        self.horizontalWidget.setSizePolicy(sizePolicy)
        self.horizontalWidget.setMinimumSize(QtCore.QSize(0, 90))
        self.horizontalWidget.setObjectName("horizontalWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalWidget = QtWidgets.QWidget(self.horizontalWidget)
        self.verticalWidget.setObjectName("verticalWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalWidget1 = QtWidgets.QWidget(self.verticalWidget)
        self.horizontalWidget1.setObjectName("horizontalWidget1")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalWidget1)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(15)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.horizontalWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(60)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(60, 0))
        self.label.setMaximumSize(QtCore.QSize(60, 16777215))
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.file_name_input = QtWidgets.QLineEdit(self.horizontalWidget1)
        self.file_name_input.setMinimumSize(QtCore.QSize(0, 20))
        self.file_name_input.setMaximumSize(QtCore.QSize(16777215, 20))
        self.file_name_input.setReadOnly(True)
        self.file_name_input.setObjectName("file_name_input")
        self.horizontalLayout_3.addWidget(self.file_name_input)
        self.open_file_button = QtWidgets.QPushButton(self.horizontalWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.open_file_button.sizePolicy().hasHeightForWidth())
        self.open_file_button.setSizePolicy(sizePolicy)
        self.open_file_button.setMinimumSize(QtCore.QSize(35, 0))
        self.open_file_button.setMaximumSize(QtCore.QSize(80, 16777215))
        self.open_file_button.setObjectName("open_file_button")
        self.horizontalLayout_3.addWidget(self.open_file_button)
        self.verticalLayout_2.addWidget(self.horizontalWidget1)
        self.widget_2 = QtWidgets.QWidget(self.verticalWidget)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(15)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_2 = QtWidgets.QLabel(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(60, 0))
        self.label_2.setMaximumSize(QtCore.QSize(90, 16777215))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_6.addWidget(self.label_2)
        self.delimiter_combo_box = QtWidgets.QComboBox(self.widget_2)
        self.delimiter_combo_box.setMaximumSize(QtCore.QSize(150, 16777215))
        self.delimiter_combo_box.setObjectName("delimiter_combo_box")
        self.horizontalLayout_6.addWidget(self.delimiter_combo_box)
        self.label_3 = QtWidgets.QLabel(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(140, 0))
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_6.addWidget(self.label_3)
        self.header_row_checkbox = QtWidgets.QCheckBox(self.widget_2)
        self.header_row_checkbox.setMinimumSize(QtCore.QSize(0, 0))
        self.header_row_checkbox.setMaximumSize(QtCore.QSize(25, 16777215))
        self.header_row_checkbox.setText("")
        self.header_row_checkbox.setObjectName("header_row_checkbox")
        self.horizontalLayout_6.addWidget(self.header_row_checkbox)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.label_4 = QtWidgets.QLabel(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMaximumSize(QtCore.QSize(95, 16777215))
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_6.addWidget(self.label_4)
        self.skip_rows_input = QtWidgets.QSpinBox(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.skip_rows_input.sizePolicy().hasHeightForWidth())
        self.skip_rows_input.setSizePolicy(sizePolicy)
        self.skip_rows_input.setMaximumSize(QtCore.QSize(60, 16777215))
        self.skip_rows_input.setMinimum(0)
        self.skip_rows_input.setMaximum(999999999)
        self.skip_rows_input.setProperty("value", 0)
        self.skip_rows_input.setObjectName("skip_rows_input")
        self.horizontalLayout_6.addWidget(self.skip_rows_input)
        self.label_5 = QtWidgets.QLabel(self.widget_2)
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_6.addWidget(self.label_5)
        self.verticalLayout_2.addWidget(self.widget_2)
        self.horizontalWidget_2 = QtWidgets.QWidget(self.verticalWidget)
        self.horizontalWidget_2.setObjectName("horizontalWidget_2")
        self.custom_delimiter_input = QtWidgets.QLineEdit(self.horizontalWidget_2)
        self.custom_delimiter_input.setGeometry(QtCore.QRect(75, 2, 100, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.custom_delimiter_input.sizePolicy().hasHeightForWidth())
        self.custom_delimiter_input.setSizePolicy(sizePolicy)
        self.custom_delimiter_input.setMaximumSize(QtCore.QSize(100, 16777215))
        self.custom_delimiter_input.setObjectName("custom_delimiter_input")
        self.verticalLayout_2.addWidget(self.horizontalWidget_2)
        self.horizontalLayout.addWidget(self.verticalWidget)
        self.verticalLayout.addWidget(self.horizontalWidget)
        self.widget = QtWidgets.QWidget(AddFileDialog)
        self.widget.setObjectName("widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.text_preview_label = QtWidgets.QTextBrowser(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text_preview_label.sizePolicy().hasHeightForWidth())
        self.text_preview_label.setSizePolicy(sizePolicy)
        self.text_preview_label.setMaximumSize(QtCore.QSize(16777215, 200))
        self.text_preview_label.setObjectName("text_preview_label")
        self.verticalLayout_3.addWidget(self.text_preview_label)
        self.data_preview_table = QtWidgets.QTableWidget(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.data_preview_table.sizePolicy().hasHeightForWidth())
        self.data_preview_table.setSizePolicy(sizePolicy)
        self.data_preview_table.setMinimumSize(QtCore.QSize(200, 0))
        self.data_preview_table.setMaximumSize(QtCore.QSize(16777215, 200))
        self.data_preview_table.setObjectName("data_preview_table")
        self.data_preview_table.setColumnCount(0)
        self.data_preview_table.setRowCount(0)
        self.verticalLayout_3.addWidget(self.data_preview_table)
        self.verticalLayout.addWidget(self.widget)
        self.widget1 = QtWidgets.QWidget(AddFileDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget1.sizePolicy().hasHeightForWidth())
        self.widget1.setSizePolicy(sizePolicy)
        self.widget1.setMaximumSize(QtCore.QSize(16777215, 60))
        self.widget1.setObjectName("widget1")
        self.done_button = QtWidgets.QPushButton(self.widget1)
        self.done_button.setGeometry(QtCore.QRect(0, 15, 110, 30))
        self.done_button.setObjectName("done_button")
        self.cancel_button = QtWidgets.QPushButton(self.widget1)
        self.cancel_button.setGeometry(QtCore.QRect(110, 15, 110, 30))
        self.cancel_button.setObjectName("cancel_button")
        self.verticalLayout.addWidget(self.widget1)

        self.retranslateUi(AddFileDialog)
        QtCore.QMetaObject.connectSlotsByName(AddFileDialog)

    def retranslateUi(self, AddFileDialog):
        _translate = QtCore.QCoreApplication.translate
        AddFileDialog.setWindowTitle(_translate("AddFileDialog", "Add Data Source"))
        self.label.setText(_translate("AddFileDialog", "File:"))
        self.open_file_button.setText(_translate("AddFileDialog", "Browse"))
        self.label_2.setText(_translate("AddFileDialog", "Delimiter:"))
        self.label_3.setText(_translate("AddFileDialog", "Use first row as headers:"))
        self.label_4.setText(_translate("AddFileDialog", "Skip n rows:"))
        self.done_button.setText(_translate("AddFileDialog", "Done"))
        self.cancel_button.setText(_translate("AddFileDialog", "Cancel"))

