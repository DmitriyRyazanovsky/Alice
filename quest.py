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

    # если пользователь новый, то просим его представиться.
    if req['session']['new']:
        res.setText('Привет! Назови свое имя!')
        # создаём пользователя
        user = User()
        users[user_id] = user
        return

    # если пользователь не новый, то попадаем сюда.
    # если поле имени пустое, то это говорит о том,
    # что пользователь ещё не представился.
    user = users[user_id]
    if user.name is None:
        first_name = get_first_name(req)
        if first_name is None:
            res.setText('Не расслышала имя. Повтори, пожалуйста!')
            return

        user.name = first_name
        res.setText(
            'Приятно познакомиться, ' + first_name.title() + '.' + \
            'Давай поиграем. Вы находитесь в начальной комнате. Вам нужно выбраться отсюда. ' + \
            'В комнате есть дверь, в углу сейф. Выберите команду: ')
        res.addButton('зайти в дверь')
        res.addButton('открыть сейф')

    else:
        button = req['request']['original_utterance'].lower()
        if button == 'зайти в дверь' and not user.password:
            res.setText('Вы зашли в дверь') + \
            'Вы вышли из комнаты и попали в другую комнату.'
            user.room = 2
            return
        elif button == 'открыть сейф':
            res.setText('Сейф закрыт, нужен пароль.')
            return
        else:
            res.setText('Непонятно')
            return


def get_first_name(req):
    # перебираем сущности
    for entity in req['request']['nlu']['entities']:
        # находим сущность с типом 'YANDEX.FIO'
        if entity['type'] == 'YANDEX.FIO':
            # Если есть сущность с ключом 'first_name',
            # то возвращаем ее значение.
            # Во всех остальных случаях возвращаем None.
            return entity['value'].get('first_name', None)
