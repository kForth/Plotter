from PyQt5 import uic

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPen, QPixmap
from PyQt5.QtWidgets import QDialog

from py_ui.DataSourceListView import Ui_DataSourcesDialog
from views.add_file import AddFileWindow

class DataSourceListDialog(QDialog):
    def __init__(self, datasets, add_func, del_func):
        super().__init__()
        self.setupUi = Ui_DataSourcesDialog.setupUi
        self.retranslateUi = lambda e: Ui_DataSourcesDialog.retranslateUi(self, e)
        self.setupUi(self, self)
        # uic.loadUi('ui/DataSourceListView.ui', self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.datasets = datasets
        self.add_func = add_func
        self.del_func = del_func

        self.add_button.clicked.connect(self.add_data_source)
        self.delete_button.clicked.connect(self.delete_data_source)
        self.edit_button.clicked.connect(self.edit_data_source)
        self.done_button.clicked.connect(self.close)

        self.last_dataset = None

        self.data_source_list.clear()
        for fp in self.datasets:
            self.data_source_list.addItem(fp)
        self.show()

    def add_data_source(self, event):
        self.add_file_window = AddFileWindow(self.add_source, lambda: 0)

    def add_source(self, filepath, data, delimiter, header_row, skip_n_rows):
        self.data_source_list.addItem(filepath)
        self.add_func(filepath, data, delimiter, header_row, skip_n_rows)

    def delete_data_source(self, event):
        if self.data_source_list.currentItem() is not None:
            self.del_func(self.datasets[self.data_source_list.currentItem().text()])
            self.data_source_list.clear()
            for fp in self.datasets:
                self.data_source_list.addItem(fp)

    def edit_data_source(self, event):
        if self.data_source_list.currentItem() is not None:
            fp = self.data_source_list.currentItem().text()
            self.data_source_to_edit = self.datasets[fp]
            self.data_source_edit_window = AddFileWindow(self.update_data, lambda: 0, fp, self.data_source_to_edit['delimiter'], self.data_source_to_edit['header_row'], self.data_source_to_edit['skip_n_rows'])
            pass

    def update_data(self, filepath, data, delimiter, header_row, skip_n_rows):
        data_source = {
            'filepath': filepath,
            'data': data,
            'delimiter': delimiter,
            'header_row': header_row
        }
        if filepath != self.data_source_to_edit['filepath']:
            del self.datasets[self.data_source_to_edit['filepath']]
            self.data_source_to_edit = self.datasets[filepath] = {}    
        self.data_source_to_edit['filepath'] = filepath
        self.data_source_to_edit['data'] = data
        self.data_source_to_edit['delimiter'] = delimiter
        self.data_source_to_edit['header_row'] = header_row
        self.data_source_to_edit['skip_n_rows'] = skip_n_rows

