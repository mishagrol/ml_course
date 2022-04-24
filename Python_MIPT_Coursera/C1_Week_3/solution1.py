class FileReader:
	def __init__(self, path_to_file):
		self.path_to_file = path_to_file
	def read(self):
		with open(self.path_to_file, 'r') as file:
			text = file.read()
		return text
		