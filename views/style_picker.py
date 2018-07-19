from PyQt5 import uic

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPen, QPixmap
from PyQt5.QtWidgets import QDialog

from py_ui.StyleSelectDialog import Ui_SelectStyleDialog

class StyleSelectDialog(QDialog):
    styleSelected = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()
        self.setupUi = Ui_SelectStyleDialog.setupUi
        self.retranslateUi = lambda e: Ui_SelectStyleDialog.retranslateUi(self, e)
        self.setupUi(self, self)
        # uic.loadUi('ui/StyleSelectDialog.ui', self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.done_button.clicked.connect(self.handle_done_button)
        self.cancel_button.clicked.connect(self.close)

        self.styles = [
            ['SolidLine', Qt.SolidLine],
            ['DashLine', Qt.DashLine],
            ['DotLine', Qt.DotLine],
            ['DashDotLine', Qt.DashDotLine],
            ['DashDotDotLine', Qt.DashDotDotLine],
            ['CustomDashLine', Qt.CustomDashLine]
        ]

        for style in self.styles:
            self.style_combo_box.addItem(style[0])

        self.style_combo_box.currentIndexChanged.connect(self.update_style)
        self.max_height = self.height()

        self.update_style()

    def open(self):
        self.show()

    def handle_done_button(self):
        if self.style_combo_box.currentIndex() == 5:
            self.styleSelected.emit((self.styles[self.style_combo_box.currentIndex()][1], self.get_custom_pattern()))
        else:
            self.styleSelected.emit((self.styles[self.style_combo_box.currentIndex()][1], []))
        self.close()

    def update_style(self):
        if self.style_combo_box.currentIndex() == 5:
            self.custom_pattern_widget.setVisible(True)
            self.setFixedSize(self.width(), self.max_height)
        else:
            self.custom_pattern_widget.setVisible(False)
            self.setFixedSize(self.width(), self.max_height - 34)
        self.repaint()


    def get_custom_pattern(self):
        pattern = []
        text = self.custom_pattern_input.text().strip().split(",")
        for val in text:
            try:
                pattern.append(int(val))
            except:
                pattern.append(0)
        return pattern


    def paintEvent(self, event):
        pixmap = QPixmap(self.line_preview_label.size())
        pixmap.fill(QColor(0, 0, 0, 0))
        qp = QPainter()
        qp.begin(pixmap)
        pen = QPen()
        pen.setWidth(5)
        pen.setStyle(self.styles[self.style_combo_box.currentIndex()][1])
        if self.style_combo_box.currentIndex() == 5:
            pattern = self.get_custom_pattern()
            if len(pattern) % 2 == 1:
                pattern = pattern[:-1]
            pen.setDashPattern(pattern)
        qp.setPen(pen)
        qp.drawLine(0, self.line_preview_label.height()/2, self.line_preview_label.width()-1, self.line_preview_label.height()/2)
        qp.end()
        self.line_preview_label.setPixmap(pixmap)