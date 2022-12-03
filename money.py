from bs4 import BeautifulSoup
import requests


base = 'https://www.banki.ru/products/currency/cb/'
html = requests.get(base)
soup = BeautifulSoup(html.text, 'lxml')
table = soup.find('table', class_='standard-table standard-table--row-highlight')
tr = table.find_all('td')


en_names = []
amount = []
ru_names = []
curs_ = []


for _ in tr[::5]:
    en_names.append(_.get_text(strip=True))

for _ in tr[2::5]:
    ru_names.append(_.get_text(strip=True))

for _ in tr[3::5]:
    curs_.append(_.get_text(strip=True))

for _ in tr[1::5]:
    amount.append(_.get_text(strip=True))

money = dict(zip(en_names, zip(amount, zip(ru_names, curs_))))
money['RUB'] = ('1', ('Российский рубль', '1'))


class BotExceptions(Exception):
    pass


class TextException(BotExceptions):
    pass


class ConvertionException(BotExceptions):
    pass

class ValueConverter:
    @staticmethod
    def converter(base: str, quote: str, amount: str):
        rub = float(money[base][1][1]) / float(money[base][0]) * float(amount)
        if base == quote:
            raise ConvertionException(f'Как перевести {base} в {quote}?')
        elif quote == 'RUB':
            total = rub
            return total
        elif quote in money.keys() and base in money.keys():
            rub2 = float(money[quote][1][1]) / float(money[quote][0])
            total = rub / rub2
            return total
        else:
            raise TextException('Не верный формат ввода')


