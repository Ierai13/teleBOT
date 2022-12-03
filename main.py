import telebot
from money import *
from setup import TOKEN


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Для конвертации валюты отправьте команду /convert в формате:\n' \
           '/convert <что конвертировать> <во что конвертировать> <сколько> \n' \
           '/values - список досдупных валют для конвертации \n' \
           '/today <валюта> - курс выбраной валюты 1 ед. на сегодня в рублях\n' \
           '/today_all - курс всех доступных валют на сегодня в рублях \n' \
           'Используйте обозначения валют в формате: RUB\n' \
           'Для просмотра всех комманд введите /help'
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = '/values - список досдупных валют для конвертации \n' \
           '/convert <что> <во что> <сколько> - конвертация валют \n' \
           '/today <валюта> - курс выбраной валюты на сегодня в рублях\n' \
           '/today_all - курс всех доступных валют на сегодня в рублях\n' \
           'Используйте обозначения валют в формате: RUB'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: \n'
    for key, value in money.items():
        text = '\n'.join((text, key + ' - ' + value[1][0]))
    bot.reply_to(message, text)


@bot.message_handler(commands=['today'])
def today(message: telebot.types.Message):
    try:
        mes = message.text.upper().split()

        if len(mes) == 1:
            raise TextException
        val = mes[1]
        text = f''

        if val in money.keys():
            text += f'Курс {val} ({money.get(val)[1][0]}) на сегодня составляет {money.get(val)[1][1]} руб.'
        else:
            raise TextException
    except BotExceptions:
        bot.send_message(message.chat.id, 'Для получения информации о валюте введите команду \n/today <валюта>\n'
                                          'Список валют: /values')
    else:
        bot.reply_to(message, text)


@bot.message_handler(commands=['today_all'])
def today_all(message: telebot.types.Message):
    text = 'Курсы валют:'
    for key, value in money.items():
        text = '\n'.join((text, f'{value[0]} {key} ({value[1][0]}): {value[1][1]} руб.'))
    bot.reply_to(message, text)


@bot.message_handler(commands=['convert'])
def convert(message: telebot.types.Message):
    val = message.text.upper().split()
    try:
        if len(val) != 4:
            raise TextException('Не верный формат ввода')
        elif not val[3].isdigit():
            raise TextException('Не верный формат ввода')
        base, quote, amount = val[1:]
        total = ValueConverter.converter(base, quote, amount)
    except BotExceptions as e:
        bot.reply_to(message, f'{e}')
        bot.send_message(message.chat.id, 'Для помощи ввода команд напишите /help')
    else:
        bot.reply_to(message, f'{amount} {base} ({money[base][1][0]}) в {quote} ({money[quote][1][0]}) будет\n'
                              f' {round(total, 2)} {quote}')



bot.polling(non_stop=True)
