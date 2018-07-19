from PyQt5 import uic

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPen, QPixmap
from PyQt5.QtWidgets import QDialog

class TextEntryDialog(QDialog):
    textChanged = pyqtSignal(str)
    textSelected = pyqtSignal(str)
    textCanceled = pyqtSignal(str)

    def __init__(self, label_text, text="", window_title="Enter Text"):
        super().__init__()
        uic.loadUi('ui/TextEntryDialog.ui', self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.setWindowTitle(window_title)

        self.label.setText(label_text)
        self.text_input.setText(text)

        self.text_input.textChanged.connect(self.text_changed)

        self.done_button.clicked.connect(self.handle_done_button)
        self.cancel_button.clicked.connect(self.cancel)

    def text_changed(self, event):
        self.textChanged.emit(self.text_input.text())

    def cancel(self):
        textCanceled.emit(self.text_input.text())

    def open(self):
        self.show()

    def handle_done_button(self):
        self.textSelected.emit(self.text_input.text())
        self.close()