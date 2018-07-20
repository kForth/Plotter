from PyQt5 import uic

from PyQt5.QtCore import Qt, QRect, QLine
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QPixmap, QCursor
from PyQt5.QtWidgets import QFileDialog, QDialog, QWidget, QApplication, QLabel, QTableWidgetItem

from py_ui.AddFileView import Ui_AddFileDialog

class AddFileWindow(QDialog):
    def __init__(self, data_callback, cancel_add_callback, filepath="", delimiter=",", header_row=False, skip_n_rows=0):
        super().__init__()
        self.setupUi = Ui_AddFileDialog.setupUi
        self.retranslateUi = lambda e: Ui_AddFileDialog.retranslateUi(self, e)
        self.setupUi(self, self)
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
            [' ', 'Space']
        ]

        [self.delimiter_combo_box.addItem(d[1]) for d in self.delimiters]

        self.delimiter_combo_box.setCurrentIndex([e[0] for e in self.delimiters].index(delimiter))
        self.header_row_checkbox.setChecked(header_row)
        self.file_name_input.setText(filepath) 
        self.skip_rows_input.setValue(skip_n_rows)

        self.delimiter_combo_box.currentIndexChanged.connect(self.repaint)
        self.header_row_checkbox.clicked.connect(self.repaint)

        self.cancel_button.clicked.connect(self.cancel)
        self.done_button.clicked.connect(self.handle_done_button)

        self.show()
        self.open_file(filepath=filepath)

    def cancel():
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
            self.repaint()
        except Exception as ex:
            print(ex)

    def paintEvent(self, event):
        if self.raw_text:
            delimiter = self.delimiters[self.delimiter_combo_box.currentIndex()][0]
            data_lines = [e.split(delimiter) for e in self.raw_text.split("\n")]
            headers = []
            if self.header_row_checkbox.isChecked():
                headers = data_lines[0]
                data_lines = data_lines[1:]
            data_lines = data_lines[self.skip_rows_input.value():]

            self.data_preview_table.setRowCount(len(data_lines))
            self.data_preview_table.setColumnCount(len(data_lines[0]))
            if headers:
                self.data_preview_table.setHorizontalHeaderLabels(headers)

            for i in range(len(data_lines)):
                for j in range(len(data_lines[0])):
                    self.data_preview_table.setItem(i, j, QTableWidgetItem(str(data_lines[i][j])))

    def handle_done_button(self):
        data, delimiter, header_row, skip_n_rows = self.get_final_data()
        if self.filename and data and data[0]:
            self.data_callback(self.filename, data, delimiter, header_row, skip_n_rows)
            self.close()

    def get_final_data(self):
        data = []
        delimiter = self.delimiters[self.delimiter_combo_box.currentIndex()][0]
        data_lines = [e.split(delimiter) for e in self.raw_text.split("\n")]
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

        if headers:
            data = [headers] + data[self.skip_rows_input.value():]

        return data, delimiter, self.header_row_checkbox.isChecked(), self.skip_rows_input.value()


