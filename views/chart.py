from PyQt5.QtCore import Qt, QRect, QLine, QPoint, QSize, QIODevice, QFile
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QPixmap, QCursor, QLinearGradient
from PyQt5.QtWidgets import QWidget, QApplication, QLabel
import numpy as np

from util import create_distinct_colours, fmod, timefunc, profilefunc

import math
from time import time

class ChartWidget:
    def __init__(self, parent, home_button, zoom_button, repaint_callback):
        self.parent = parent
        self.home_button = home_button
        self.zoom_button = zoom_button
        self.repaint_callback = repaint_callback

        self.parent.wheelEvent = self.wheelEvent

        self.parent_resizeEvent = self.parent.resizeEvent
        self.parent.resizeEvent = self.resizeEvent

        self.parent.mousePressEvent = self.mousePressEvent
        self.parent.mouseMoveEvent = self.mouseMoveEvent
        self.parent.mouseReleaseEvent = self.mouseReleaseEvent

        self.pages = []

        self.last_lines = []

        self.x_scale = 1
        self.y_scale = 1
        self.origin_offset = [0, 0]
        self.data_margin = 70
        self.axis_margin = [50, 30]

        self.axis_pen = QPen()
        self.axis_pen.setWidth(1)
        self.axis_pen.setColor(QColor(50, 50, 50))
        self.grid_pen = QPen()
        self.grid_pen.setWidth(1)
        self.grid_pen.setColor(QColor(50, 50, 50))
        self.sub_grid_pen = QPen()
        self.sub_grid_pen.setWidth(1)
        self.sub_grid_pen.setColor(QColor(200, 200, 200))
        self.sub_grid_pen.setStyle(Qt.DotLine)

        self.should_repaint = True
        self.last_axis_pixmap = None
        self.last_lines_pixmap = None
        self.last_tracker_pixmap = None

        self.last_important_mouse_pos = None
        self.current_mouse_pos = None
        self.last_size = self.parent.size()
        self.quick_drag_offset = [0, 0]

        self.mouse_mode = None

        self.zoom_button.clicked.connect(self.handle_zoom_button)
        self.home_button.clicked.connect(self.fit_data)

    def fit_data(self):
        if self.last_lines: 
            min_x = min([min(line.get_data()[0]) for line in self.last_lines])
            max_x = max([max(line.get_data()[0]) for line in self.last_lines])
            min_y = min([min(line.get_data()[1]) for line in self.last_lines])
            max_y = max([max(line.get_data()[1]) for line in self.last_lines])

            self.x_range = max_x - min_x
            self.y_range = max_y - min_y

            self.x_scale = (self.parent.width() - self.data_margin * 2) / (2.5 ** math.ceil(math.log(self.x_range)))
            self.y_scale = self.x_scale # (self.parent.height() - self.data_margin * 2) / (2.5 ** math.ceil(math.log(self.y_range)))

            self.axis_margin[0] = math.ceil(math.log(max(max_x, abs(min_x)))) + 3 * 14
            # self.axis_margin[1] = math.ceil(math.log(max(max_y, abs(min_y)))) + 3 * 14

            self.origin_offset = [
                (min_x + self.x_range / 2) * -self.x_scale,
                (min_y + self.y_range / 2) * self.y_scale
            ]
        else:
            self.x_range = 10
            self.y_range = 10
            self.origin_offset = [0, 0]
            self.x_scale = 1
            self.y_scale = 1
        self.repaint()

    def handle_zoom_button(self):
        self.mouse_mode = 'zoom'

    def zoom_to_rect(self, pt1, pt2):
        w = pt2.x() - pt1.x()
        h = pt2.y() - pt1.y()
        cx = pt1.x() + w / 2
        cy = pt1.y() + h / 2
        self.zoom([cx, cy], self.parent.width() / w, self.parent.height() / h, [self.parent.width()/2, self.parent.height()/2])
    
    def repaint(self, update_lines=True):
        for line in self.last_lines:
            line.set_pixmap_to_update()
        self.repaint_callback(update_lines, True)

    def wheelEvent(self, event):
        pos = event.pos()
        val = -event.angleDelta().y() + event.angleDelta().x()
        scroll_speed = 1.0 + abs(val) / 100
        if val < 0:
            scroll_speed = 1 / scroll_speed
        # self.zoom([self.parent.width()/2, self.parent.height()/2], scroll_speed, scroll_speed)
        self.zoom([pos.x(), pos.y()], scroll_speed, scroll_speed)
        self.repaint()

    def zoom(self, center_point, x_scale_diff=1, y_scale_diff=1, new_coords=None):
        if new_coords is None:
            new_coords = center_point
        center_val = self.calc_val_point(center_point)
        self.x_scale *= x_scale_diff
        self.y_scale *= y_scale_diff
        self.origin_offset = [
            -(center_val[0] * self.x_scale - new_coords[0] + self.parent.width() / 2),
            center_val[1] * self.y_scale + new_coords[1] - self.parent.height() / 2
        ]

    def mousePressEvent(self, event):
        self.last_important_mouse_pos = event.pos()
        if self.mouse_mode is None:
            if QApplication.keyboardModifiers() & Qt.ShiftModifier:
                self.mouse_mode = 'zoom'
            else:
                self.quick_drag_offset = [0, 0]
                self.mouse_mode = 'drag'

    def mouseMoveEvent(self, event):
        self.current_mouse_pos = event.pos()
        if self.mouse_mode == 'drag' and self.last_important_mouse_pos is not None:
            self.quick_drag_offset[0] += event.pos().x() - self.last_important_mouse_pos.x()
            self.quick_drag_offset[1] += event.pos().y() - self.last_important_mouse_pos.y()
            self.origin_offset[0] += event.pos().x() - self.last_important_mouse_pos.x()
            self.origin_offset[1] += event.pos().y() - self.last_important_mouse_pos.y()
            self.last_important_mouse_pos = event.pos()
            # self.repaint()
            self.paint_lines(self.last_lines, quick=True)
        else:
            self.paint_lines(self.last_lines, False, False)

    def mouseReleaseEvent(self, event):
        if self.mouse_mode == 'zoom':
            self.zoom_to_rect(self.last_important_mouse_pos, event.pos())
        self.last_important_mouse_pos = None
        self.mouse_mode = None
        self.repaint()

    def resizeEvent(self, event):
        size = self.parent.size()
        self.origin_offset[0] = self.origin_offset[0] * size.width() / self.last_size.width()
        self.origin_offset[1] = self.origin_offset[1] * size.height() / self.last_size.height()
        self.last_size = size
        self.parent_resizeEvent(event)
        self.repaint()

    # https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
    def ccw(self, A, B, C):
        return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

    def intersect(self, A, B, C, D):
        return self.ccw(A,C,D) != self.ccw(B,C,D) and self.ccw(A,B,C) != self.ccw(A,B,D)

    def draw_axis_pixmap(self):
        axis_pixmap = QPixmap(self.parent.size())
        axis_pixmap.fill(QColor(255, 255, 255, 0))
        qpainter = QPainter()
        qpainter.begin(axis_pixmap)

        origin = self.calc_gui_point([0, 0])

        axis_origin = [
            max(min(origin[0], self.parent.width() - self.axis_margin[0]), self.axis_margin[0]),
            max(min(origin[1], self.parent.height() - self.axis_margin[1]), self.axis_margin[1])
        ]

        qpainter.setPen(self.grid_pen)
        x_tick_width = 10 ** (math.floor(math.log10(self.parent.width() / self.x_scale) + 0.3))/2 * self.x_scale
        y_tick_width = 10 ** (math.floor(math.log10(self.parent.height() / self.y_scale) + 0.3))/2 * self.y_scale
            
        for i in range(int(max(self.parent.height(), self.parent.width()) // x_tick_width + 1)):
            x = i * x_tick_width + origin[0] % x_tick_width
            y = i * y_tick_width + origin[1] % y_tick_width
            x_sub_ticks = 5
            y_sub_ticks = 5
            qpainter.setPen(self.sub_grid_pen)
            for j in range(-x_sub_ticks, 10, 10 // x_sub_ticks):
                sub_x = x + j * x_tick_width / x_sub_ticks
                qpainter.drawLine(sub_x, 0, sub_x, self.parent.height()) # X Grid

            for j in range(-y_sub_ticks, 10, 10 // y_sub_ticks):
                sub_y = y + j * y_tick_width / y_sub_ticks
                qpainter.drawLine(0, sub_y, self.parent.width(), sub_y) # Y Grid

            qpainter.setPen(self.grid_pen)
            qpainter.drawLine(x, 0, x, self.parent.height()) # X Grid
            x_label = self.calc_val_point([x, origin[1]])[0]
            qpainter.drawText(QRect(x + 5, axis_origin[1] + 5, self.axis_margin[0], 15), Qt.AlignLeft, str(round(x_label, 2)))

            qpainter.drawLine(0, y, self.parent.width(), y) # Y Grid
            y_label = self.calc_val_point([origin[0], y])[1]
            qpainter.drawText(QRect(axis_origin[0]-self.axis_margin[0], y, self.axis_margin[0], 15), Qt.AlignRight, str(round(y_label, 2)))

        if self.mouse_mode == 'zoom' and self.last_important_mouse_pos is not None and self.current_mouse_pos is not None:
            pt = self.last_important_mouse_pos
            pt2 = self.current_mouse_pos
            qpainter.drawRect(pt.x(), pt.y(), pt2.x() - pt.x(), pt2.y() - pt.y())

        qpainter.end()
        return axis_pixmap

    def draw_tracker_pixmap(self, cursor_pos):
        tracker_pixmap = QPixmap(self.parent.size())
        tracker_pixmap.fill(QColor(255, 255, 255, 0))
        qpainter = QPainter()
        qpainter.begin(tracker_pixmap)

        origin = self.calc_gui_point([0, 0])
        axis_origin = [
            max(min(origin[0], self.parent.width() - self.axis_margin[0]), self.axis_margin[0]),
            max(min(origin[1], self.parent.height() - self.axis_margin[1]), self.axis_margin[1])
        ]

        qpainter.setPen(self.axis_pen)
        pnt = self.calc_val_point([cursor_pos.x(), cursor_pos.y()])
        x_label = str(round(pnt[0], 2))
        y_label = str(round(pnt[1], 2))
        str_rect = QRect(cursor_pos.x() + 5, axis_origin[1], qpainter.fontMetrics().width(x_label), 25)

        g_rect = QRect(str_rect.x() - 30, str_rect.y(), 30, str_rect.height())
        gradient = QLinearGradient(QPoint(g_rect.right(), g_rect.center().y()), QPoint(g_rect.left(), g_rect.center().y()))
        gradient.setColorAt(0, QColor(255, 255, 255))
        gradient.setColorAt(1, QColor(255, 255, 255, 0))
        qpainter.fillRect(g_rect, gradient)

        g_rect = QRect(str_rect.right(), str_rect.y(), 30, str_rect.height())
        gradient = QLinearGradient(QPoint(g_rect.left(), g_rect.center().y()), QPoint(g_rect.right(), g_rect.center().y()))
        gradient.setColorAt(0, QColor(255, 255, 255))
        gradient.setColorAt(1, QColor(255, 255, 255, 0))
        qpainter.fillRect(g_rect, gradient)

        qpainter.fillRect(str_rect, QColor(255, 255, 255))
        qpainter.drawText(str_rect, Qt.AlignLeft | Qt.AlignCenter, x_label)
        qpainter.drawLine(cursor_pos.x(), axis_origin[1], cursor_pos.x(), axis_origin[1] + 10)

        label_width = qpainter.fontMetrics().width(y_label)
        str_rect = QRect(axis_origin[0] - label_width - 1, cursor_pos.y() + 1, label_width, 15)

        g_rect = QRect(str_rect.x(), str_rect.y() - 10, str_rect.width(), 10)
        gradient = QLinearGradient(QPoint(g_rect.center().x(), g_rect.bottom()), QPoint(g_rect.center().x(), g_rect.top()))
        gradient.setColorAt(0, QColor(255, 255, 255))
        gradient.setColorAt(1, QColor(255, 255, 255, 0))
        qpainter.fillRect(g_rect, gradient)
        
        g_rect = QRect(str_rect.x(), str_rect.bottom(), str_rect.width(), 10)
        gradient = QLinearGradient(QPoint(g_rect.center().x(), g_rect.top()), QPoint(g_rect.center().x(), g_rect.bottom()))
        gradient.setColorAt(0, QColor(255, 255, 255))
        gradient.setColorAt(1, QColor(255, 255, 255, 0))
        qpainter.fillRect(g_rect, gradient)

        qpainter.fillRect(str_rect, QColor(255, 255, 255))
        qpainter.drawText(str_rect, Qt.AlignRight | Qt.AlignCenter, y_label)
        qpainter.drawLine(axis_origin[0], cursor_pos.y(), axis_origin[0] - 10, cursor_pos.y())

        qpainter.end()
        return tracker_pixmap

    @profilefunc
    def get_lines_pixmap(self, lines):
        pixmap = QPixmap(self.parent.size())
        pixmap.fill(QColor(255, 255, 255, 0))
        qp = QPainter()
        qp.begin(pixmap)
        for line in lines:
            qp.drawPixmap(QPoint(0, 0), line.get_pixmap(self.parent.size(), self.calc_gui_point))
        qp.end()
        return pixmap

    def paint_lines(self, lines, update_lines=True, update_axis=True, update_tracker=True, quick=False):
        st = time()
        pixmap = QPixmap(self.parent.size())
        pixmap.fill(QColor(255, 255, 255))
        qp = QPainter()
        qp.begin(pixmap)

        self.last_lines = lines
        qp.setRenderHints(QPainter.SmoothPixmapTransform | QPainter.Antialiasing)

        if quick and self.last_lines_pixmap is not None:
            qp.fillRect(QRect(0, 0, self.parent.width(), self.parent.height()), QColor("#fafafa"))
            qp.drawPixmap(QPoint(*self.quick_drag_offset), self.last_lines_pixmap)
        else:
            # if update_lines or not self.last_lines_pixmap:
            self.last_lines_pixmap = self.draw_lines_pixmap(lines)
            qp.drawPixmap(QPoint(0, 0), self.last_lines_pixmap)

        if update_axis or not self.last_axis_pixmap:
            self.last_axis_pixmap = self.draw_axis_pixmap()
        qp.drawPixmap(QPoint(0, 0), self.last_axis_pixmap)

        cursor_pos = self.parent.mapFromGlobal(QCursor.pos())
        if cursor_pos.x() > 0 and cursor_pos.x() < self.parent.width() and cursor_pos.y() > 0 and cursor_pos.y() < self.parent.height():
            self.last_tracker_pixmap = self.draw_tracker_pixmap(cursor_pos)
            qp.drawPixmap(QPoint(0, 0), self.last_tracker_pixmap)

        qp.end()
        self.parent.setPixmap(pixmap)

    def is_point_visible(self, pt):
        return (0 <= pt[0] <= self.parent.width()) and (0 <= pt[1] <= self.parent.height())

    def is_segment_visible(self, pt, pt2, simple=True):
        return self.is_point_visible(pt) or self.is_point_visible(pt2) or \
                (not simple and (self.intersect(pt, pt2, [0, 0], [self.parent.width(), 0]) or \
                self.intersect(pt, pt2, [0, 0], [0, self.parent.height()]) or \
                self.intersect(pt, pt2, [0, self.parent.height()], [self.parent.width(), self.parent.height()]) or \
                self.intersect(pt, pt2, [self.parent.width(), 0], [self.parent.width(), self.parent.height()])))

    def calc_gui_point(self, pnt):
        x = pnt[0] * self.x_scale + self.parent.width() / 2 + self.origin_offset[0]
        y = self.parent.height() / 2 - (pnt[1] * self.y_scale) + self.origin_offset[1]
        return x, y

    def calc_val_point(self, pnt):
        x = (pnt[0] - self.origin_offset[0] - self.parent.width() / 2) / self.x_scale
        y = (pnt[1] - self.origin_offset[1] - self.parent.height() / 2) / -self.y_scale
        return x, y
