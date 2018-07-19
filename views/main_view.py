from PyQt5 import uic

from PyQt5.QtCore import Qt, QRect, QLine, QFile, QIODevice, QSize
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QPixmap, QCursor, QFontDatabase
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QWidget, QApplication, QLabel, QColorDialog, QPushButton, QRadioButton

import numpy as np

from collections import OrderedDict

from views.add_file import AddFileWindow
from views.chart import ChartWidget
from views.style_picker import StyleSelectDialog
from views.text_entry_dialog import TextEntryDialog
from views.data_source_list_view import DataSourceListDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/MainView.ui', self)
        self.fontDB = QFontDatabase()
        self.fontDB.addApplicationFont("OpenSansEmoji.ttf")

        self.chart = ChartWidget(self.chart_label, self.home_button, self.zoom_button)
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
        self.datasets = OrderedDict()
        self.pages = []
        self.page = {}
        self.add_page()

        self.add_page_button.clicked.connect(self.add_page)
        self.add_line_button.clicked.connect(self.handle_add_line_button)
        self.add_line_button_2.clicked.connect(self.handle_add_line_button)
        self.edit_lines_button.clicked.connect(self.toggle_edit_lines)

        self.line_combo_box.currentIndexChanged.connect(self.set_line_to_edit_from_combo_box)
        self.dataset_combo_box.currentIndexChanged.connect(self.update_data_set)
        self.name_input.textChanged.connect(self.update_edited_line)
        self.sort_by_x_checkbox.clicked.connect(self.update_edited_line)
        self.x_key_combo_box.currentIndexChanged.connect(self.update_edited_line)
        self.y_key_combo_box.currentIndexChanged.connect(self.update_edited_line)
        self.display_line_checkbox.clicked.connect(self.update_edited_line)
        self.line_width_slider.valueChanged.connect(self.update_edited_line)
        self.line_opacity_slider.valueChanged.connect(self.update_edited_line)

        self.line_colour_label.mousePressEvent = self.open_colour_dialog
        self.line_pattern_label.mousePressEvent = self.open_style_dialog

        self.line_settings_widget.setVisible(False)
        self.line_to_edit = None
        self.remove_line_button.clicked.connect(self.handle_remove_line_button)


        self.show()
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
            [self.line_combo_box.addItem(l['name']) for l in self.page['lines']]
            self.repaint()
            if not self.page['lines'] and self.datasets:
                self.handle_add_line_button()
            else:
                self.line_combo_box.setCurrentIndex(0)

            self.repaint()

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

    def open_colour_dialog(self, event):
        self.colour_dialog = QColorDialog()
        self.colour_dialog.colorSelected.connect(self.update_line_colour)
        self.colour_dialog.open()

    def set_line_to_edit_from_combo_box(self):
        if self.page['lines']:
            self.line_to_edit = self.page['lines'][self.line_combo_box.currentIndex()]
            self.name_input.setText(self.line_to_edit['name'])
            self.dataset_combo_box.setCurrentIndex(list(self.datasets.keys()).index(self.line_to_edit['dataset']['filepath']))
            self.x_key_combo_box.setCurrentIndex(self.line_to_edit['x_key'])
            self.y_key_combo_box.setCurrentIndex(self.line_to_edit['y_key'])
            self.sort_by_x_checkbox.setChecked(self.line_to_edit['sort_by_x'])
            self.display_line_checkbox.setChecked(self.line_to_edit['display'])
            self.dataset_combo_box.setCurrentIndex(list(self.datasets.keys()).index(self.line_to_edit['dataset']['filepath']))
            self.line_width_slider.setValue(int(self.line_to_edit['line_width'] * 10))
            self.draw_line_label_colour(self.line_to_edit['colour'])
            self.draw_line_label_pattern(self.line_to_edit['style'])

            if self.datasets:
                self.line_settings_widget.setVisible(True)
                self.legend.setVisible(False)
            else:
                self.line_settings_widget.setVisible(False)
                self.legend.setVisible(True)

    def open_data_file(self):
        self.add_file_window = AddFileWindow(self.add_data_source, lambda: 0)

    def add_data_source(self, filepath, data, delimiter, header_row, skip_n_rows):
        self.datasets[filepath] = {
            'filepath': filepath,
            'data': data,
            'delimiter': delimiter,
            'header_row': header_row,
            'skip_n_rows': skip_n_rows
        }
        self.dataset_combo_box.addItem(filepath.split("/")[-1])

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
        del self.datasets[data_source['filepath']]
        self.dataset_combo_box.clear()
        [self.dataset_combo_box.addItem(d) for d in self.datasets]
        self.update_data_set()
        self.repaint()


    def handle_add_line_button(self):
        if self.datasets:
            default_name = 'Line 1'
            while default_name in [e['name'] for e in self.page['lines']]:
                default_name = 'Line ' + str(int(default_name.split(' ')[-1]) + 1)
            self.page['lines'].append({
                'name': default_name,
                'dataset': self.datasets[list(self.datasets.keys())[0]],
                'colour': QColor(50, 50, 250, 255),
                'style': Qt.SolidLine,
                'pattern': [],
                'display': True,
                'line_width': 1.5,
                'x_key': 0,
                'y_key': 1,
                'sort_by_x': False
            })
            self.line_combo_box.addItem(self.page['lines'][-1]['name'])
            self.line_combo_box.setCurrentIndex(len(self.page['lines'])-1)
            self.set_line_to_edit_from_combo_box()

            self.update_data_set()
            self.chart.paint_lines(self.page['lines'])
            self.chart.fit_data()

    def handle_remove_line_button(self, event):
        self.page['lines'].remove(self.line_to_edit)
        self.line_to_edit = None
        self.line_combo_box.clear()
        if len(self.page['lines']) < 1:
            self.line_settings_widget.setVisible(False)
            self.legend.setVisible(True)
        else:
            [self.line_combo_box.addItem(e['name']) for e in self.page['lines']]
            self.line_combo_box.setCurrentIndex(0)
        self.repaint()

    def draw_line_label_colour(self, colour):
        pixmap = QPixmap(self.line_colour_label.size())
        pixmap.fill(colour)
        self.line_colour_label.setPixmap(pixmap)

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

    def update_edited_line(self):
        if self.line_to_edit:
            self.line_to_edit['name'] = self.name_input.text()
            self.line_combo_box.setItemText(self.line_combo_box.currentIndex(), self.line_to_edit['name'])
            self.line_to_edit['line_width'] = self.line_width_slider.value() / 10
            self.line_to_edit['display'] = self.display_line_checkbox.isChecked()
            self.line_to_edit['sort_by_x'] = self.sort_by_x_checkbox.isChecked()
            self.line_to_edit['x_key'] = self.x_key_combo_box.currentIndex()
            self.line_to_edit['y_key'] = self.y_key_combo_box.currentIndex()
            self.line_to_edit['colour'].setAlpha(self.line_opacity_slider.value())
            self.repaint()

    def update_line_colour(self, colour):
        if self.line_to_edit:
            self.line_to_edit['colour'] = colour
            self.line_to_edit['colour'].setAlpha(self.line_opacity_slider.value())
            self.draw_line_label_colour(colour)
            self.repaint()

    def update_line_style(self, result):
        if self.line_to_edit:
            self.line_to_edit['style'] = result[0]
            self.line_to_edit['pattern'] = result[1]
            self.draw_line_label_pattern(*result)
            self.repaint()

    def update_data_set(self):
        if self.line_to_edit is not None:
            dataset = self.line_to_edit['dataset']
            if dataset['header_row']:
                keys = dataset['data'][0]
            else:
                keys = map(str, range(len(dataset['data'][0])))
            self.x_key_combo_box.clear()
            self.y_key_combo_box.clear()
            self.x_key_combo_box.addItem('Row Number')
            self.y_key_combo_box.addItem('Row Number')
            for key in keys:
                self.x_key_combo_box.addItem(key)
                self.y_key_combo_box.addItem(key)

            if self.line_to_edit is not None:
                self.line_to_edit['dataset'] = dataset
                self.line_to_edit['x_key'] = 0
                self.line_to_edit['y_key'] = 1
                self.x_key_combo_box.setCurrentIndex(0)
                self.y_key_combo_box.setCurrentIndex(1)

    def paintEvent(self, event):
        self.dataset_count_label.setText('{} Dataset{}'.format(len(self.datasets), "s" if len(self.datasets) != 1 else ""))
        self.line_count_label.setText('{} Line{}'.format(len(self.page['lines']), "s" if len(self.page['lines']) != 1 else ""))
        self.legend.setFixedSize(self.legend_widget.size())
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
            qp.drawText(QRect(10, 12 + i * y_spacing, 120, 20), Qt.AlignLeft, line['name']);
            line_pen = QPen()
            line_pen.setWidth(4)
            line_pen.setColor(line['colour'])
            line_pen.setStyle(line['style'])
            if line['pattern'] and line['style'] is Qt.CustomDashLine:
                line_pen.setDashPattern(line['pattern'])
            qp.setPen(line_pen)
            qp.drawLine(140, 10 + i * y_spacing + 10, 190, 10 + i * y_spacing + 10)
            # qp.drawRect(QRect(55, 10 + i * y_spacing, 50, 20))
            pass
        qp.end()
        self.legend.setPixmap(pixmap)

        if self.page['lines'] and self.datasets:
            self.chart.paint_lines([e for e in self.page['lines'] if e['display']])
            