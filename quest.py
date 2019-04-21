from flask import request
import logging
import json
from user import User
from response import Response

# создаём словарь, где для каждого пользователя мы будем хранить его данные
users = {}


def main():
    logging.info('Request: %r', request.json)
    response = Response(request)
    handle_dialog(response, request.json)
    logging.info('Response: %r', response)
    return json.dumps(response.res)


def handle_dialog(res, req):
    user_id = req['session']['user_id']

    if req['session']['new']:
        res.addText('Привет! Назови свое имя!')
        user = User()
        users[user_id] = user
        return

    user = users[user_id]
    command = req['request']['original_utterance'].lower()

    if user.name is None:
        first_name = get_first_name(req)

        if first_name is None:
            res.addText('Не расслышала имя. Повтори, пожалуйста!')
            return

        user.name = first_name
        res.addText('Приятно познакомиться, ' + first_name.title() + '.')
        res.addText('Давай поиграем.')
        command = None

    if user.room == 1:
        Room1(res, user, command)

    elif user.room == 2:
        Room2(res, user, command)

    elif user.room == 3:
        Room3(res, user, command)


def Room1(res, user, command):
    user.room = 1

    if command == 'открыть сейф':
        if user.seif:
            res.addText('Сейф уже открыт.')
        else:
            res.addText('Сейф закрыт, нужен пароль.')

    elif command == 'открыть сейф паролем 1234':
        if user.seif:
            res.addText('Сейф уже открыт.')
        else:
            res.addText('Сейф открылся. Внутри лежит ключ.')
            user.seif = True

    elif command == 'взять ключ' and user.seif:
        if user.key:
            res.addText('Вы уже взяли ключ.')
        else:
            res.addText('Вы взяли ключ.')
            user.key = True

    elif command == 'выйти из комнаты':
        Room2(res, user, None)
        return

    else:
        if command:
            res.addText('Непонятная команда.')
        res.addText('Вы в какой-то комнате.')
        res.addText('Вам нужно выбраться отсюда.')
        res.addText('В комнате есть дверь, в углу сейф.')

    res.addText('Выберите команду:')

    if not user.seif:
        res.addButton('открыть сейф')
    if user.password and not user.seif:
        res.addButton('открыть сейф паролем 1234')
    if not user.key and user.seif:
        res.addButton('взять ключ')
    res.addButton('выйти из комнаты')


def Room2(res, user: User, command):
    user.password = True
    user.room = 2

    if command == 'зайти в начальную комнату':
        Room1(res, user, None)
        return

    elif command == 'открыть дверь ключом':
        if user.opened:
            res.addText('Дверь уже открыта')
        elif user.key:
            res.addText('Вы открыли дверь')
            user.opened = True
        else:
            res.addText('У вас нет ключа.')

    elif command == 'зайти в следующую комнату':
        if user.opened:
            Room3(res, user, None)
            return
        else:
            res.addText('Дверь закрыта на ключ.')

    elif command == 'вылезти в окно':
        if user.window:
            res.addText('Поздравляем, вы прошли квест!')
            return
        else:
            res.addText('Окно слишком высоко')

    elif command == 'поставить табуретку под окно':
        if user.window:
            res.addText('Табуретка уже стоит под окном')
        elif user.taburetka:
            res.addText('Вы поставили табуретку под окно')
            user.window = True
            user.taburetka = False
        else:
            res.addText('У вас нет табуретки')

    else:
        if command:
            res.addText('Непонятная команда.')
        res.addText('Вы во второй комнате.')
        res.addText('Здесь 2 двери, одна в первую комнату, другая в третью.')
        res.addText('Высоко под потолком окно.')
        res.addText('На стене надпись 1234, но вы бы ни за что не догадались, что это код от сейфа.')

    res.addButton('зайти в начальную комнату')
    res.addButton('зайти в следующую комнату')
    res.addButton('вылезти в окно')
    if user.taburetka and not user.window:
        res.addButton('поставить табуретку под окно')
    if user.key:
        res.addButton('открыть дверь ключом')


def Room3(res, user, command):
    res.addText('Вы в третьей комнате.')
    res.addText('Здесь только дверь назад.')
    if not user.taburetka:
        res.addText('В углу стоит табуретка.')

    # табуретки нет
    if not user.taburetka:
        res.addButton('зайти в прошлую комнату')  # 1
        res.addButton('взять табуретку')  # 2
        if command == 'зайти в прошлую комнату':
            res.addText('Вы вышли из комнаты и попали во вторую комнату.')
            user.room = 2
            return
        elif command == 'взять табуретку':
            res.addText('Вы взяли табуретку.')
            user.taburetka = True
            return
        else:
            res.addText('Неверная команда, введите еще раз.')
    # табуретка взята
    else:
        res.addButton('зайти в прошлую комнату комнату')  # 1
        res.addButton('поставить табуретку обратно')  # 2
        if command == 'зайти в прошлую комнату комнату':
            res.addText('Вы вышли из комнаты и попали во вторую комнату.')
            user.room = 2
            return
        elif command == 'поставить табуретку обратно':
            res.addText('Вы поставили табуретку.')
            user.taburetka = False
            return
        else:
            res.addText('Неверная команда, введите еще раз.')


def get_first_name(req):
    # перебираем сущности
    for entity in req['request']['nlu']['entities']:
        # находим сущность с типом 'YANDEX.FIO'
        if entity['type'] == 'YANDEX.FIO':
            # Если есть сущность с ключом 'first_name',
            # то возвращаем ее значение.
            # Во всех остальных случаях возвращаем None.
            return entity['value'].get('first_name', None)
