from flask import request
import logging
import json
from user import User
from response import Response
from images import Image
import maps

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

    Moscow(res, req, user, command)
    return

    if user.room == 1:
        Room1(res, req, user, command)

    elif user.room == 2:
        Room2(res, req, user, command)

    elif user.room == 3:
        Room3(res, req, user, command)

    else:
        Moscow(res, req, user, command)


def Room1(res, req, user, command):
    user.room = 1

    if command == 'покажи комнату':
        if not user.seif:
            res.setImage('Комната с закрытым сейфом', Image.ROOM1_SEIF_CLOSED)
        elif not user.key:
            res.setImage('Комната с открытым сейфом с ключём внутри', Image.ROOM1_SEIF_OPENED_KEY)
        else:
            res.setImage('Комната с пустым открытым сейфом', Image.ROOM1_SEIF_OPENED)


    elif command == 'открыть сейф':
        if user.seif:
            res.addText('Сейф уже открыт.')
        else:
            res.addText('Сейф закрыт, нужен пароль.')

    elif command == 'открыть сейф паролем 1234':
        if user.seif:
            res.addText('Сейф уже открыт.')
        else:
            res.addText('Долго подбирая код вы воспользовались надписью на стене и открыли сейф.')
            res.addText('В сейфе лежит ключ.')
            user.seif = True

    elif command == 'взять ключ' and user.seif:
        if user.key:
            res.addText('Вы уже взяли ключ.')
        else:
            res.addText('Вы взяли ключ.')
            user.key = True

    elif command == 'выйти из комнаты':
        Room2(res, req, user, None)
        return

    else:
        if command:
            res.addText('Непонятная команда.')
        res.addText('Вы в какой-то комнате.')
        res.addText('Вам нужно выбраться отсюда.')
        res.addText('В комнате есть дверь, в углу сейф.')

    res.addText('Выберите команду:')

    res.addButton('покажи комнату')
    if not user.seif:
        res.addButton('открыть сейф')
    if user.password and not user.seif:
        res.addButton('открыть сейф паролем 1234')
    if not user.key and user.seif:
        res.addButton('взять ключ')
    res.addButton('выйти из комнаты')


def Room2(res, req, user: User, command):
    user.password = True
    user.room = 2

    if command == 'покажи комнату':
        if not user.window:
            res.setImage('Комната с окном', Image.ROOM2)
        else:
            res.setImage('Комната с окном, а под ним табуретка', Image.ROOM2_TABURETKA)

    elif command == 'зайти в начальную комнату':
        Room1(res, req, user, None)
        return

    elif command == 'открыть дверь ключом':
        if user.opened:
            res.addText('Дверь уже открыта.')
        elif user.key:
            res.addText('Вы открыли дверь.')
            user.opened = True
        else:
            res.addText('У вас нет ключа.')

    elif command == 'зайти в следующую комнату':
        if user.opened:
            Room3(res, req, user, None)
            return
        else:
            res.addText('Дверь закрыта на ключ.')

    elif command == 'вылезти в окно':
        if user.window:
            Moscow(res, req, user, None)

            return
        else:
            res.addText('Окно слишком высоко.')

    elif command == 'поставить табуретку под окно':
        if user.window:
            res.addText('Табуретка уже стоит под окном.')
        elif user.taburetka:
            res.addText('Вы поставили табуретку под окно.')
            user.window = True
            user.taburetka = False
        else:
            res.addText('У вас нет табуретки.')

    else:
        if command:
            res.addText('Непонятная команда.')
        res.addText('Вы во второй комнате.')
        res.addText('Здесь 2 двери, одна в первую комнату, другая в третью.')
        res.addText('Высоко под потолком окно.')
        res.addText('На стене надпись 1234, но вы бы ни за что не догадались, что это код от сейфа.')

    res.addText('Выберите команду:')

    res.addButton('покажи комнату')
    res.addButton('зайти в начальную комнату')
    res.addButton('зайти в следующую комнату')
    res.addButton('вылезти в окно')
    if user.taburetka and not user.window:
        res.addButton('поставить табуретку под окно')
    if user.key:
        res.addButton('открыть дверь ключом')


