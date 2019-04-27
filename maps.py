import requests
import logging
import math

OUR_COORD = (37.61663946, 55.75657055)


def getCoord(name):
    # описание, как получить координаты объекта:

    geocoder_request = "http://geocode-maps.yandex.ru/1.x/?geocode=" + name + "&format=json"

    # Выполняем запрос.
    try:
        response = requests.get(geocoder_request)
        if response:
            # Преобразуем ответ в json-объект
            json_response = response.json()
            coord = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
            x, y = coord.split()
            return (float(x), float(y))
        else:
            logging.error("Ошибка выполнения запроса:")
            logging.error(geocoder_request)
            logging.error("Http статус:", response.status_code, "(", response.reason, ")")
    except:
        logging.error("Запрос не удалось выполнить. Проверьте подключение к сети Интернет.")

    return None


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000  # 111 километров в метрах
    a_lon, a_lat = a
    b_lon, b_lat = b

    # Берем среднюю по широте точку и считаем коэффициент для нее.
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    # Вычисляем смещения в метрах по вертикали и горизонтали.
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    # Вычисляем расстояние между точками.
    distance = math.sqrt(dx * dx + dy * dy)

    return distance


def getOrganization(name):
    # описание как получить информация об организации
    # https://tech.yandex.ru/maps/doc/geosearch/concepts/response_structure_business-docpage/

    key = 'fe7b2a61-955c-4291-aef1-baf38b3f2de8'
    text = 'ближайшее ' + name
    coord = f'{OUR_COORD[0]},{OUR_COORD[1]}'
    request = f'https://search-maps.yandex.ru/v1/?apikey={key}&text={text}&lang=ru_RU&ll={coord}&results=1'

    # Выполняем запрос.
    try:
        response = requests.get(request)
        if response:
            # Преобразуем ответ в json-объект
            json_response = response.json()
            features = json_response['features']
            if len(features) > 0:
                return features[0]
        else:
            logging.error("Ошибка выполнения запроса:")
            logging.error(request)
            logging.error("Http статус:", response.status_code, "(", response.reason, ")")
    except:
        logging.error("Запрос не удалось выполнить. Проверьте подключение к сети Интернет.")

    return None
