class Dog():
    """Простая модель собаки"""
    def __init__(self, name, age):
        """Инициализируем атрибуты имя и возраст"""
        self.name = name
        self.age = age
        print("Собака создана")
    def sit(self):
        """Собака будет садиться по команде"""
        print(self.name.title() + "собака села")

    def jump(self):
        """Собака будет прыгать по команде"""
        print(self.name.title() + "собака прыгнула")
        
