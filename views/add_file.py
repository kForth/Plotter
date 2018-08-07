from PyQt5 import uic

from PyQt5.QtCore import Qt, QRect, QLine
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QPixmap, QCursor
from PyQt5.QtWidgets import QFileDialog, QDialog, QWidget, QApplication, QLabel, QTableWidgetItem

from py_ui.AddFileView import Ui_AddFileDialog
from dataset import Dataset

import re

class AddFileWindow(QDialog):
    def __init__(self, data_callback, cancel_add_callback, dataset=None):
        super().__init__()
        self.setupUi = Ui_AddFileDialog.setupUi
        self.retranslateUi = lambda e: Ui_AddFileDialog.retranslateUi(self, e)
        self.setupUi(self, self)
        if dataset:
            self.dataset = dataset
        else:
            self.dataset = Dataset("", [], ",", False, 0)
        # uic.loadUi('ui/AddFileView.ui', self)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.data_callback = data_callback
        self.cancel_add_callback = cancel_add_callback

        self.open_file_button.clicked.connect(self.open_file)
        self.raw_text = ""
        self.filename = ""

        self.delimiters = [
            [',', 'Comma (,)'],
            [';', 'Semi-Colon (;)'],
            [':', 'Colon (:)'],
            ['\t', 'Tab'],
            [' ', 'Space'],
            [None, 'Any White Space'],
            [None, 'Any Non-Numeric Character'],
            [None, 'Custom']
        ]

        [self.delimiter_combo_box.addItem(d[1]) for d in self.delimiters]

        self.delimiter_combo_box.setCurrentIndex([e[0] for e in self.delimiters].index(self.dataset.delimiter))
        self.header_row_checkbox.setChecked(self.dataset.header_row)
        self.file_name_input.setText(self.dataset.filepath) 
        self.skip_rows_input.setValue(self.dataset.skip_n_rows)

        self.delimiter_combo_box.currentIndexChanged.connect(self.update_table)
        self.custom_delimiter_input.textChanged.connect(self.update_table)
        self.header_row_checkbox.clicked.connect(self.update_table)

        self.cancel_button.clicked.connect(self.cancel)
        self.done_button.clicked.connect(self.handle_done_button)

        self.show()
        self.open_file(filepath=self.dataset.filepath)

    def cancel(self, event):
        self.cancel_add_callback()
        self.close()

    def open_file(self, event=None, filepath=""):
        try:
            if filepath:
                self.filename = filepath
            else:
                self.filename = QFileDialog.getOpenFileName(None, 'Select File', '', '*.csv')[0]
            self.file_name_input.setText(self.filename)
            self.raw_text = open(self.filename).read().strip()
            self.text_preview_label.setText(self.raw_text)
            self.update_table()
            # self.repaint()
        except Exception as ex:
            print(ex)

    def update_table(self):
        self.custom_delimiter_input.setVisible(self.delimiters[self.delimiter_combo_box.currentIndex()][1] == 'Custom')
        if self.raw_text:
            data_lines = self.get_data()
            headers = []
            if self.header_row_checkbox.isChecked():
                headers = data_lines[0]
                data_lines = data_lines[1:]
            data_lines = data_lines[self.skip_rows_input.value():]
            print(data_lines)

            num_cols = max([len(e) for e in data_lines])
            self.data_preview_table.setRowCount(len(data_lines))
            self.data_preview_table.setColumnCount(num_cols)
            if headers:
                self.data_preview_table.setHorizontalHeaderLabels(headers)

            for i in range(len(data_lines)):
                for j in range(num_cols):
                    self.data_preview_table.setItem(i, j, QTableWidgetItem(str(data_lines[i][j]) if j < len(data_lines[i]) else ""))

    def handle_done_button(self):
        dataset = self.get_final_data()
        if self.filename and dataset.data and dataset.data[0]:
            if self.data_callback:
                self.data_callback(dataset)
            self.close()

    def get_data(self):
        delimiter = self.delimiters[self.delimiter_combo_box.currentIndex()][0]
        if self.delimiter_combo_box.currentIndex() < 5:
            data_lines = [e.split(delimiter) for e in self.raw_text.split("\n")]
        else:
            delimiter = self.delimiters[self.delimiter_combo_box.currentIndex()][1]
            if delimiter == 'Any White Space':
                data_lines = [re.split("\s+", e) for e in self.raw_text.split("\n")]
            elif delimiter == 'Any Non-Numeric Character':
                data_lines = [re.split("[^0-9.]+", e) for e in self.raw_text.split("\n")]
            elif delimiter == 'Custom':
                data_lines = [e for e  in self.raw_text.split("\n")]
                if self.custom_delimiter_input.text():
                    try:
                        data_lines = [re.split(self.custom_delimiter_input.text(), e) for e in self.raw_text.split("\n")]
                    except:
                        pass
        return data_lines


    def get_final_data(self):
        data = []
        delimiter = self.delimiters[self.delimiter_combo_box.currentIndex()][0]
        data_lines = self.get_data()
        if self.raw_text:
            headers = []
            if self.header_row_checkbox.isChecked():
                headers = data_lines[0]
                data_lines = data_lines[1:]
            for i in range(len(data_lines)):
                data.append([])
                for j in range(len(data_lines[i])):
                    try:
                        data[-1].append(float(data_lines[i][j]))
                    except:
                        data[-1].append(0)

        data = data[self.skip_rows_input.value():]
        if headers:
            data = [headers] + data

        Dataset.__init__(self.dataset, self.filename, data, delimiter, self.header_row_checkbox.isChecked(), self.skip_rows_input.value())
        return self.dataset


