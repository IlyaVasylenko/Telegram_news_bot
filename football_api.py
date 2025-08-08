import requests
import json
import datetime
import translators as ts
import os

def today_matches():

  football_api_key = os.getenv('FOOTBALL_API')
  url = "https://v3.football.api-sports.io/fixtures"

  today_date = datetime.datetime.today().strftime('%Y-%m-%d')

  headers = {
    'x-rapidapi-key': football_api_key,
    'x-rapidapi-host': 'v3.football.api-sports.io'
  }
  params = {
      'date': today_date,
      'timezone': 'Europe/Kiev',
  }

  #запис результаів запросу до football.json
  response = requests.request("GET", url, headers=headers, params=params)

  data = response.json()

  with open('football_api_jsons/fixtures.json', 'w', encoding='utf-8') as file:
      json.dump(data, file, indent=4, ensure_ascii=False)

  today_matches_teams = []
  international_competitions = ['UEFA Champions League', 'UEFA Europa Conference League', 'UEFA Europa League', 'UEFA Super Cup']

  with open('football_api_jsons/popular_clubs.json', 'r+', encoding='utf-8') as file:
    popular_clubs = json.loads(file.read())
  
  with open('football_api_jsons/fixtures.json','r', encoding='utf-8') as file:
      data = json.loads(file.read())

  # print(data)
  for match in data['response']:
    if match['league']['name'] in international_competitions:
        if match['teams']['home']['name'] in popular_clubs or match['teams']['away']['name'] in popular_clubs:
          home = ts.translate_text(match['teams']['home']['name'], translator='bing', from_language='en', to_language='uk') 
          away = ts.translate_text(match['teams']['away']['name'], translator='bing', from_language='en', to_language='uk') 
          time = match['fixture']['date'][11:16]
          league =ts.translate_text(match['league']['name'][5:], translator='bing', from_language='en', to_language='uk') 
          venue = ts.translate_text(match['fixture']['venue']['name'], translator='bing', from_language='en', to_language='uk') 
          city = ts.translate_text(match['fixture']['venue']['city'], translator='bing', from_language='en', to_language='uk')
          id = match['fixture']['id']
          print(f"{home} vs {away} в {league} о {time}")
          today_matches_teams.append({
             'home':home,
             'away':away,
             'league':league,
             'time':time,
             'venue':venue,
             'city':city,
             'id' : id
          })
  with open('today_fixtures.json', 'w', encoding='utf-8') as file:
    json.dump(today_matches_teams, file, indent=4, ensure_ascii=False)

