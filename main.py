from footballnews_parse import news_parse
from ai import rewrite_news
from football_api import today_matches
from lineups import team_lineup
import telebot
import json
import random
import os
import datetime
# import schedule 

date = datetime.datetime.now().strftime("%d.%m.%Y")

bot_id = os.getenv('TELEGRAM_BOT_TOKEN')
channel_id = os.getenv('TELEGRAM_CHANNEL_ID')
print('Writing',bot_id, channel_id)
bot = telebot.TeleBot(bot_id)
match_posted = True

#Париснг і скорочення тексту в певний час
try:
    os.mkdir(f'data{date}')
    news_parse()
    rewrite_news()
    today_matches()
    match_posted = False
except:
    print('Folder is already exists')

#файл з новинами
base_dir = os.path.dirname(os.path.abspath(__file__))  # путь к папке, где лежит main.py
json_path = os.path.join(base_dir, f'data{date}', f"data{date}gemini.json")

with open(json_path,'r', encoding='utf-8') as file:
    data = json.loads(file.read())
# print(data)

#файл з використаними новинами
with open('used_post.json', encoding='utf-8') as file:
    used_post = json.loads(file.read())
# print(used_post)

#файл з сьогоднішніми матчами

if match_posted == False:
    with open('today_fixtures.json', 'r', encoding='utf-8') as file:
            list_match = json.loads(file.read())
    if list_match != []:
        message_matches = 'Сьгоднішні матчі:\n'
        for match in list_match:
            message_matches += f'{match["league"]}\n{match["home"]} vs {match["away"]}\n⏱️{match["time"]}\n🏙️{match["city"]}\n🏟️{match["venue"]}\n'

        bot.send_message(channel_id, text = message_matches.strip())

#пости зі складами команд

# time = list_match[0]['']
with open('today_fixtures.json', 'r', encoding='utf-8') as file:
        list_match = json.loads(file.read())
for match in list_match:
    if int(match["time"][0:-3]) == int(datetime.datetime.now().strftime('%H'))+4:
        print(int(datetime.datetime.now().strftime('%H')))
        print(int(match["time"][0:-3]))
        fixture = match['id']
        team_lineup(match['id'])
        photos = [
        open('images/away_team lineup.jpg', 'rb'),
        open('images/home_team lineup.jpg', 'rb')
        ]
        media = []
        for photo in photos:
            media.append(telebot.types.InputMediaPhoto(photo))
        bot.send_media_group(chat_id=os.getenv('TELEGRAM_CHANNEL_ID'), media=media)
        for photo in photos:
            photo.close()
        # bot.send_photo(chat_id= os.getenv('TELEGRAM_CHANNEL_ID'),photo=['images/away_team lineup','images/home_team lineup'])
        

#відправлення постів в телеграм канал

try:
    for item in data:
        # random.shuffle(data)
        # while data[0]['title'] in used_post:
        #     random.shuffle(data)
        # item = data[0]
        if item['title'] in used_post:
            continue
        bot.send_photo(chat_id= os.getenv('TELEGRAM_CHANNEL_ID'), photo = item['image'], caption=f'<b>{item["title"]}</b>\n{item["text"][0:950]}\n@goals_news', parse_mode='html')
        used_post.append(item['title'])
        break
        # print(item)
        # post = f'{item["title"]}\n{item["image"]}\n{item["text"][0:100]}'
        # bot.send_message(message.chat.id, post, parse_mode='html')
except:
    print("Can't post news")
#додавання використаних постів в used_post.json
with open('used_post.json','w', encoding='utf-8') as file:
    json.dump(used_post, file, indent=4, ensure_ascii=False)
# print(used_post)
# print(datetime.datetime.now().strftime('%H:%M'))

print(int(datetime.datetime.now().strftime('%H')))
print(int(list_match[0]["time"][0:-3]))
