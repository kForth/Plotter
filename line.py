from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

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