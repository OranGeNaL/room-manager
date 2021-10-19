import os
import telebot
import json

from requests import get
from wakeonlan import send_magic_packet


subs = []
pending_subs = []


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
print(subs)



bot = telebot.TeleBot(os.environ.get("TELEGRAM_KEY"))




@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    # read_cache_subs()
    print(message.text)
    if message.text.upper() == "ПРИВЕТ":
        bot.send_message(message.from_user.id, "Ohaio")

    elif message.text == "/sub":
        if message.from_user.id in pending_subs:
            bot.send_message(message.from_user.id, "Для того, чтобы подписаться, введите пароль администратора")
        elif message.from_user.id in subs:
            bot.send_message(message.from_user.id, "Вы уже подписаны на обновления")
        else:
            bot.send_message(message.from_user.id, "Для того, чтобы подписаться, введите пароль администратора")
            pending_subs.append(message.from_user.id)

    elif message.text == "/subs":
        if message.from_user.id in subs:
            subs_string = ""
            for i in subs:
                UsrInfo = bot.get_chat_member(i, i).user
                subs_string += str(i) + " - " + UsrInfo.username + "\n"
            bot.send_message(message.from_user.id, subs_string)
        else:
            bot.send_message(message.from_user.id, "Вы не являетесь подписчиком")

    elif message.text == "/ip":
        if message.from_user.id in subs:
            ip = get('https://api.ipify.org').text
            bot.send_message(message.from_user.id, "Текущий IP сервера:")
            bot.send_message(message.from_user.id, ip)
        else:
            bot.send_message(message.from_user.id, "Вы не являетесь подписчиком")

    elif message.text == "/help":
        bot.send_message(message.from_user.id, """/help  - Помощь
/sub   - Подписаться
/subs - Список подписанных пользователей
/ip      - Получить текущий IP сервера""")


    elif message.text == os.environ.get("ADMIN_PASSWORD"):
        if message.from_user.id in pending_subs or not(message.from_user.id in subs):
            subs.append(message.from_user.id)
            if message.from_user.id in pending_subs:
                pending_subs.remove(message.from_user.id)
            bot.send_message(message.from_user.id, "Вы успешно подписаны на обновления")
            cache_subs(subs)
        
    else:
        bot.send_message(message.from_user.id, "Не понимаю")


bot.infinity_polling()

# bot.polling(none_stop=True, interval=0)