import telebot
from config import keys, TOKEN
from extensions import Exxe, Currencies

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Я — бот для конвертации валют, и я могу:\n 🗃️ дать список доступных валют по запросу /values\n \
🧮 конвертировать по запросу формата\n <сколько_надо> <интересующая_валюта> <валюта_расчёта>'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = '💸 Доступны валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise Exxe('Введённые параметры неверны...\nПример запроса:  100 рубль вона')

        amount, base, quote = values
        total_quote = Currencies.get_price(amount, base, quote)
    except Exxe as e:
        bot.reply_to(message, f'⚠️ {e}')
    except Exception as e:
        bot.reply_to(message, f'⛔ Ошибка сервера ⛔\n{e}')

    else:
        text = f'💱 {amount} {base} = {total_quote} {quote}'
        bot.send_message(message.chat.id, text)


bot.polling()
