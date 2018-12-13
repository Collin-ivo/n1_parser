#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -- author: Nikolay Ivanov --

import requests, time, csv
from bs4 import BeautifulSoup as bs


payload = {
    'rubric': 'flats',
    'deal_type': 'sell',
    'limit': '100',
    'district': '1306589%2C1306590',
    'rooms': '2',
    'is_newbuilding': 'False',
    'floor_not_first': 'True',
    'floor_not_last': 'True',
    'has_balcony': 'True',
    'page': '1'
}

def pars_data(url, page=1, district='1306589'):
    payload = {
        'rubric': 'flats',
        'deal_type': 'sell',
        'limit': '100',
        'district': district,
        'rooms': '2',
        'is_newbuilding': 'False',
        'floor_not_first': 'True',
        'floor_not_last': 'True',
        'has_balcony': 'True',
        'page': page
    }
    response = requests.get(url, params = payload).text
    soup = bs(response, features="lxml")
    search_result = soup.find('div', {'class': 'search-content__results'})
    find_items = search_result.find_all('div', {'class': 'living-list-card'})

    results = []
    for item in find_items:
        room_link = ('https://n1.ru{}'.format(item.find('div', {'class': 'living-list-card__title'}).find('a').get('href')))
        room_adress = item.find('span', {'class': 'living-list-card-title__text'}).text
        room_district = item.find('div', {'class': 'search-item-district'}).text
        room_city = item.find('span', {'class': 'living-list-card-city-with-estate__item'}).text
        room_size = item.find('div', {'class': 'living-list-card__area'}).text
        room_price = item.find('div', {'class': 'living-list-card-price__item _object'}).text

        to_skip = False
        for room in results:
            if room_link == room.get('ссылка'):
                print('Это объявление уже есть')
                to_skip = True
                break
        if to_skip:
            continue
        date_of_publication = bs(requests.get(room_link).text, features="lxml").find('p', {'class': 'card-living-content__state'}).text

        item_data = {
            'ссылка': room_link,
            'адрес': room_adress,
            'район': room_district,
            'город': room_city,
            'площадь': room_size,
            'цена': room_price,
            'дата публикации': date_of_publication[36:]
                    }
        print(item_data)
        results.append(item_data)

    if len(find_items) != 0:
        page += 1
        time.sleep(1)
        results.extend(pars_data(url, page, district))
    return results

def save_to_data_csv(input_results):
    data_list = []
    for dict in input_results:
        data_list.append(list(dict.values()))
    print(data_list)
    with open('data.csv', 'w') as data_csv:
        pass


def send_new_links(links):
    pass

if __name__ == "__main__":
    save_to_data_csv([{'1': 'foo', '2': 'baar'}, {'4': 'brrr', '5': 'aaaa'}])
    parsed_links = pars_data('https://arhangelsk.n1.ru/search/', 1, district='1306589')
    print(len(parsed_links))
    parsed_links_2 = pars_data('https://arhangelsk.n1.ru/search/', 1, district='1306590')
    print(len(parsed_links_2))

    to_save_data = parsed_links.extend(parsed_links_2)
