import telebot
from GoldToken import keys, TOKEN
from Extensions import APIException, CryConvert

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def Drago_help(message: telebot.types.Message):
    text = 'Для начала работы введите команду боту в следующем формате: \n <Имя валюты> \
<В какую валюту перевести> \
<Количество переводимой валюты> \n Увидеть список доступных для конвертации валют: /values'

    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def Drago_values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def Drago_convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Ошибка. Введено слишком много параметров!')

        base, quote, amount = values
        total_quote = CryConvert.get_price(base, quote, amount)
        total_res = (float(total_quote)*int(amount))
    except APIException as u:
        bot.reply_to(message, f'Ошибка пользователя при вводе данных. \n {u}')
    except Exception as e:
        bot.reply_to(message, f'Не вышло обработать команду.\n {e}')
    else:
        text = f'Цена {amount} {base} в валюте {quote} равна {total_res}'
        bot.send_message(message.chat.id, text)

bot.polling()
