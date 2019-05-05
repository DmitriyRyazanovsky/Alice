from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///alice.db')
Base = declarative_base()


class DbUser(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True)
    name = Column(String)
    room = Column(Integer)
    key3 = Column(Boolean, nullable=False)
    key4 = Column(Boolean, nullable=False)
    opened3 = Column(Boolean, nullable=False)
    opened4 = Column(Boolean, nullable=False)
    seif = Column(Boolean, nullable=False)
    password = Column(Boolean, nullable=False)
    taburetka = Column(Boolean, nullable=False)
    window = Column(Boolean, nullable=False)
    choko = Column(Boolean, nullable=False)
    fridge = Column(Boolean, nullable=False)
    state = Column(Integer)

    def __init__(self, id):
        self.id = id  # ид пользователя
        self.name = None  # имя пользователя
        self.room = 1  # комната, где находимся
        self.key3 = False  # взяли ключ от комнаты 3
        self.key4 = False  # взяли ключ от комнаты 4
        self.opened3 = False  # дверь 3 открыта ключом
        self.opened4 = False  # дверь 4 открыта ключом
        self.seif = False  # сейф открыт
        self.password = False  # знаем пароль
        self.taburetka = False  # взяли табуретку
        self.window = False  # поставили табуретку под окно
        self.choko = False  # съели шоколадку
        self.fridge = False  # открыли холодильник
        self.state = None  # текущий этап в Москве


def __repr__(self):
    return "<User('%s','%s')>" % (self.id, self.name)


# Создание таблицы
Base.metadata.create_all(engine)

# Создание сессии в базе данных
Session = sessionmaker(bind=engine)
session = Session()


# создаем пользователя в базе данных
def createUser(id: str):
    # если такой был, то удаляем
    user = findUser(id)
    if user:
        session.delete(user)
    user = DbUser(id)
    session.add(user)
    return user


# находим пользователя в базе данных по ид
def findUser(id: str):
    return session.query(DbUser).filter_by(id=id).first()


# сохраняем изменения в базе данных
def commit():
    session.commit()
