class Human():
	def __init__(self, name, age=0):
		self.name = name
		self.age = age
	def __repr__(self):
		return self.name
	def _say(self, text):
		print(text)

	def say_name(self):
		self._say(f"Hello, my name id {self.name}")
	def say_age(self):
		self._say(f"Hello, my age is {self.age}")

class Planet():
	def __init__(self, name, population=None):
		self.name = name
		self.population = population or []

	def add_human(self, human):
		print(f"Welcome to {self.name}, {human.name}") 
		self.population.append(human)
	def __str__(self):
		return self.name
	def __repr__(self):
		return self.name