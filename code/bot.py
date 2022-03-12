import os
import random

import telebot
import json

from requests import get

subs = []
pending_subs = []
# pendingTorrent = [False]

pendingTorrent = False


def cache_subs(a):
    json_note = ""
    if len(a) != 0:
        print("Записываю подписчиков в файл")
        json_note = json.dumps(a)
    file = open("/app/volume/subs.json", "w")
    file.write(json_note)
    file.close()


def read_cache_subs(a):
    try:
        file = open("/app/volume/subs.json", "r")
        json_note = file.read()
        print("Подписчики: " + json_note)
        if len(json_note) > 0:
            for i in json.loads(json_note):
                a.append(i)
            print(a)
    except:
        file = open("/app/volume/subs.json", "w")
        file.write("")
        file.close()


read_cache_subs(subs)
# print(subs)

bot = telebot.TeleBot(os.environ.get("TELEGRAM_KEY"))


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.from_user.id, """/help  - Помощь
/sub   - Подписаться
/subs  - Список подписанных пользователей
/ip    - Получить текущий IP сервера""")


@bot.message_handler(commands=['subs'])
def handle_subs(message):
    if message.from_user.id in subs:
        subs_string = ""
        for i in subs:
            UsrInfo = bot.get_chat_member(i, i).user
            subs_string += str(i) + " - " + UsrInfo.username + "\n"
        bot.send_message(message.from_user.id, subs_string)
    else:
        bot.send_message(message.from_user.id, "Вы не являетесь подписчиком")


@bot.message_handler(commands=['ip'])
def handle_ip(message):
    if message.from_user.id in subs:
        ip = get('https://api.ipify.org').text
        bot.send_message(message.from_user.id, "Текущий IP сервера:")
        bot.send_message(message.from_user.id, ip)
    else:
        bot.send_message(message.from_user.id, "Вы не являетесь подписчиком")


@bot.message_handler(content_types=['document'])
def handle_docs_audio(message):
    file_id = message.document.file_id
    file_info = bot.get_file(file_id)
    file = get('https://api.telegram.org/file/bot{0}/{1}'.format(os.environ.get("TELEGRAM_KEY"), file_info.file_path))

    savedFile = open('/app/torrent/' + message.document.file_name, 'wb')
    savedFile.write(file.content)
    savedFile.close()
    bot.send_message(message.from_user.id, "Сохранён файл " + message.document.file_name)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    # read_cache_subs()
    print(message.text)
    if message.text.upper() == "ПРИВЕТ":
        bot.send_message(message.from_user.id, "Ohaio")

    elif message.text == "/download":
        if message.from_user.id in subs:
            # pendingTorrent[0] = True
            global pendingTorrent
            pendingTorrent = True
            bot.send_message(message.from_user.id, "Отправьте торрент файл или magnet ссылку")
        else:
            bot.send_message(message.from_user.id, "Вы не являетесь подписчиком")

    elif message.text == os.environ.get("ADMIN_PASSWORD"):
        if message.from_user.id in pending_subs or not (message.from_user.id in subs):
            subs.append(message.from_user.id)
            if message.from_user.id in pending_subs:
                pending_subs.remove(message.from_user.id)
            bot.send_message(message.from_user.id, "Вы успешно подписаны на обновления")
            cache_subs(subs)

    elif "magnet" in message.text:
        if message.from_user.id in subs:
            filename = random.randint(1, 500)
            file = open("/app/torrent/" + str(filename) + ".magnet", "w")
            file.write(message.text)
            file.close()
            bot.send_message(message.from_user.id, "Файл: " + str(filename) + ".magnet")

    else:
        bot.send_message(message.from_user.id, "Не понимаю")


bot.infinity_polling()

# bot.polling(none_stop=True, interval=0)
# magnet:?xt=urn:btih:F38AD02AF844868888B4C37AB1FFC112DAE80F1D&tr=http%3A%2F%2Fbt.t-ru.org%2Fann%3Fmagnet&dn=Восемьдесят%20шесть%202%20(ТВ-1%2C%20часть%202)%20%2F%2086%20Part%202%20%2F%20Eighty%20Six%202nd%20Season%20%5BTV%2BSpecial%5D%20%5B1-10%2B2%20из%20%3E11%2B2%5D%20%5BБез%20хардсаба%5D%20%5BJAP%2BSub%5D%20%5B2021%2C%20экшен%2C%20драма%2C%20ф
