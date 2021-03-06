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
        for dataset in self.datasets:
            self.data_source_list.addItem(dataset.filepath)
        self.show()

    def add_data_source(self, event):
        self.add_file_window = AddFileWindow(self.add_source, lambda: 0)

    def add_source(self, dataset):
        self.data_source_list.addItem(dataset.filepath)
        self.add_func(dataset)

    def delete_data_source(self, event):
        if self.data_source_list.currentItem() is not None:
            self.del_func(self.datasets[self.data_source_list.currentIndex()])
            self.data_source_list.clear()
            for dataset in self.datasets:
                self.data_source_list.addItem(dataset.filepath)

    def edit_data_source(self, event):
        if self.data_source_list.currentItem() is not None:
            self.data_source_edit_window = AddFileWindow(lambda: 0, lambda: 0, fp, self.datasets[self.data_source_list.currentIndex()])

    # def update_data(self, data_source):
        # if filepath != self.data_source_to_edit.filepath:
        # self.data_source_to_edit.filepath = filepath
        # self.data_source_to_edit.data = data
        # self.data_source_to_edit.delimiter = delimiter
        # self.data_source_to_edit.header_row = header_row
        # self.data_source_to_edit.skip_n_rows = skip_n_rows

