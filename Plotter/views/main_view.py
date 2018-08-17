from PyQt5 import uic

from PyQt5.QtCore import Qt, QRect, QLine, QFile, QIODevice, QSize
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QPixmap, QCursor, QFontDatabase
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QWidget, QApplication, QLabel, QColorDialog, QPushButton, QRadioButton

from collections import OrderedDict

from py_ui.MainView import Ui_PlotterMainWindow
from views.add_file import AddFileWindow
from views.chart import ChartWidget
from views.style_picker import StyleSelectDialog
from views.text_entry_dialog import TextEntryDialog
from views.data_source_list_view import DataSourceListDialog
from dataset import Dataset
from line import Line, PointShape

from time import time


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi = Ui_PlotterMainWindow.setupUi
        self.retranslateUi = lambda e: Ui_PlotterMainWindow.retranslateUi(self, e)
        self.setupUi(self, self)
        # uic.loadUi('ui/MainView.ui', self)
        self.fontDB = QFontDatabase()
        self.fontDB.addApplicationFont("OpenSansEmoji.ttf")

        self.chart = ChartWidget(self.chart_label, self.home_button, self.zoom_button, self.update_chart)
        self.legend = QLabel(self.legend_widget)
        self.screenshot_button.clicked.connect(self.handle_screenshot_button)

        self.add_dataset_button = self.add_dataset_button_3
        self.line_combo_box = self.line_combo_box_3
        self.add_dataset_button.clicked.connect(self.open_data_file)
        self.edit_datasets_button.clicked.connect(self.open_edit_dataset)
        self.add_file_action.triggered.connect(self.open_data_file)
        self.add_page_action.triggered.connect(self.add_page)
        self.edit_page_name_action.triggered.connect(self.edit_page_name)
        self.delete_current_page_action.triggered.connect(self.delete_page)

        # self.add_page_button.setPosition(
        self.datasets = []
        self.pages = []
        self.page = {}
        self.add_page()

        self.add_page_button.clicked.connect(self.add_page)
        self.add_line_button.clicked.connect(self.handle_add_line_button)
        self.add_line_button_2.clicked.connect(self.handle_add_line_button)
        self.edit_lines_button.clicked.connect(self.toggle_edit_lines)

        self.line_combo_box.currentIndexChanged.connect(self.set_line_to_edit_from_combo_box)
        self.dataset_combo_box.currentIndexChanged.connect(self.update_data_set)
        self.name_input.textChanged.connect(self.update_edited_line_data)
        self.sort_by_x_checkbox.clicked.connect(self.update_edited_line_data)
        self.x_key_combo_box.currentIndexChanged.connect(self.update_edited_line_data)
        self.y_key_combo_box.currentIndexChanged.connect(self.update_edited_line_data)
        self.display_line_checkbox.clicked.connect(self.update_edited_line_pixmap)
        self.line_width_slider.valueChanged.connect(self.update_edited_line_pixmap)
        self.line_opacity_slider.valueChanged.connect(self.update_edited_line_pixmap)
        self.display_point_checkbox.clicked.connect(self.update_edited_line_pixmap)
        self.point_size_slider.valueChanged.connect(self.update_edited_line_pixmap)
        self.point_opacity_slider.valueChanged.connect(self.update_edited_line_pixmap)
        self.point_shape_combobox.currentIndexChanged.connect(self.update_edited_line_pixmap)
        for e in list(PointShape):
            self.point_shape_combobox.addItem(e.name.title())
        self.point_shape_combobox.setCurrentIndex(0)

        self.line_colour_label.mousePressEvent = lambda _: self.open_colour_dialog(self.update_line_colour)
        self.line_pattern_label.mousePressEvent = self.open_style_dialog
        self.point_colour_label.mousePressEvent = lambda _: self.open_colour_dialog(self.update_point_colour)

        self.line_settings_widget.setVisible(False)
        self.line_to_edit = None
        self.remove_line_button.clicked.connect(self.handle_remove_line_button)

        self.line_count_label.setText('{} Line{}'.format(len(self.page['lines']), "s" if len(self.page['lines']) != 1 else ""))
        self.dataset_count_label.setText('{} Dataset{}'.format(len(self.datasets), "s" if len(self.datasets) != 1 else ""))

        self.show()

        self.legend.setFixedSize(self.legend_widget.size())
        self.chart.fit_data()

    def open_edit_dataset(self, event):
        self.dataset_edit_dialog = DataSourceListDialog(self.datasets, self.add_data_source, self.delete_data_source)

    def edit_page_name(self, event):
        self.text_entry_dialog = TextEntryDialog('Enter Page Name:', text=self.page['name'], window_title="Edit Page Name")
        self.text_entry_dialog.textSelected.connect(self.update_page_name)
        self.text_entry_dialog.open()

    def update_page_name(self, new_name):
        self.page['name'] = new_name
        self.page['button'].setText(new_name)

    def delete_page(self, event, page=None):
        if page is None:
            page = self.page
        self.pages.remove(page)
        try:
            self.tab_widget.layout().removeWidget(page['button'])
        except:
            pass
        page['button'].hide()
        del page['button']
        if self.pages:
            self.select_page(self.pages[0]['id'])
        else:
            self.add_page()

    def add_page(self):
        self.line_to_edit = None
        page_button = QPushButton()
        page_button.setCheckable(True)
        page_button.setStyleSheet(self.add_page_button.styleSheet() + "\nQPushButton:checked{\nbackground: #ddd;\n}")
        self.tab_widget.layout().addWidget(page_button)
        page_button.setChecked(False)

        new_id = 'page_1'
        while new_id in [p['id'] for p in self.pages]:
            new_id = 'page_' + str(int(new_id[5:]) + 1)

        page = {
            'id': new_id,
            'name': new_id.replace("_", " ").title(),
            'lines': [],
            'button': page_button
        }

        page_button.clicked.connect(lambda: self.select_page(new_id))
        page_button.setText(page['name'])
        page_button.setMinimumSize(QSize(60, 30))

        self.pages.append(page)
        self.select_page(new_id)

    def select_page(self, page_id):
        if self.page:
            self.page['button'].setChecked(False)
        page_ids = [e['id'] for e in self.pages]
        if page_id in page_ids:
            self.line_to_edit = None
            self.line_settings_widget.setVisible(False)
            self.legend.setVisible(True)

            page = self.pages[page_ids.index(page_id)]
            if self.page is page:
                return
            self.page = page
            self.page['button'].setChecked(True)
            
            self.line_combo_box.clear()
            [self.line_combo_box.addItem(l.name) for l in self.page['lines']]

            if not self.page['lines'] and self.datasets:
                self.handle_add_line_button()
            else:
                self.line_combo_box.setCurrentIndex(0)

            self.update_chart()

    def toggle_edit_lines(self, event):
        if self.line_to_edit is None and self.datasets:
            if self.page['lines']:
                self.line_combo_box.setCurrentIndex(0)
            else:
                self.handle_add_line_button()
            self.line_settings_widget.setVisible(True)
            self.legend.setVisible(False)
        else:
            self.line_to_edit = None
            self.line_settings_widget.setVisible(False)
            self.legend.setVisible(True)

    def handle_screenshot_button(self, event):
        pixmap = self.chart_label.pixmap()
        if pixmap:
            filename = QFileDialog.getSaveFileName(None, 'Save Screenshot', '', '*.png')[0]
            file = QFile(filename);
            file.open(QIODevice.WriteOnly);
            pixmap.save(file, "PNG");

    def open_style_dialog(self, event):
        self.style_dialog = StyleSelectDialog()
        self.style_dialog.styleSelected.connect(self.update_line_style)
        self.style_dialog.open()

    def open_colour_dialog(self, target):
        self.colour_dialog = QColorDialog()
        self.colour_dialog.colorSelected.connect(target)
        self.colour_dialog.open()

    def set_line_to_edit_from_combo_box(self):
        if self.page['lines']:
            self.line_to_edit = self.page['lines'][self.line_combo_box.currentIndex()]
            self.name_input.setText(self.line_to_edit.name)
            self.dataset_combo_box.setCurrentIndex(self.datasets.index(self.line_to_edit.dataset))
            self.x_key_combo_box.setCurrentIndex(self.line_to_edit.x_key)
            self.y_key_combo_box.setCurrentIndex(self.line_to_edit.y_key)
            self.sort_by_x_checkbox.setChecked(self.line_to_edit.sort_by_x)
            self.display_line_checkbox.setChecked(self.line_to_edit.display_line)
            self.dataset_combo_box.setCurrentIndex(self.datasets.index(self.line_to_edit.dataset))
            self.line_width_slider.setValue(int(self.line_to_edit.line_width * 10))
            self.draw_line_label_colour(self.line_to_edit.line_colour)
            self.draw_line_label_pattern(self.line_to_edit.line_style)
            self.draw_point_label_colour(self.line_to_edit.point_colour)
            self.point_shape_combobox.setCurrentIndex(self.line_to_edit.point_shape.value)

            if self.datasets:
                self.line_settings_widget.setVisible(True)
                self.legend.setVisible(False)
            else:
                self.line_settings_widget.setVisible(False)
                self.legend.setVisible(True)

    def open_data_file(self):
        self.add_file_window = AddFileWindow(self.add_data_source, lambda: 0)

    def add_data_source(self, dataset):
        self.datasets.append(dataset)
        self.dataset_combo_box.addItem(dataset.filepath.split("/")[-1])

        self.dataset_count_label.setText('{} Dataset{}'.format(len(self.datasets), "s" if len(self.datasets) != 1 else ""))
        self.update_data_set()
        if not self.page['lines']:
            self.handle_add_line_button()

    def delete_data_source(self, data_source):
        for page in self.pages:
            for line in page['lines']:
                if line['dataset'] is data_source:
                    if line is self.line_to_edit:
                        self.handle_remove_line_button(None)
                    else:
                        page['lines'].remove(line)
        self.datasets.remove(data_source)
        self.dataset_combo_box.clear()
        [self.dataset_combo_box.addItem(d.filepath) for d in self.datasets]
        self.dataset_count_label.setText('{} Dataset{}'.format(len(self.datasets), "s" if len(self.datasets) != 1 else ""))
        self.update_data_set()
        self.update_chart(False)


    def handle_add_line_button(self):
        if self.datasets:
            default_name = 'Line 1'
            while default_name in [e.name for e in self.page['lines']]:
                default_name = 'Line ' + str(int(default_name.split(' ')[-1]) + 1)
            line = Line(default_name, self.datasets[0])
            self.page['lines'].append(line)
            self.line_combo_box.addItem(line.name)
            self.line_combo_box.setCurrentIndex(len(self.page['lines'])-1)
            self.set_line_to_edit_from_combo_box()

            self.line_count_label.setText('{} Line{}'.format(len(self.page['lines']), "s" if len(self.page['lines']) != 1 else ""))
            self.update_data_set()
            self.chart.paint_lines(self.page['lines'], update_axis=False)
            self.chart.fit_data()

    def handle_remove_line_button(self, event):
        self.page['lines'].remove(self.line_to_edit)
        self.line_to_edit = None
        self.line_combo_box.clear()
        if len(self.page['lines']) < 1:
            self.line_settings_widget.setVisible(False)
            self.legend.setVisible(True)
        else:
            [self.line_combo_box.addItem(e.name) for e in self.page['lines']]
            self.line_combo_box.setCurrentIndex(0)

        self.line_count_label.setText('{} Line{}'.format(len(self.page['lines']), "s" if len(self.page['lines']) != 1 else ""))
        self.update_chart(False)

    def draw_line_label_colour(self, colour):
        pixmap = QPixmap(self.line_colour_label.size())
        pixmap.fill(colour)
        self.line_colour_label.setPixmap(pixmap)
        self.line_to_edit.set_pixmap_to_update()

    def draw_point_label_colour(self, colour):
        pixmap = QPixmap(self.point_colour_label.size())
        pixmap.fill(colour)
        self.point_colour_label.setPixmap(pixmap)
        self.line_to_edit.set_pixmap_to_update()

    def draw_line_label_pattern(self, style, pattern=[]):
        pixmap = QPixmap(self.line_pattern_label.size())
        pixmap.fill(QColor(0, 0, 0, 0))
        qp = QPainter()
        qp.begin(pixmap)
        pen = QPen()
        pen.setColor(QColor(50, 50, 50))
        pen.setWidth(4)
        pen.setStyle(style)
        if pattern and style is Qt.CustomDashLine:
            pen.setDashPattern(pattern)
        qp.setPen(pen)
        qp.drawLine(0, pixmap.height()/2, pixmap.width(), pixmap.height()/2)
        qp.end()
        self.line_pattern_label.setPixmap(pixmap)
        self.line_to_edit.set_pixmap_to_update()

    def update_edited_line_data(self):
        if self.line_to_edit:
            self.line_to_edit.name = self.name_input.text()
            self.line_combo_box.setItemText(self.line_combo_box.currentIndex(), self.line_to_edit.name)
            self.line_to_edit.sort_by_x = self.sort_by_x_checkbox.isChecked()
            self.line_to_edit.x_key = self.x_key_combo_box.currentIndex()
            self.line_to_edit.y_key = self.y_key_combo_box.currentIndex()
            self.line_to_edit.set_data_to_update()
            self.update_edited_line_pixmap()
            self.update_chart(False)

    def update_edited_line_pixmap(self):
        if self.line_to_edit:
            self.line_to_edit.name = self.name_input.text()
            self.line_to_edit.display_line = self.display_line_checkbox.isChecked()
            self.line_to_edit.line_width = self.line_width_slider.value() / 10
            self.line_to_edit.line_colour.setAlpha(self.line_opacity_slider.value())
            self.line_to_edit.display_points = self.display_point_checkbox.isChecked()
            self.line_to_edit.point_size = self.point_size_slider.value()
            self.line_to_edit.point_colour.setAlpha(self.point_opacity_slider.value())
            self.line_to_edit.point_shape = PointShape.from_val(self.point_shape_combobox.currentIndex())
            self.line_to_edit.set_pixmap_to_update()
            self.update_chart(False)

    def update_line_colour(self, colour):
        if self.line_to_edit:
            self.line_to_edit.line_colour = colour
            self.line_to_edit.line_colour.setAlpha(self.line_opacity_slider.value())
            self.draw_line_label_colour(colour)
            self.update_chart(False)

    def update_point_colour(self, colour):
        if self.line_to_edit:
            self.line_to_edit.point_colour = colour
            self.line_to_edit.point_colour.setAlpha(self.point_opacity_slider.value())
            self.line_to_edit.set_all_to_update()
            self.draw_point_label_colour(colour)
            self.update_chart(False)

    def update_line_style(self, result):
        if self.line_to_edit:
            self.line_to_edit.line_style = result[0]
            self.line_to_edit.line_pattern = result[1]
            self.line_to_edit.set_all_to_update()
            self.draw_line_label_pattern(*result)
            self.update_chart(False)

    def update_data_set(self):
        if self.line_to_edit is not None:
            dataset = self.datasets[self.dataset_combo_box.currentIndex()]
            # dataset = self.line_to_edit.dataset
            if dataset.header_row:
                keys = dataset.data[0]
            else:
                keys = map(str, range(len(dataset.data[0])))
            self.x_key_combo_box.clear()
            self.y_key_combo_box.clear()
            self.x_key_combo_box.addItem('Row Number')
            self.y_key_combo_box.addItem('Row Number')
            for key in keys:
                self.x_key_combo_box.addItem(key)
                self.y_key_combo_box.addItem(key)

            if self.line_to_edit is not None:
                self.line_to_edit.dataset = dataset
                self.line_to_edit.x_key = 0
                self.line_to_edit.y_key = 1
                self.x_key_combo_box.setCurrentIndex(0)
                self.y_key_combo_box.setCurrentIndex(1)

            self.line_to_edit.dataset = dataset
            self.line_to_edit.x_key = self.x_key_combo_box.currentIndex()
            self.line_to_edit.y_key = self.y_key_combo_box.currentIndex()
            self.line_to_edit.set_all_to_update()
            self.update_chart(False)

    def paintEvent(self, event):
        pass

    def update_chart(self, update_axis=True, update_lines=True):
        pixmap = QPixmap(self.legend.size())
        pixmap.fill(QColor(0, 0, 0, 0))
        qp = QPainter()
        qp.begin(pixmap)

        y_spacing = 30
        legend_pen = QPen()
        qp.setPen(legend_pen)
        for i in range(len(self.page['lines'])):
            line = self.page['lines'][i]
            qp.setPen(legend_pen)
            qp.drawText(QRect(10, 12 + i * y_spacing, 120, 20), Qt.AlignLeft, line.name);
            line_pen = QPen()
            line_pen.setWidth(4)
            line_pen.setColor(line.line_colour)
            line_pen.setStyle(line.line_style)
            if line.line_pattern and line.line_style is Qt.CustomDashLine:
                line_pen.setDashPattern(line.line_pattern)
            qp.setPen(line_pen)
            qp.drawLine(140, 10 + i * y_spacing + 10, 190, 10 + i * y_spacing + 10)
        qp.end()
        self.legend.setPixmap(pixmap)

        if self.page['lines'] and self.datasets:
            self.chart.paint_lines(self.page['lines'], update_lines, update_axis)
            