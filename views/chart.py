from PyQt5.QtCore import Qt, QRect, QLine, QPoint
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QPixmap, QCursor, QLinearGradient
from PyQt5.QtWidgets import QWidget, QApplication, QLabel

from util import create_distinct_colours, fmod

from enum import Enum
import math
from time import time

class MouseMode(Enum):
    drag = 0
    zoom = 1

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
        self.last_data = []

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

        self.last_important_mouse_pos = None
        self.current_mouse_pos = None
        self.last_size = self.parent.size()

        self.mouse_mode = None

        self.zoom_button.clicked.connect(self.handle_zoom_button)
        self.home_button.clicked.connect(self.fit_data)

    def fit_data(self):
        if self.last_data: 
            min_x = min([min([e[0] for e in line]) for line in self.last_data])
            max_x = max([max([e[0] for e in line]) for line in self.last_data])
            min_y = min([min([e[1] for e in line]) for line in self.last_data])
            max_y = max([max([e[1] for e in line]) for line in self.last_data])

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
    
    def repaint(self):
        self.repaint_callback()
        # self.parent.repaint()

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
                self.mouse_mode = 'drag'

    def mouseMoveEvent(self, event):
        self.current_mouse_pos = event.pos()
        if self.mouse_mode == 'drag' and self.last_important_mouse_pos is not None:
            pos = event.pos()
            self.origin_offset[0] += pos.x() - self.last_important_mouse_pos.x()
            self.origin_offset[1] += pos.y() - self.last_important_mouse_pos.y()
            self.last_important_mouse_pos = pos
        self.repaint()

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

    def paint_lines(self, lines):
        pixmap = QPixmap(self.parent.size())
        pixmap.fill(QColor('#fff'))
        qp = QPainter()
        qp.begin(pixmap)

        self.paint_chart(qp, lines)

        qp.end()
        self.parent.setPixmap(pixmap)

    def paint_line(self, qp, points):
        self.last_data.append(points)
        for i in range(1, len(points)):
            x, y = self.calc_gui_point(points[i])
            x2, y2 = self.calc_gui_point(points[i-1])
            if self.is_segment_visible([x, y], [x2, y2]):
                qp.drawLine(x, y, x2, y2)

    # https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
    def ccw(self, A, B, C):
        return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

    def intersect(self, A, B, C, D):
        return self.ccw(A,C,D) != self.ccw(B,C,D) and self.ccw(A,B,C) != self.ccw(A,B,D)

    def is_segment_visible(self, pt, pt2):
        return ((0 <= pt[0] <= self.parent.width()) and (0 <= pt[1] <= self.parent.height())) or \
                ((0 <= pt2[0] <= self.parent.width()) and (0 <= pt2[1] <= self.parent.height())) or \
                self.intersect(pt, pt2, [0, 0], [self.parent.width(), 0]) or \
                self.intersect(pt, pt2, [0, 0], [0, self.parent.height()]) or \
                self.intersect(pt, pt2, [0, self.parent.height()], [self.parent.width(), self.parent.height()]) or \
                self.intersect(pt, pt2, [self.parent.width(), 0], [self.parent.width(), self.parent.height()])

    def paint_chart(self, qp, lines):
        print("painting chart", time())
        self.last_lines = lines
        self.last_data = []
        qp.setRenderHints(QPainter.SmoothPixmapTransform | QPainter.Antialiasing)

        track_cursor = False
        pos = self.parent.mapFromGlobal(QCursor.pos())
        cursor_pos = [
            pos.x(),
            pos.y()
        ]
        if cursor_pos[0] > 0 and cursor_pos[0] < self.parent.width() and cursor_pos[1] > 0 and cursor_pos[1] < self.parent.height():
            track_cursor = True

        origin = self.calc_gui_point([0, 0])

        axis_origin = [
            max(min(origin[0], self.parent.width() - self.axis_margin[0]), self.axis_margin[0]),
            max(min(origin[1], self.parent.height() - self.axis_margin[1]), self.axis_margin[1])
        ]

        qp.setPen(self.grid_pen)
        x_tick_width = 10 ** (math.floor(math.log10(self.parent.width() / self.x_scale) + 0.3))/2 * self.x_scale
        y_tick_width = 10 ** (math.floor(math.log10(self.parent.height() / self.y_scale) + 0.3))/2 * self.y_scale
            
        for i in range(max(self.parent.height(), self.parent.width() // x_tick_width + 1)):
            x = i * x_tick_width + origin[0] % x_tick_width
            y = i * y_tick_width + origin[1] % y_tick_width
            x_sub_ticks = 5
            y_sub_ticks = 5
            qp.setPen(self.sub_grid_pen)
            for j in range(-x_sub_ticks, 10, 10 // x_sub_ticks):
                sub_x = x + j * x_tick_width / x_sub_ticks
                qp.drawLine(sub_x, 0, sub_x, self.parent.height()) # X Grid

            for j in range(-y_sub_ticks, 10, 10 // y_sub_ticks):
                sub_y = y + j * y_tick_width / y_sub_ticks
                qp.drawLine(0, sub_y, self.parent.width(), sub_y) # Y Grid

            qp.setPen(self.grid_pen)
            qp.drawLine(x, 0, x, self.parent.height()) # X Grid
            x_label = self.calc_val_point([x, origin[1]])[0]
            qp.drawText(QRect(x + 5, axis_origin[1] + 5, self.axis_margin[0], 15), Qt.AlignLeft, str(round(x_label, 2)));

            qp.drawLine(0, y, self.parent.width(), y) # Y Grid
            y_label = self.calc_val_point([origin[0], y])[1]
            qp.drawText(QRect(axis_origin[0]-self.axis_margin[0], y, self.axis_margin[0], 15), Qt.AlignRight, str(round(y_label, 2)));


        #  Draw Data Lines
        for line in lines:
            data = []
            for i, e in enumerate(line.dataset.data[(1 if line.dataset.header_row else 0):]):
                data.append((i if line.x_key == 0 else e[line.x_key-1], i if line.y_key == 0 else e[line.y_key-1]))
            if line.sort_by_x:
                data = sorted(data, key=lambda e: e[0])
            if line.display_line:
                pen = QPen()
                pen.setStyle(line.line_style)
                pen.setCapStyle(Qt.RoundCap);
                if line.line_pattern and line.line_style is Qt.CustomDashLine:
                    pen.setDashPattern(line.line_pattern)
                pen.setColor(line.line_colour)
                pen.setWidth(line.line_width)
                qp.setPen(pen)
                self.paint_line(qp, data)

        if track_cursor:
            qp.setPen(self.axis_pen)
            pnt = self.calc_val_point(cursor_pos)
            x_label = str(round(pnt[0], 2))
            y_label = str(round(pnt[1], 2))
            str_rect = QRect(cursor_pos[0] + 5, axis_origin[1], qp.fontMetrics().width(x_label), 25)

            g_rect = QRect(str_rect.x() - 30, str_rect.y(), 30, str_rect.height())
            gradient = QLinearGradient(QPoint(g_rect.right(), g_rect.center().y()), QPoint(g_rect.left(), g_rect.center().y()))
            gradient.setColorAt(0, QColor(255, 255, 255));
            gradient.setColorAt(1, QColor(255, 255, 255, 0));
            qp.fillRect(g_rect, gradient)

            g_rect = QRect(str_rect.right(), str_rect.y(), 30, str_rect.height())
            gradient = QLinearGradient(QPoint(g_rect.left(), g_rect.center().y()), QPoint(g_rect.right(), g_rect.center().y()))
            gradient.setColorAt(0, QColor(255, 255, 255));
            gradient.setColorAt(1, QColor(255, 255, 255, 0));
            qp.fillRect(g_rect, gradient)

            qp.fillRect(str_rect, QColor(255, 255, 255))
            qp.drawText(str_rect, Qt.AlignLeft | Qt.AlignCenter, x_label)
            qp.drawLine(cursor_pos[0], axis_origin[1], cursor_pos[0], axis_origin[1] + 10)

            label_width = qp.fontMetrics().width(y_label)
            str_rect = QRect(axis_origin[0] - label_width - 1, cursor_pos[1] + 1, label_width, 15)

            g_rect = QRect(str_rect.x(), str_rect.y() - 10, str_rect.width(), 10)
            gradient = QLinearGradient(QPoint(g_rect.center().x(), g_rect.bottom()), QPoint(g_rect.center().x(), g_rect.top()))
            gradient.setColorAt(0, QColor(255, 255, 255));
            gradient.setColorAt(1, QColor(255, 255, 255, 0));
            qp.fillRect(g_rect, gradient)
            
            g_rect = QRect(str_rect.x(), str_rect.bottom(), str_rect.width(), 10)
            gradient = QLinearGradient(QPoint(g_rect.center().x(), g_rect.top()), QPoint(g_rect.center().x(), g_rect.bottom()))
            gradient.setColorAt(0, QColor(255, 255, 255));
            gradient.setColorAt(1, QColor(255, 255, 255, 0));
            qp.fillRect(g_rect, gradient)

            qp.fillRect(str_rect, QColor(255, 255, 255))
            qp.drawText(str_rect, Qt.AlignRight | Qt.AlignCenter, y_label)
            qp.drawLine(axis_origin[0], cursor_pos[1], axis_origin[0] - 10, cursor_pos[1])

        if self.mouse_mode == 'zoom' and self.last_important_mouse_pos is not None and self.current_mouse_pos is not None:
            pt = self.last_important_mouse_pos
            pt2 = self.current_mouse_pos
            qp.drawRect(pt.x(), pt.y(), pt2.x() - pt.x(), pt2.y() - pt.y())

    def calc_gui_point(self, pnt):
        x = pnt[0] * self.x_scale + self.origin_offset[0] + self.parent.width() / 2
        y = self.parent.height() / 2 + self.origin_offset[1] - (pnt[1] * self.y_scale)
        return x, y

    def calc_val_point(self, pnt):
        x = (pnt[0] - self.origin_offset[0] - self.parent.width() / 2) / self.x_scale
        y = (pnt[1] - self.origin_offset[1] - self.parent.height() / 2) / -self.y_scale
        return x, y
