#!/usr/bin/python
# -*- coding: utf-8 -*-

#/home/test_user/code/zen_dash.py
# Построение дашборда

# импорт библиотек

import pandas as pd
import numpy as np
from datetime import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from sqlalchemy import create_engine

# #########################
# # Работа в режиме отладки 
# # Загрузка данных из тестовой выборки df_raw.csv
# data_raw = pd.read_csv('df_raw.csv')
# data_raw['ts'] = pd.to_datetime(data_raw['ts']/1000, unit='s').dt.round('min')
# data_raw = data_raw.rename(columns={'ts':'dt'})

# # Готовим агрегирующие таблицы
# df_dash_visits =  (data_raw.groupby(['item_topic', 'source_topic', 'age_segment', 'dt'])
#                             .agg({'event_id':'count'}).fillna(0).reset_index())
# df_dash_visits = df_dash_visits.rename(columns = {'event_id':'visits'})

# df_dash_engagement = (data_raw.groupby(['dt', 'item_topic', 'event', 'age_segment'])
#                               .agg({'user_id':'nunique'}).fillna(0).reset_index())
# df_dash_engagement = df_dash_engagement.rename(columns = {'user_id':'unique_users'})
# #########################

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


# выгружаем данные из таблиц 
if __name__ == "__main__":
    # Подключаемся к БД.
    engine = create_engine(connection_string)
    # Выполняем запрос и сохраняем результат
    # выполнения в DataFrame
    # Формируем sql-запрос
    df_dash_visits = pd.io.sql.read_sql('SELECT * FROM dash_visits',
                                        con = engine, index_col = 'record_id')
    df_dash_engagement = pd.io.sql.read_sql('SELECT * FROM dash_engagement',
                                        con = engine, index_col = 'record_id')
    # Преобразуем данные к нужным типам.
    # (дублирование обработки, для надежности)
    df_dash_visits['dt'] = pd.to_datetime(df_dash_visits['dt']).dt.round('min')
    df_dash_engagement['dt'] = pd.to_datetime(df_dash_engagement['dt']).dt.round('min')


# Разметка Дашборда
note = '''
          Этот дашборд показывает взаимодействие пользователей по темам карточек и источников.
          Используйте выбор интервала даты-времени, возрастной категории и тем карточек для управления дашбордом.
          Используйте селектор выбора режима отображения для того, чтобы показать среднюю глубину взаимодействия 
          пользователей в формате столбчатой диаграммы или "воронки продаж".
       '''

# задаём лейаут
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, compress=False)

# настройка цветов элементов дашборда
colors = {
    'background': '#FFFFFF',
    'text': '#navy'
}


app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[  
    
    # формируем html
    html.H1(children = 'Взаимодействие пользователей с карточками', style={'color':'Navy'}),
    html.H1(children = 'Яндекс.Дзен', style={'color':'Red'}),
    html.Br(),  

    # пояснения
    html.Label(note), 
    html.Br(),  
    
    # установка фильтров
    html.Div([  

        html.Div([
            html.Div([
            # выбор временного периода
            html.Label('Временной интервал:', ),
            dcc.DatePickerRange(
                start_date = df_dash_visits['dt'].dt.date.min(),
                end_date = df_dash_visits['dt'].dt.date.min() + pd.Timedelta(1, 'days'),
                display_format = 'YYYY-MM-DD',
                id = 'dt_selector',       
            ),
                ]),

            html.Div([    
            # выбор возростной группы
            html.Label('Возрастные группы:'),
            dcc.Dropdown(
                options = [{'label': x, 'value': x} for x in df_dash_visits['age_segment'].unique()],
                value = df_dash_visits['age_segment'].unique().tolist(),
                multi = True,
                id = 'age_selector'
                    ),                   
                    ]), 
             
                ], className = 'six columns'),
        

        html.Div([         
            # выбор карточек по темам
            html.Label('Выбор карточек по темам'),
            dcc.Dropdown(
                options = [{'label': x, 'value': x} for x in df_dash_visits['item_topic'].unique()],
                value = df_dash_visits['item_topic'].unique().tolist(),
                multi = True,
                id = 'item_selector'
            ),                
        ], className = 'six columns'),

    ], className = 'row'), 

    html.Br(),     
    
    # вывод графиков
    html.Div([
        html.Div([

            # график истории событий по темам карточек
            html.Label('История событий по темам карточек'),    

             
            dcc.Graph(
                style = {'height':'50vw'},
                id = 'data_by_item_topic'
            ),  
        ], className = 'six columns'),            

         html.Div([

            # График разбивки событий по темам источников
            html.Label('Разбивка событий по темам источников'),    

             
            dcc.Graph(
                style = {'height':'25vw'},
                id = 'data_by_source'
            ),  
        ], className = 'six columns'),            
        
        html.Div([

            # график глубины взаимодействия пользователей
            html.Label('Глубина взаимодействия пользователей'),    
        
            dcc.RadioItems(
                options = [
                    {'label': 'Столбцы', 'value': 'bar'},
                    {'label': 'Воронка', 'value': 'funnel'},
                ],
                value = 'bar',
                id = 'mode_selector'
            ),
            
            dcc.Graph(
                style = {'height':'25vw'},
                id = 'data_by_event'
            ),  
        ], className = 'six columns'),            

                
    ], className = 'row'),  

])

