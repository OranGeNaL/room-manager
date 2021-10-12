import os
import telebot
import json

from requests import get
from wakeonlan import send_magic_packet

# bot = telebot.TeleBot(os.environ.get("TELEGRAM_KEY"))


# subs = []
# pending_subs = []
# print("work13")

#получение глобального ip
# print(get("https://api.ipify.org").text)
# print(os.environ.get("MAC_ADDRESS"))
# os.system("wakeonlan " + os.environ.get("MAC_ADDRESS"))
# send_magic_packet(os.environ.get("MAC_ADDRESS"))


# print(os.environ.get("TELEGRAM_KEY"))
# print(os.environ.get("MAC_ADDRESS"))

# def main():
#     print("work43")
#     read_cache_subs()
#     bot.polling(none_stop=True, interval=0)

def cache_subs():
    json_note = ""
    if len(subs) != 0:
        print("Записываю подписчиков в файл")
        json_note = json.dumps(subs)
    file = open("/app/volume/subs.json", "w")
    file.write(json_note)
    file.close()

def read_cache_subs():
    file = open("/app/volume/subs.json", "r")
    json_note = file.read()
    print("Подписчики: " + json_note)
    if len(json_note) > 0:
        subs = json.loads(json_note)

    

# try:

# except FileNotFoundError:
    # cache_subs()
subs = []
pending_subs = []
print("work13")
print("work43")
read_cache_subs()


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
                subs_string += str(i) + "\n"
            bot.send_message(message.from_user.id, subs_string)
        else:
            bot.send_message(message.from_user.id, "Вы не являетесь подписчиком")


    elif message.text == os.environ.get("ADMIN_PASSWORD"):
        if message.from_user.id in pending_subs or not(message.from_user.id in subs):
            subs.append(message.from_user.id)
            if message.from_user.id in pending_subs:
                pending_subs.remove(message.from_user.id)
            bot.send_message(message.from_user.id, "Вы успешно подписаны на обновления")
            cache_subs()
        
    else:
        bot.send_message(message.from_user.id, "Не понимаю")






# main()
# def main():
# if __name__ == "__main__":
#     print("work43")
#     read_cache_subs()

bot.infinity_polling()

# bot.polling(none_stop=True, interval=0)