#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -- author: Nikolay Ivanov --

import requests, time, csv
from bs4 import BeautifulSoup as bs
import smtplib
from email.mime.text import MIMEText

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

    existing_data = []
    with open('data.csv', 'r', encoding='utf-8') as data_csv:
        fieldnames = ['ссылка', 'адрес', 'район', 'город', 'площадь', 'цена', 'дата публикации']
        reader = csv.DictReader(data_csv, delimiter=';', fieldnames=fieldnames)
        for line in reader:
            existing_data.append(line['ссылка'])
    existing_data.remove('ссылка')
    existing_data = set(existing_data)
    print(existing_data)

    results = []
    for item in find_items:
        room_link = ('https://n1.ru{}'.format(item.find('div', {'class': 'living-list-card__title'}).find('a').get('href')))
        room_adress = item.find('span', {'class': 'living-list-card-title__text'}).text
        room_district = item.find('div', {'class': 'search-item-district'}).text
        room_city = item.find('span', {'class': 'living-list-card-city-with-estate__item'}).text
        room_size = item.find('div', {'class': 'living-list-card__area'}).text
        room_price = item.find('div', {'class': 'living-list-card-price__item _object'}).text

        room_link_locale_set = set([room_link])
        print(room_link_locale_set)
        if not existing_data.isdisjoint(room_link_locale_set):
            print('Это объявление уже есть')
            continue

        time.sleep(0.5)
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
    with open('data.csv', 'a', encoding='utf-8', newline='') as csv_file:
        fieldnames = ['ссылка', 'адрес', 'район', 'город', 'площадь', 'цена', 'дата публикации']
        writer = csv.DictWriter(csv_file, delimiter=';', fieldnames=fieldnames)
        for line in input_results:
            writer.writerow(line)

def send_new_links(links):
    sender = ''
    subject = ''
    sender_password = ''
    msg = str(links)
    msg = MIMEText('{}'.format(msg).encode('utf-8'), _charset='utf-8')
    mail_lib = smtplib.SMTP_SSL('smtp.mail.ru', 465)
    mail_lib.login(sender, sender_password)
    mail_lib.sendmail(sender, subject, msg)
    mail_lib.quit()

if __name__ == "__main__":
    parsed_links_1 = pars_data('https://arhangelsk.n1.ru/search/', 1, district='1306589')
    save_to_data_csv(parsed_links_1)
    parsed_links_2 = pars_data('https://arhangelsk.n1.ru/search/', 1, district='1306590')
    save_to_data_csv(parsed_links_2)

    # list_to_send = []
    # list_to_send.append(parsed_links_2)
    # list_to_send.append(parsed_links_1)
    # if len(list_to_send) > 0:
    #     send_new_links(list_to_send)

