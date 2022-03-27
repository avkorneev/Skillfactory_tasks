import telebot
from extensions import Conv, APIException

f = open('config.txt', 'r')  # config.txt should contain Telegram bot token (and only Telegram bot token)
bot = telebot.TeleBot(f.read())
f.close()


@bot.message_handler(commands=['start', 'help'])  # some comments on bot application
def repeat(message: telebot.types.Message):
    bot.send_message(message.chat.id,
                     '''Hello there! \nI was created to make you compliments! Let's get started! \nAlso I can convert currencies for you! Type /values for more information!\n Or send me some picture 
                         because I'm very bored here :(''')


@bot.message_handler(commands=['values'])
def repeat(message: telebot.types.Message):
    bot.send_message(message.chat.id,
                     f"Hello there! I can convert currencies! Just type <what to convert><to what to convert><how "
                     f"much to convert>\nFor example: USD RUB 300\nAvailable currencies are:{Conv.currency_list()}")


@bot.message_handler(content_types=['text'])  # Facing text, the bot will try to convert currencies
def repeat(message: telebot.types.Message):
    currencies = Conv.currency_list().split(' ')  # It will request list of currencies available
    msg = True  # This counter is needed so that bot would not give usual respond if we're going to convert anything
    for a in currencies:  # This cycle will check whether the message contains any of available currencies
        if message.text.find(a) != -1:  # And if it finds, it will try to reformat message for conversion
            try:
                text = message.text.split(' ')  # space is the separator in selected format
                bot.reply_to(message, Conv.get_price(text[0], text[1], text[2]))  # Calling converting function
            except IndexError:  # This error raises when the order is broken or only one currency found. Like "USD 10"
                bot.reply_to(message,
                             "Looks like you're trying to convert something and requested non-existing currency! Try again?")
                raise APIException("Incorrect format!")
            except ValueError:  # And this one raises when we can't convert amount to number. Like "USD EUR asdf"
                bot.reply_to(message,
                             "Looks like you're trying to convert something and used incorrect amount! Try again?")
                raise APIException("I don't understand, please use correct format!")
            finally:
                msg = False  # Usual respond is not needed
                break  # And no need to check other currencies
    if msg:  # Usual respond
        bot.reply_to(message,
                     f"Welcome, {str(message.chat.first_name) + ' ' + str(message.chat.last_name)}! Glad you're here!")


@bot.message_handler(content_types=['photo'])  # Bonus function responding on pictures :)
def repeat(message: telebot.types.Message):
    bot.send_photo(message.chat.id, open("BobRoss.jpg", 'rb'), 'Nice meme! Send me more XD', None, None, None,
                   None,
                   message.message_id, None, None)


bot.polling(none_stop=True)
