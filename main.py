from footballnews_parse import news_parse
from ai import rewrite_news
import telebot
import json
import random
import os
import datetime
# import schedule 

date = f'data{datetime.datetime.now().strftime('%d.%m.%Y')}'
# date = 'data07.17.25'

bot_id = os.getenv('TELEGRAM_BOT_TOKEN')
channel_id = os.getenv('TELEGRAM_CHANNEL_ID')
bot = telebot.TeleBot(bot_id)

#Париснг і скорочення тексту в певний час
if datetime.datetime.now().strftime('%H:%M') == '07:00':
    news_parse()
    # rewrite_news()

#файл з новинами
with open(f'{date}/{date}gemini.json','r', encoding='utf-8') as file:
    data = json.loads(file.read())
# print(data)

#файл з використаними новинами
with open('used_post.json', encoding='utf-8') as file:
    used_post = json.loads(file.read())
# print(used_post)
#відправлення постів в телеграм канал

# item = data[0]
# bot.send_photo(channel_id, photo = item['image'], caption=f'<b>{item['title']}</b>\n{item['text'][0:950]}', parse_mode='html')
@bot.message_handler(commands=['start'])
def main(message):
    random.shuffle(data)
    
    while data[0]['title'] in used_post:
            random.shuffle(data)
    item = data[0]
    # print(item)
    # post = f'{item["title"]}\n{item["image"]}\n{item["text"][0:100]}'
    # bot.send_message(message.chat.id, post, parse_mode='html')
    bot.send_photo(channel_id, photo = item['image'], caption=f'<b>{item['title']}</b>\n{item['text'][0:950]}', parse_mode='html')
    used_post.append(item['title'])

    #додавання використаних постів в used_post.json
    with open('used_post.json','w', encoding='utf-8') as file:
        json.dump(used_post, file, indent=4, ensure_ascii=False)
    # print(used_post)

bot.polling(none_stop=True)

