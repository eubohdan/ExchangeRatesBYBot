import requests
from bs4 import BeautifulSoup as Bs
from create_bot import redis
from keyboards import cur_types as ct


def refresh_db(city: str, day: str):
    print('Обновление курсов валют')
    r = requests.get('https://myfin.by/currency/' + city + '/' + day)
    soup = Bs(r.content, 'lxml')
    table = soup.find(class_='c-best-rates')
    keys = []
    for i in table.find("thead").findAll("th"):
        keys.append(i.text)
    values = []
    for i in table.find("tbody").findAll("td"):
        values.append(i.text.strip())
    best_usd, best_eur, best_rub, best_pln, best_uah = {}, {}, {}, {}, {}
    for i in range(len(keys)):
        best_usd[keys[i]] = values[i]
        best_eur[keys[i]] = values[i + 5]
        best_rub[keys[i]] = values[i + 10]
        best_pln[keys[i]] = values[i + 15]
        best_uah[keys[i]] = values[i + 20]
    print('Курсы валют обновлены')
    return [best_usd, best_eur, best_rub, best_pln, best_uah]


async def add_to_redis(curr_today: list, curr_yesterday: list):
    cur_types = ['usd', 'eur', 'rub', 'pln', 'uah']
    cur_names = list(ct.keys())
    for i in range(5):
        dif_buy = round(float(curr_today[i]['Покупка']) - float(curr_yesterday[i]['Покупка']), 4)
        dif_sell = round(float(curr_today[i]['Продажа']) - float(curr_yesterday[i]['Продажа']), 4)
        dif_nbrb = round(float(curr_today[i]['НБ РБ']) - float(curr_yesterday[i]['НБ РБ']), 4)
        msg = f"<b>{cur_names[i]}</b>\n\nПокупка: <b>{curr_today[i]['Покупка']}</b> <i>({(f'{dif_buy}', f'+{dif_buy}')[dif_buy > 0]})</i>\n"
        msg += f"Продажа: <b>{curr_today[i]['Продажа']}</b> <i>({(f'{dif_sell}', f'+{dif_sell}')[dif_sell > 0]})</i>\n"
        msg += f"НБ РБ: <b>{curr_today[i]['НБ РБ']}</b> <i>({(f'{dif_nbrb}', f'+{dif_nbrb}')[dif_nbrb > 0]})</i>\n"
        await redis.set(name=f"{cur_types[i]}", value=msg)
