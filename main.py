#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -- author: Nikolay Ivanov --

import requests, time
from bs4 import BeautifulSoup as bs
from lxml import html

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

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    }
    response = requests.get(url, params=payload)

    list_html= response.text.split(sep='"')
    pars_url = []
    out_url = []
    for item in list_html:
        if item.find('arhangelsk.n1.ru/view/') != -1:
            item_in_out = False
            for string in pars_url:
                if string == item:
                    item_in_out = True
                    break
            if item_in_out == False:
                pars_url.append(item)
    out_url.extend(pars_url)
    print('Скачано ссылок: ' + str(len(pars_url)))
    if len(pars_url) != 0:
        page += 1
        time.sleep(1)
        out_url.extend(pars_data(url, page))
    return(out_url)

def compare_links(file, parsed_links):
    old_links = []
    unicue_links = []
    with open(file, 'r', encoding='utf-8') as opened_file:
        for line in opened_file:
            old_links.append(line)
    for item in parsed_links:
        unic_flag = True
        for old_item in old_links:
            if old_item.find(item) != -1:
                unic_flag = False
        if unic_flag == True:
            unicue_links.append(item)
    with open(file, 'a', encoding='utf-8') as opened_file:
        for item in unicue_links:
            opened_file.write('\n'+item)
    return unicue_links

def send_new_links(links):
    pass

if __name__ == "__main__":
    parsed_links = pars_data('https://arhangelsk.n1.ru/search/', 1, district='1306589')
    new_unicue_links = compare_links('links_n1.txt', parsed_links)
    print(new_unicue_links)

    parsed_links = pars_data('https://arhangelsk.n1.ru/search/', 1, district='1306590                     ')
    new_unicue_links = compare_links('links_n1.txt', parsed_links)
    print(new_unicue_links)