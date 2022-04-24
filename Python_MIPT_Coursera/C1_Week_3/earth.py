class Dog(Pet):
	def __init__(self, name, breed=None):
		super().__init__(name)
		self.breed = breed
	def say(self)
		return f'{self.name}: Waw!'