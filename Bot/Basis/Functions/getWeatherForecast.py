import requests
from bs4 import BeautifulSoup


def getWeather():
    url = 'https://weather.com/ru-RU/weather/today/l/RSXX0091:1:RS'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="lxml")

    # погода текущая
    weatherNow = soup.find('div', attrs={'class': ['today_nowcard-main'], 'style': ''})
    city = weatherNow.find('span').text
    weather = city + '\n\n'
    temp = weatherNow.find('div', attrs={'class': ['today_nowcard-temp']}).text
    phrase = weatherNow.find('div', attrs={'class': ['today_nowcard-phrase']}).text
    weather += 'Сейчас: ' + temp + ' ' + phrase + '\n'
    feels = weatherNow.find('div', attrs={'class': ['today_nowcard-feels']}).text
    weather += feels + '\n'
    hilo = weatherNow.find('div', attrs={'class': ['today_nowcard-hilo']}).text
    hilo = hilo[:hilo.find('УФ-индекс')]
    sidecar = soup.find('div', attrs={'class': ['today_nowcard-sidecar']})
    humidity = sidecar.find_all('tr')[1]
    humidity = humidity.find('th').text + ': ' + humidity.find('td').text
    weather += humidity + '\n'
    weather += hilo + '\n\n'

    todayDaypart = soup.find('div', attrs={'class': ['today-daypart-content'], 'style': ''})
    todayDaypartTop = todayDaypart.find('div', attrs={'class': ['today-daypart-top'], 'style': ''}).find_all('span')
    weather += todayDaypartTop[0].text + ':\n' + todayDaypartTop[1].text + '. '
    todayDaypartHilo = soup.find('div', attrs={'class': ['today-daypart-hilo'], 'style': ''}).text
    todayDaypartTemp = soup.find('div', attrs={'class': ['today-daypart-temp'], 'style': ''}).text
    weather += todayDaypartHilo + ' ' + todayDaypartTemp + '\n'
    precipVal = soup.find('span', attrs={'class': ['precip-val'], 'style': ''}).text
    weather += 'Вероятность осадков: ' + precipVal

    return weather
