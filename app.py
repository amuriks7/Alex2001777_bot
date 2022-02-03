from flask import Flask, request
import telebot, wikipedia, re
import os

app = Flask(__name__)
TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)
wikipedia.set_lang("ru")


def getwiki(s):
    try:
        ny = wikipedia.page(s)
        wikitext = ny.content[:1000]
        wikimas = wikitext.split('.')
        wikimas = wikimas[:-1]
        wikitext_2 = ''
        for x in wikimas:
            if not ('==' in x):
                if (len(x.strip()) > 3):
                    wikitext_2 = wikitext_2 + x + '.'
                else:
                    break
        wikitext_2 = re.sub('\([^()]*\)', '', wikitext_2)
        wikitext_2 = re.sub('\([^()]*\)', '', wikitext_2)
        wikitext_2 = re.sub('\{[^\{\}]*\}', '', wikitext_2)
        return wikitext_2
    except Exception as e:
        return 'В энциклопедии нет информации об этом'


@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Отправьте мне любое слово, и я найду его значение на Wikipedia')


@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, getwiki(message.text))


bot.polling(none_stop=True, interval=0)


@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_messages([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return 'Python Telegram Bot 03.02.2022', 200


@app.route('/')
def main():
    bot.remove_webhook()
    bot.set_webhook(url='....' + TOKEN)
    return 'Python Telegram Bot', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
