#!/usr/bin/python
# -*- coding: utf-8 -*-

#import psycopg2
#import sys
#import getopt
from sqlalchemy import create_engine


# Задаём параметры подключения к БД,
# их можно узнать у администратора БД.
db_config = {'user': 'my_user',         # имя пользователя
             'pwd': 'my_user_password', # пароль
             'host': 'localhost',       # адрес сервера
             'port': 5432,              # порт подключения
             'db': 'zen'}             # название базы данных

# Формируем строку соединения с БД.
connection_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_config['user'],
                                                        db_config['pwd'],
                                                        db_config['host'],
                                                        db_config['port'],
                                                        db_config['db']) 
 
def create_tables():
# """ создание таблиц PostgreSQL database"""
    # команды SQL по созданию двух доп. таблиц в базе
    commands = (
        """
        CREATE TABLE dash_engagement (
            record_id SERIAL PRIMARY KEY,
            dt TIMESTAMP NOT NULL,
            item_topic VARCHAR(128),
            event VARCHAR(128),
            age_segment VARCHAR(128),
            unique_users BIGINT );
        """,

        """ 
        CREATE TABLE dash_visits (
            record_id SERIAL PRIMARY KEY,
            dt TIMESTAMP,
            item_topic VARCHAR(128),
            source_topic VARCHAR(128),
            age_segment VARCHAR(128),
            visits INT); 
        """
        )
    
    # подключение к базе и выполнение операций
    try:
       
        # соединение с сервером PostgreSQL
        engine = create_engine(connection_string)
        # create tables
        engine.execute(commands)
    
    except:
        print(error)
    
if __name__ == '__main__':
    create_tables()