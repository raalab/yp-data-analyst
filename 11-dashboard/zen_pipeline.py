#!/usr/bin/python
# -*- coding: utf-8 -*-

#/home/test_user/code/zen_pipeline.py

# Импорт библиотек
import sys
import getopt
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine

# Параметры подключения к БД
db_config = {'user': 'my_user',         # имя пользователя
             'pwd': 'my_user_password', # пароль
             'host': 'localhost',       # адрес сервера
             'port': 5432,              # порт подключения
             'db': 'zen'}               # название базы данных

# Строка соединения с БД
connection_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_config['user'],
                                                        db_config['pwd'],
                                                        db_config['host'],
                                                        db_config['port'],
                                                        db_config['db'])

# Функция для ввода из строки времени начала и конца выборки
def sdt_edt():
    unixOptions = "s:e"
    gnuOptions = ["start_dt=", "end_dt="]
    
    fullCmdArguments = sys.argv
    argumentList = fullCmdArguments[1:] #excluding script name
    
    try:
        arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
    except getopt.error as err:
        print (str(err))
        sys.exit(2)
    
    start_dt = ''
    end_dt = ''
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-s", "--start_dt"):
            start_dt = currentValue
        elif currentArgument in ("-e", "--end_dt"):
            end_dt = currentValue
    return (start_dt, end_dt)


# Основная обработка
if __name__ == "__main__":

    # ввод из командной строки временных границ среза: начала и конца
    
    start_dt, end_dt = sdt_edt()

    # Подключаемся к БД.
    engine = create_engine(connection_string)

    # Выполняем запрос и сохраняем результат
    # выполнения в DataFrame

	# Формируем sql-запрос
    query = '''SELECT *
        FROM log_raw 
        WHERE TO_TIMESTAMP(ts / 1000) AT TIME ZONE 'Etc/UTC' BETWEEN '{}'::TIMESTAMP AND '{}'::TIMESTAMP 
        '''.format(start_dt, end_dt)
    
    data_raw = pd.io.sql.read_sql(query, con = engine, index_col = 'record_id')

    # Преобразуем данные к нужным типам.
    data_raw['dt'] = pd.to_datetime(data_raw['ts']/1000, unit='s').dt.round('min')
   
    # Готовим агрегирующие таблицы
    df_dash_visits =  (data_raw.groupby(['item_topic', 'source_topic', 'age_segment', 'dt'])
                            .agg({'user_id':'count'}).fillna(0).reset_index())

    df_dash_engagement = (data_raw.groupby(['dt', 'item_topic', 'event', 'age_segment'])
                              .agg({'user_id':'nunique'}).fillna(0).reset_index())

    # Переименовываем столбцы датафрейма так,
    # чтобы их имена совпадали с колонками в БД.
    # Это поможет sqlalchemy записать данные автоматически.
    df_dash_visits = df_dash_visits.rename(columns = {'user_id':'visits'})
    df_dash_engagement = df_dash_engagement.rename(columns = {'user_id':'unique_users'})

     

    # Список соответствия таблиц БД и датафреймов 
    tables = {'dash_visits': df_dash_visits, 
              'dash_engagement': df_dash_engagement}

    # Удаление старых записей между start_dt и end_dt и добавление данных в таблицах БД 
    for table_name, table_data in tables.items():   
        query = '''
                  DELETE FROM {} WHERE dt BETWEEN '{}'::TIMESTAMP AND '{}'::TIMESTAMP
                '''.format(table_name, start_dt, end_dt)
        engine.execute(query)

        table_data.to_sql(name = table_name, con = engine, if_exists = 'append', index = False)

    print('Дело сделано.', datetime.now().strftime("%d-%m-%Y %H:%M"))