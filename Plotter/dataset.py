class Dataset:
	def __init__(self, filepath, data, delimiter, header_row, skip_n_rows):
		self.filepath = filepath
		self.data = data
		self.delimiter = delimiter
		self.header_row = header_row
		self.skip_n_rows = skip_n_rows