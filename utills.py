import requests
from config import *


class CreateCoordinate(object):
    """
    класс для получения координт дома, если ошибка, то ее траит
    """

    def __init__(self):
        pass

    @staticmethod
    def get_coordinate(address):
        q = f'http://geocode-maps.yandex.ru/1.x/?apikey={YANDEX_API_KEY}&geocode={address}&format=json'
        result = requests.get(q).json()
        return result.get('response').get('GeoObjectCollection').get(
            'featureMember')[0].get('GeoObject').get(
            'Point').get('pos').split(' ')


print (CreateCoordinate.get_coordinate('нижняя первомайская'))
