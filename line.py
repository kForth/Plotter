from PyQt5.QtCore import Qt, QRect, QLine, QPoint, QSize, QIODevice, QFile
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QPixmap, QCursor, QLinearGradient
from PyQt5.QtGui import QColor
import numpy as np

class Line:
	def __init__(self, name, dataset, line_colour=QColor(50, 50, 250), display_line=True, line_style=Qt.SolidLine, line_pattern=[], line_width=1.5, point_colour=QColor(0, 0, 255), point_shape=0, display_point=False, point_size=3, sort_by_x=False, x_key=0, y_key=1):
		self.name = name
		self.dataset = dataset
		self.line_colour = line_colour
		self.line_style = line_style
		self.line_pattern = line_pattern
		self.display_line = display_line
		self.line_width = line_width
		self.point_colour = point_colour
		self.point_shape = point_shape
		self.display_point = display_point
		self.point_size = point_size
		self.x_key = x_key
		self.y_key = y_key
		self.sort_by_x = sort_by_x
		self._data = None
		self._pixmap = None

		self._should_update_data = False
		self._should_update_pixmap = False

	def set_all_to_update(self):
		self._should_update_data = True
		self._should_update_pixmap = True

	def get_data(self, update=False):
		if self._data is None or update or self._should_update_data:
			self._should_update_data = False
			self.update_data()
		return self._data

	def set_data_to_update(self):
		self._should_update_data = True

	def update_data(self):
		print("updating data")
		x_data = []
		y_data = []
		for i, e in enumerate(self.dataset.data):
			if i == 0 and self.dataset.header_row:
				continue
			pt = (i if self.x_key == 0 else e[self.x_key-1], i if self.y_key == 0 else e[self.y_key-1])
			x_data.append(pt[0])
			y_data.append(pt[1])
		self._data = [x_data, y_data]
		self._pixmap = None
		return self._data

	def get_pixmap(self, size, convert_to_gui_point, update=False):
		if self._pixmap is None or update or self._should_update_pixmap:
			self._should_update_pixmap = False
			self.update_pixmap(size, convert_to_gui_point)
		return self._pixmap

	def set_pixmap_to_update(self):
		self._should_update_pixmap = True

	def update_pixmap(self, size, convert_to_gui_point):
		pixmap = QPixmap(size)
		pixmap.fill(QColor(255, 255, 255, 0))
		qp = QPainter()
		qp.begin(pixmap)

		if self.display_line or self.display_points:
			x_data, y_data = self.get_data()

			line_points = np.dstack(convert_to_gui_point([np.array(x_data), np.array(y_data)]))[0]
			if self.sort_by_x:
				line_points = line_points[line_points[:,0].argsort()]

			if self.display_line and len(line_points) > 0:
				pen = QPen()
				pen.setStyle(self.line_style)
				pen.setCapStyle(Qt.RoundCap)
				if self.line_style is Qt.CustomDashLine and self.line_pattern:
					pen.setDashPattern(self.line_pattern)
				pen.setColor(self.line_colour)
				pen.setWidth(self.line_width)
				qp.setPen(pen)
				qp.drawPolyline(*[QPoint(e[0], e[1]) for e in line_points])  # if self.is_point_visible(e)])

			if self.display_point:
				pass
		qp.end()
		self._pixmap = pixmap
		return self._pixmap