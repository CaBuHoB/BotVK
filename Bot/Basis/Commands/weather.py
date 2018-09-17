# -*- coding: utf-8 -*-
from Bot.Basis import command_system
import json
import urllib.parse
import urllib.request

from Bot.Basis.Keyboards.getButtons import get_default_buttons


def weather(values):
    translator = {
        # дни недели
        'Mon': 'Пн',
        'Tue': 'Вт',
        'Wed': 'Ср',
        'Thu': 'Чт',
        'Fri': 'Пт',
        'Sat': 'Сб',
        'Sun': 'Вс',

        # месяцы
        'Jan': 'Января',
        'Feb': 'Февраля',
        'Mar': 'Марта',
        'Apr': 'Апреля',
        'May': 'Мая',
        'Jun': 'Июня',
        'Jul': 'Июля',
        'Aug': 'Августа',
        'Sep': 'Сентября',
        'Oct': 'Октября',
        'Nov': 'Ноября',
        'Dec': 'Декабря',

        # состояния
        'tornado': 'Торнадо',
        'tropical storm': 'Тропическая буря',
        'hurricane': 'Ураган',
        'severe thunderstorms': 'Сильные грозы',
        'thunderstorms': 'Гроза',
        'mixed rain and snow': 'Смешанный снег и снег',
        'mixed rain and sleet': 'Смешанный снег и снег',
        'mixed snow and sleet': 'Смешанный снег и снег',
        'freezing drizzle': 'Изморозь',
        'drizzle': 'Изморось',
        'freezing rain': 'Ледяной дождь',
        'showers': 'Ливни',
        'snow flurries': 'Порывы снега',
        'light snow showers': 'Легкий снежный дождь',
        'blowing snow': 'Низовая метель',
        'snow': 'Снег',
        'hail': 'Град',
        'sleet': 'Дождь со снегом',
        'dust': 'Пыль',
        'foggy': 'Туман',
        'haze': 'Мгла',
        'smoky': 'Дымчато',
        'blustery': 'Бушующий',
        'windy': 'Ветрено',
        'cold': 'Холодно',
        'cloudy': 'Облачно',
        'mostly cloudy (night)': 'Облачно (ночь)',
        'mostly cloudy (day)': 'Облачно (день)',
        'partly cloudy (night)': 'Облачно (ночь)',
        'partly cloudy (day)': 'Облачно (день)',
        'clear (night)': 'Ясная ночь',
        'sunny': 'Солнечно',
        'fair (night)': 'Ясно (ночь)',
        'fair (day)': 'Ясно (день)',
        'mixed rain and hail': 'Смешанный дождь и град',
        'hot': 'Жара',
        'isolated thunderstorms': 'Изолированные грозы',
        'scattered thunderstorms': 'Рассеянные грозы',
        'scattered showers': 'Разбросанные ливни',
        'heavy snow': 'Снегопад',
        'scattered snow showers': 'Разбросанные снежные ливни',
        'partly cloudy': 'Переменная облачность',
        'thundershowers': 'Гроза',
        'snow showers': 'Снегопады',
        'isolated thundershowers': 'Изолированные грозы',
        'not available': '',
        'breezy': 'Свежо'
    }

    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = "select * from weather.forecast where woeid=2123260 and u='C'"
    yql_url = baseurl + urllib.parse.urlencode({'q': yql_query}) + "&format=json"
    result = urllib.request.urlopen(yql_url).read()
    data = json.loads(result)['query']['results']['channel']

    # погода сейчас
    date = data['lastBuildDate'].split()
    date[0] = translator[date[0][:-1]] + ','
    date[2] = translator[date[2]]
    message = ' '.join(date) + '\n'
    message += 'Санкт-Петербург, Россия\n'
    message += 'Состояние: ' + data['item']['condition']['temp'] + ' C° '
    if translator.get(data['item']['condition']['text'].lower()) is not None:
        message += translator[data['item']['condition']['text'].lower()]
    message += '\nВосход: ' + data['astronomy']['sunrise'] + ' \n' + 'Закат: ' + data['astronomy']['sunset']
    return message, None, get_default_buttons(values)


command = command_system.Command()

command.keys = ['погода']
command.description = 'Возвращается прогноз погоды в СПб'
command.process = weather