# логика дашборда
@app.callback(
    [Output('data_by_item_topic', 'figure'),
     Output('data_by_source', 'figure'),
     Output('data_by_event', 'figure')
],
    [Input('dt_selector', 'start_date'),
     Input('dt_selector', 'end_date'),
     Input('age_selector', 'value'),
     Input('item_selector', 'value'),
     Input('mode_selector', 'value')
])

# подготовка данных для графиков
def update_figures(start_date, end_date, selected_age_segment, selected_item_topic, selected_mode):

    #тестовые параметры
    # start_time = start_date
    # end_time = end_date
    # selected_age_segment = selected_age_segment
    # selected_item_topic = selected_item_topic
    # selected_mode = selected_mode
    
    #приводим входные параметры к нужным типам
    start_time = datetime.strptime(start_date, '%Y-%m-%d')
    end_time = datetime.strptime(end_date, '%Y-%m-%d')
   
    
    #применяем фильтрацию
    filter_time = 'dt >= @start_time and dt <= @end_time'
    filter_age_segment = 'age_segment in @selected_age_segment'
    filter_item_topic = 'item_topic in @selected_item_topic'

    
           
    # График истории событий по темам карточек
    df_dash_visits_filtered = (
                                df_dash_visits.query(filter_time ).query(filter_age_segment).query(filter_item_topic)
                                              .groupby(['dt', 'item_topic'])['visits'].sum().reset_index()
                              )
  
    data_by_item_topic = []
    for item_topic in df_dash_visits['item_topic'].unique():
        data_by_item_topic += [go.Scatter(x = df_dash_visits_filtered.query('item_topic == @item_topic')['dt'],
                                          y = df_dash_visits_filtered.query('item_topic == @item_topic')['visits'],
                                             mode = 'lines',
                                             stackgroup = 'one',
                                             name = item_topic)]
        
    # График разбивки событий по темам источников
    df_dash_source_filtered = (
                                df_dash_visits.query(filter_time ).query(filter_age_segment).query(filter_item_topic)
                                              .groupby(['dt', 'source_topic'])['visits'].sum().reset_index()
                              )
    
    data_by_source = [go.Pie(labels = df_dash_source_filtered['source_topic'],
                                           values = df_dash_source_filtered['visits'],
                                           name = 'source_topic')]            

    
    # График глубины взаимодействия пользователей
    df_dash_engagement_filtered = (df_dash_engagement.query(filter_time ).query(filter_age_segment).query(filter_item_topic)
                                  .groupby(['event'])['unique_users'].mean().reset_index()
                                  )
    df_dash_engagement_filtered = (df_dash_engagement_filtered.rename(columns={'unique_users':'avg_unique_users'})
                                  .sort_values(by='avg_unique_users', ascending=False)
                                  )
    
    # трансформируем в соотв. с выбранным режимом отображения
    if selected_mode == 'bar':
        data_by_event = [go.Bar(x = df_dash_engagement_filtered['event'],
                               y = df_dash_engagement_filtered['avg_unique_users'],
                               text = np.round(df_dash_engagement_filtered['avg_unique_users'], 2), textposition='auto',
                               marker_color='LawnGreen', marker_line_color='Teal', marker_line_width=1, opacity=0.6)]
    else:    
        data_by_event = [go.Funnel( x = list(np.round(df_dash_engagement_filtered['avg_unique_users'] 
                                          / df_dash_engagement_filtered['avg_unique_users'].sum()*100, 2)),
                                   y = list(df_dash_engagement_filtered['event']),
                                   marker_color='LawnGreen', marker_line_color='Teal', marker_line_width=1, opacity=0.6)]


    #формирование результата для отображения
    return (
                    {
                        'data': data_by_item_topic,
                        'layout': go.Layout(xaxis = {'title': 'Время'},
                                            yaxis = {'title': 'Число просмотров карточки'})
                    },
                    {
                        'data': data_by_source,
                        'layout': go.Layout(xaxis = {'title': 'Время'},
                                            yaxis = {'title': 'Тема источника'},
                                            barmode = 'stack',
                                           )
                    },             
                    {
                        'data': data_by_event,
                        'layout': go.Layout()
                    },
             )  


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
