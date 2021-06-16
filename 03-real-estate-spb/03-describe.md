#Исследование объявлений о продаже квартир в г.Санкт-Петербург

##Описание проекта
В распоряжении имеются данные сервиса Яндекс.Недвижимость — архив объявлений о продаже квартир в Санкт-Петербурге за несколько лет. Требуется научиться определять рыночную стоимость объектов недвижимости,  установить параметры для построения автоматизированной системы, отслеживающей аномалии и мошеннические действия.

##Вопросы для исследования:
•	Каковы типичные параметры продаваемых квартир (например, площадь, цена)?  Сколько обычно длится процесс продажи?
•	Убрать квартиры с очень высокой ценой и другими необычными параметрами. Описать, какие особенности обнаружены.
•	Какие факторы больше всего влияют на стоимость квартиры? 
Зависит ли цена квадратного метра: от числа комнат, этажа (первого или последнего), удалённости от центра и даты размещения: дня недели, месяца и года.
•	Что можно сказать о цене квадратного метра в пригородах? 
•	Выделить сегменты типичных квартир в центре (по удалённости, числу комнат и площади) и вне центра. 
•	Подобрать наиболее характерные параметры для апартаментов, студий и квартир свободной планировки. Влияют ли они на цену? Сравнить со схожими параметрами квартир типовой планировки.

##Источник данных:
Сервис Яндекс.Недвижимость — архив объявлений о продаже квартир в Санкт-Петербурге за несколько лет,
файл со статистикой: /datasets/real_estate_data.csv
***
По каждой продаваемой квартире есть два вида данных. 
Первые — вносили сами пользователи при публикации объявлений, вторые — получены на основе картографических данных: расстояния до центра, аэропорта, ближайшего парка и водоёма.

## Использованные библиотеки Python:
pandas
numpy
matplotlib.pyplot