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

	@staticmethod
	def is_age_valid(age):
		return 0 < age < 150

class Robot():
	def __init__(self, power):
		self._power = power 

	power = property()

	@power.setter
	def power(self, value):
		if value<0:
			self._power = 0
		else: 
			self._power = value

	@power.getter
	def power(self):
		print("Hello, i'm getter")
		return self._power
	
	@power.deleter
	def power(self):
		print("Robot must die")
		del self._power 


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


class Event():
	def __init__(self, description, date):
		self.description = description
		self.date = date

	def __str__(self):
		return f"Event \"{self.description}\" at {self.date}"

	def extract_description(self, user_string):
		return "Открытие ЧМ"

	def extract_date(sefl, user_string):
		return date(2018,6,14)


	@classmethod
	def from_string(cls, user_input):
		description = self.extract_description(user_input)
		event_date = self.extract_date(user_input)
		return cls(description, date)
