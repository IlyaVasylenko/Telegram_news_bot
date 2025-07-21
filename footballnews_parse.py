from bs4 import BeautifulSoup
import requests
import lxml
import os
import datetime
import json

def news_parse():

    #Массив новин
    posts_list = []

    # Дата постів
    date = datetime.datetime.now().strftime('%d.%m.%Y')

    # Парсинг основної сторінки
    urls = ['https://football.ua/england.html','https://football.ua/spain.html', 'https://football.ua/italy.html','https://football.ua/france.html','https://football.ua/germany.html']
    headers = {
        'accept':'*/*',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0'
    }

    for url in urls:

        req = requests.get(url, headers=headers)

        src = req.text
        # print(src.encode('utf-8'))
        with open('index.html','w', encoding='utf-8') as file:
            file.write(src)

        with open('index.html', encoding='utf-8') as file:
            src = file.read()
        soup = BeautifulSoup(src, 'lxml')

        all_news = soup.find('div', class_='col-right').find_all('a')
        # print(all_news)
        all_news.append(soup.find('article', class_='news-block').find('a'))
        all_categories_list = []

        for item in all_news:
            title = item.text.strip()
            link = item.get("href").strip()
            if title!='' and link!='':
                all_categories_list.append(link)
            
        # print(all_categories_list)



        #Парсинг текстів з постів

        post_text_string=''
        file_text = ''
        folder = f'data{date}'
        try:
            os.mkdir(folder)
        except:
            print('Folder is already exists')

        for site in all_categories_list:
            req = requests.get(site, headers)
            src = req.text
                # print(file_text)
            soup = BeautifulSoup(src, 'lxml')
            try:
                post_title = soup.find('article', class_='author-article').find('h1')
                # print(post_title.text)
            except:
                post_title = "Could't find the title"
                # print(post_title)

            try:
                post_image = soup.find('div', class_='article-photo').find('img').get('src')
                # print(post_image)
            except:
                post_image = "Couldn't find the image"
                # print(post_image)
            try: 
                post_text = soup.find('div', class_='article-text').find_all('p')
                # print(post_text)
                for el in post_text:
                    post_text_string += el.text+'\n'
                    # print(post_text_string)
                post_text_string = post_text_string.strip()

            except:
                post_text = "Couldn't find the text"
                print(post_text)
            posts_list.append(
                {
                    'title':post_title.text,
                    'image': post_image,
                    'text': post_text_string,
                }
            
            )
            post_text_string = ''
        # print(posts_list)
        with open(f'{folder}/{folder}.json','w', encoding='utf-8') as file:
            json.dump(posts_list, file, indent=4, ensure_ascii=False)
    # print(posts_list)
    