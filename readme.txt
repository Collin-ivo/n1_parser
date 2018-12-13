# Проект парсера

Парсер собирает объявления на сайте n1 и шлет уведомление о новых объявлениях изменение цен избранных объявлений.


https://arhangelsk.n1.ru/search/?rubric=flats&deal_type=sell&district=1306589%2C1306590&rooms=2&is_newbuilding=false&floor_not_first=true&floor_not_last=true&has_balcony=true

params = {
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