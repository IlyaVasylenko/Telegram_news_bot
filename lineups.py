import json
import requests
from PIL import Image, ImageDraw, ImageColor, ImageFont
import os

#request
def team_lineup(fixture):
    with open('today_fixtures.json', 'r', encoding='utf-8') as file: 
        today_match = json.loads(file.read())

    # football_api_key = '18fab6c5615a8f9c5e949136ece86093'
    football_api_key = os.getenv('FOOTBALL_API')
    url = "https://v3.football.api-sports.io/fixtures/lineups"

    headers = {
        'x-rapidapi-key': football_api_key,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    params = {
        'fixture' : fixture
    }

    #запис результаів запросу до football.json
    response = requests.request("GET", url, headers=headers, params=params)

    if response.status_code == 200:

        with open('football_api_jsons/lineups2.json', 'w', encoding='utf-8') as file:
            json.dump(response.json(), file, indent=4, ensure_ascii=False)

    #Отримання інформації команд
    with open('football_api_jsons/lineups2.json', 'r', encoding='utf-8') as file:
            lineups = json.loads(file.read())


    #Створення розстановок

    team_count = 0
    for teams in lineups['response']:
        football_pitch = Image.open('images/football_pitch2.png')

        football_pitch_pattern = ImageDraw.Draw(football_pitch)


        #лого команди
        logo_link= teams['team']['logo']
        # print(logo_link)

        response = requests.get(logo_link)

        if response.status_code == 200:
            with open('images/requests.jpg', 'wb') as file:
                file.write(response.content)

        logo = Image.open('images/requests.jpg')

        #колір футболки
        color_player = teams['team']['colors']['player']
        color_goalkeeper = teams['team']['colors']['goalkeeper']

        old_border_color = (0,0,0,225)
        old_color = (255,255,255,255)

        new_color = ImageColor.getcolor(f"#{color_player['primary']}", "RGBA")
        new_border_color = ImageColor.getcolor(f"#{color_player['border']}", "RGBA")
        new_number_color = ImageColor.getcolor(f"#{color_player['number']}", "RGBA")

        new_color_goalkeeper = ImageColor.getcolor(f"#{color_goalkeeper['primary']}", "RGBA")
        new_border_goalkeeper = ImageColor.getcolor(f"#{color_goalkeeper['border']}", "RGBA")
        new_number_goalkeeper = ImageColor.getcolor(f"#{color_goalkeeper['number']}", "RGBA")

        # print(new_color)


        #створення футболки гравців
        shirt = Image.open('images/White_T-shirt.png').convert('RGBA')
        shirt = shirt.resize((85,85))

        pixels = shirt.getdata()
        # print(pixels)
        new_pixels = [
            new_color if pixel == old_color else
            new_border_color if pixel == old_border_color else
            pixel 
            for pixel in pixels
        ]

        shirt.putdata(new_pixels)
        shirt.save("images/shirt.png")

        #створення футболки голкіпера

        shirt = Image.open('images/White_T-shirt.png').convert('RGBA')
        shirt = shirt.resize((85,85))

        pixels = shirt.getdata()
        # print(pixels)
        #воротар
        new_pixels = [
            new_color_goalkeeper if pixel == old_color else
            new_border_goalkeeper if pixel == old_border_color else
            pixel 
            for pixel in pixels
        ]

        shirt.putdata(new_pixels)
        shirt.save("images/goalkeeper_shirt.png")



        #масив гравців команд
        all_players = []
        count_midfielder = 1

        formation = teams['formation']
        formation = str(formation).split('-')
        formation = [1] + formation
        print(formation)
        quantity_players = len(formation)


        all_players2=[]
        players = []
        count_players = 0
        for qnt in formation:
            for person in range(0,int(qnt)):
                players.append(teams["startXI"][count_players])
                count_players += 1
            all_players2.append(players)
            players = []
        print(all_players2, '!!!!')





        #розстановка на полі

        count = 0
        max_height = 900
        max_width = 600

        start_position_y = 900 // quantity_players - (900 // quantity_players//2)
        position_y = 900 // quantity_players

        # print(start_position_y)
        new_shirt_goalkeeper = Image.open('images/goalkeeper_shirt.png')
        new_shirt = Image.open('images/shirt.png')
        draw_shirt = ''
        # print(len(formation)+1)

        for player_y in all_players2:
            max_width = 600
            for player_x in player_y:
                if player_x['player']['pos'] == 'G':
                    player_shirt = Image.open('images/goalkeeper_shirt.png')
                    font = ImageFont.truetype(font = 'font/Roboto-Bold.ttf',size=28)
                    draw_shirt = ImageDraw.Draw(player_shirt)
                    draw_shirt.text((42,43),font=font, text = str(player_x['player']['number']), fill = new_number_goalkeeper, align='center', anchor = 'mm')

                else:
                    player_shirt = Image.open('images/shirt.png')
                    font = ImageFont.truetype(font = 'font/Roboto-Bold.ttf',size=28)
                    draw_shirt = ImageDraw.Draw(player_shirt)
                    draw_shirt.text((42,43),font=font, text = str(player_x['player']['number']), fill = new_number_color, align='center', anchor = 'mm')

                if count == 0:
                    start_position_x = max_width // len(player_y) - (600 // len(player_y)//2)
                    max_width -= start_position_x
                    count+=1
                position_x = 600 // len(player_y)

                font = ImageFont.truetype(font = 'font/Roboto-Bold.ttf', size=20)
                if len(str(player_x['player']['name']))>=19:
                    text = str(player_x['player']['name']).split(' ')
                    for word in text:
                        name+=f'\n{word}'
                else:
                    name = str(player_x['player']['name'])
                football_pitch.paste(player_shirt,(max_width +170, max_height - 80), mask=player_shirt)
                football_pitch_pattern.text((max_width +170+40, max_height - 80+92), font=font, text = name, fill = 'white', align='center', anchor = 'mm', stroke_width=2, stroke_fill="black")

                name = ''
                max_width -= position_x
                
            count=0
            max_height -= position_y
            
        #substitution, coach, logo
        football_pitch.paste(logo,(10,30), mask=logo)

        response = requests.get(teams['coach']['photo'])

        if response.status_code == 200:
            with open('images/coach.png', 'wb') as file:
                file.write(response.content)

        coach_photo = Image.open('images/coach.png')
        coach_name = teams['coach']['name']

        font = ImageFont.truetype(font = 'font/Roboto-Bold.ttf', size=25)
        football_pitch.paste(coach_photo,(950,50))
        football_pitch_pattern.text((1020,220), font=font, text = coach_name, fill = 'white', align='center', anchor = 'mm', stroke_width=2, stroke_fill="black")


        padding = 20
        font = ImageFont.truetype(font = 'font/Roboto-Bold.ttf', size=30)
        for substitution in teams['substitutes']:
            text = f"{substitution['player']['number']} {substitution['player']['name']}"
            football_pitch_pattern.text((920, 320 + padding), font=font, text = text, fill = 'white', align='right', anchor = 'lm', stroke_width=2, stroke_fill="black")
            padding += 40 
        # shirt.show()
        #додавання картинок
        
        if team_count == 0:
            football_pitch.save(f'images/home_team lineup.jpg')
        else:
            football_pitch.save(f'images/away_team lineup.jpg')
        team_count += 1
        football_pitch.show()
team_lineup(1386557)