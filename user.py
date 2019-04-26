class User:
    def __init__(self):
        self.name = None
        self.room = 1  # комната, где находимся
        self.key = False  # взяли ключ
        self.opened = False  # дверь открыта ключом
        self.seif = False  # сейф открыт
        self.password = False  # знаем пароль
        self.taburetka = False  # взяли табуретку
        self.window = False  # поставили табуретку под окно
        self.state = None
