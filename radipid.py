import requests
from collections.abc import Iterable
from telebot import types
from loguru import logger
from decouple import config
from re import sub
from telebot.types import InputMediaPhoto

from database.user_bd import get_user_info

rapidapi_key = config('RAPIDAPI_KEY')
headers = {'x-rapidapi-host': 'hotels4.p.rapidapi.com', 'x-rapidapi-key': rapidapi_key}


@logger.catch
def find_destinations(destination: str) -> dict:
    """ Функция поиска вариантов по запросу"""

    url = 'https://hotels4.p.rapidapi.com/locations/v2/search'
    query_city = {'query': destination, 'locale': 'ru_RU', 'currency': 'USD'}
    destinations_dict = dict()
    try:
        response_hotels = requests.request('GET', url, headers=headers, params=query_city, timeout=10)
        suggestions_hotels = response_hotels.json()['suggestions'][0]['entities']
        for i_elem in suggestions_hotels:
            caption = sub(r'<.*?>', '', i_elem['caption'])
            destination_id = i_elem['destinationId']
            destinations_dict[caption] = destination_id
    except (requests.exceptions.ReadTimeout, IndexError) as exception:
        logger.info(f"Can't find destination for {destination}: {exception}")
    finally:
        return destinations_dict


@logger.catch
def output_hotels(destination_id: int, page_number: str, hotels_number: str, check_in: str, check_out: str,
                  price_min: int or None, price_max: int or None, sort_order: str) -> Iterable[dict]:
    pass


@logger.catch
def output_photos(hotel_id: int, photos_number: int) -> Iterable[str]:
    pass


@logger.catch
def output_lowprice_highprice(user_id: int) -> Iterable or None:
    """ Функция вывода информации о запрошенных отелях с фотографиями"""

    city_id = get_user_info(column='city_id', user_id=user_id)
    hotels_amount = get_user_info(column='hotels_amount', user_id=user_id)
    check_in = get_user_info(column='check_in', user_id=user_id)
    check_out = get_user_info(column='check_out', user_id=user_id)
    photos_amount = get_user_info(column='photos_amount', user_id=user_id)
    command = get_user_info(column='command', user_id=user_id)
    if command == '/lowprice':
        sort_order = 'Low price'
    else:
        sort_order = 'High price'
    hotels = output_hotels(destination_id=city_id, page_number='1', hotels_number=hotels_amount, check_in=check_in,
                           check_out=check_out, price_min=None, price_max=None, sort_order=sort_order)
    if hotels is None:
        return None
    for index, hotel in enumerate(hotels):
        text = f"{index}: {hotel['hotel_name']}\nРейтинг: {hotel['rating']}\n " \
               f"Адрес: {hotel['country']}, {hotel['locality']}, {hotel['street']}, {hotel['postel_code']}\n" \
               f"Расстояние до центра: {hotel['downtown_distance']}\n" \
               f"Цена {hotel['price_info']}: {hotel['price']}$\n" \
               f"Ссылка: {hotel['url']}"
        photos = list()
        if photos_amount != 0:
            photos_url = output_photos(hotel_id=hotel['hotel_id'], photos_number=photos_amount)
            for photo_url in photos_url:
                photos.append(InputMediaPhoto(photo_url))
        yield hotel['hotel_name'], text, photos


@logger.catch
def output_bestdeal(message: types.Message) -> dict:
    pass