def Room3(res, req, user, command):
    user.room = 3

    if command == 'покажи комнату':
        if not user.taburetka:
            res.setImage('Комната с табуреткой', Image.ROOM3_TABURETKA)
        else:
            res.setImage('Пустая комната', Image.ROOM3)

    elif command == 'выйти из комнаты':
        Room2(res, req, user, None)
        return

    elif command == 'поднять табуретку':
        if user.taburetka:
            res.addText('Она у вас в руках.')
        else:
            res.addText('Вы с великим и упорным трудом подняли табуретку.')
            user.taburetka = True

    elif command == 'поставить табуретку':
        if user.taburetka:
            res.addText('Вы поставили табуретку обратно.')
            user.taburetka = False
        else:
            res.addText('Не путайте кнопки!')

    else:
        if command:
            res.addText('Непонятная команда.')
        res.addText('Вы в третьей комнате.')
        if not user.taburetka:
            res.addText('Здесь табуретка, дверь и всё.')
        else:
            res.addText('Интересно стоять в пустой комнате с табуреткой в руках.')

    res.addText('Выберите команду:')

    res.addButton('покажи комнату')
    res.addButton('выйти из комнаты')
    if user.taburetka:
        res.addButton('поставить табуретку')
    else:
        res.addButton('поднять табуретку')


# состояние - пользователь отгадывает город
GUESS_CITY = 1
# состояние - пользователь выбирает место, где праздновать победу
CHOOSE_PLACE = 2
# состояние - пользоватль выбирает подходит место или нет
CHOOSE_YES_NO = 3


def Moscow(res, req, user, command):
    if user.state == CHOOSE_YES_NO:
        if command == 'да':
            res.addText('Отлично! Квест пройден!')
            res.endSession()

        elif command == 'нет':
            res.addText('А где именно вы хотите отметить?')
            user.state = CHOOSE_PLACE

        elif command == 'покажи на карте' or command == 'как дойти?':
            res.addText('Подходит?')
            res.addButton('да')
            res.addButton('нет')

        else:
            res.addText('Не понятно. Так да или нет?')
            res.addButton('да')
            res.addButton('нет')
            res.addButton('покажи на карте')

    elif user.state == CHOOSE_PLACE:
        organization = maps.getOrganization(command)

        if organization:
            name = organization['properties']['CompanyMetaData']['name']
            id = organization['properties']['CompanyMetaData']['id']
            coords = organization['geometry']['coordinates']

            res.addText('Ближайшее ' + command + ' - ' + name + '.')
            res.addText('Подходит?')
            res.addButton('да')
            res.addButton('нет')
            res.addButton('покажи на карте', f'https://yandex.ru/maps/org/{id}')
            res.addButton('как дойти?', f'https://yandex.ru/maps/?rtext={coords[1]},{coords[0]}~{maps.OUR_COORD[1]},{maps.OUR_COORD[0]}&rtt=pd')
            user.state = CHOOSE_YES_NO

        else:
            res.addText('Не знаю такого места.')
            res.addText('Попробуйте другой вариант.')
            res.addButton('кафе')
            res.addButton('пиццерия')
            res.addButton('кинотеатр')

    elif user.state == GUESS_CITY:
        if command == 'покажи город':
            res.setImage('Город под названием ******. Отгадывай!', Image.MOSCOW)
            res.addText('Отгадывай')
        else:
            city = get_city(req)
            if city == 'москва':
                res.addText('Вы отгадали.')
                res.addText('Прямо перед вами Московский исторический музей.')
                res.addText('После стольких усилий вы наверняка хотите отпразновать победу.')
                res.addText('Выберите место для этого или предложите свой вариант.')
                res.addButton('кафе')
                res.addButton('пиццерия')
                res.addButton('кинотеатр')
                user.state = CHOOSE_PLACE
            elif city:
                res.addText('Знаю такой город, но это не он.')
                coord1 = maps.OUR_COORD
                coord2 = maps.getCoord(city)
                if coord1 and coord2:
                    distance = maps.lonlat_distance(coord1, coord2)
                    distance = int(distance / 1000)
                    res.addText(f'Вы ошиблись на {distance} км.')
                res.addText('Попробуй отгадать ещё раз.')
                res.addButton('покажи город')
            else:
                res.addText('Нет такого города. Попробуй отгадать ещё раз.')
                res.addButton('покажи город')

    else:
        res.addText('Вы вылезли через окно и неожиданно для вас вы оказываетесь на крыше пятиэтажки.')
        res.addText('Перед вами открывается вид на очень знакомый город.')
        res.addText('Попытайтесь его отгадать.')
        res.addButton('покажи город')
        user.state = GUESS_CITY


def get_first_name(req):
    # перебираем сущности
    for entity in req['request']['nlu']['entities']:
        # находим сущность с типом 'YANDEX.FIO'
        if entity['type'] == 'YANDEX.FIO':
            # Если есть сущность с ключом 'first_name',
            # то возвращаем ее значение.
            # Во всех остальных случаях возвращаем None.
            return entity['value'].get('first_name', None)


def get_city(req):
    # перебираем именованные сущности
    for entity in req['request']['nlu']['entities']:
        # если тип YANDEX.GEO, то пытаемся получить город(city), если нет, то возвращаем None
        if entity['type'] == 'YANDEX.GEO':
            # возвращаем None, если не нашли сущности с типом YANDEX.GEO
            return entity['value'].get('city', None)
