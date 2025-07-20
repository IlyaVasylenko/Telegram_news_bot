import google.generativeai as genai
import os
import json
import datetime

def rewrite_news():
    genai.configure(api_key=os.getenv('GEMINI_API'))

    model =genai.GenerativeModel(
        model_name='gemini-2.5-pro'
    )
    # text = "Баварія запропонувала 67,5 мільйонів євро за лівого вінгера Ліверпуля Луїса Діаса, передає видання The Athletic.\nПовідомляється, що чинний чемпіон Англії одразу ж відхилив першу офіційну пропозицію мюнхенського клубу. У той же час гравець чітко дав Ліверпулю зрозуміти, що хоче піти.\nЙого контракт із \"червоними\" розраховано до кінця червня 2027 року. Раніше повідомлялося, що за Діаса вони хочуть отримати 70-80 млн євро.\nУ разі відходу Луїса Ліверпуль може поборотися за флангового нападника мадридського Реала Родріго. Станом на зараз колумбієць вважається важливою частиною планів клубу, про що було повідомлено зацікавлені в його переході сторони.\nЗа даними журналіста Флоріана Плеттенберга, гранд Бундесліги готує нову пропозицію. Із Баварією виконавець може підписати розрахований на чотири або п'ять років контракт.\nДіас приєднався до мерсісайдців у січні 2022 року з Порту за 37,5 млн фунтів стерлінгів, тоді як з урахуванням бонусів сума трансферу може зрости до 50 млн. На рахунку лівого вінгера 41 гол і 23 асисти в 148-ми матчах за \"червоних\" у всіх турнірах."
    # response = model.generate_content(f'Скороти та перевразуй цю новину до 1000 символів:{text}')

    date = (datetime.datetime.now().strftime('%d.%m.%Y')
    with open(f'data{date}/data{date}.json','r', encoding='utf-8') as file:
        src = json.loads(file.read())
    count = 0
    for item in range(0,len(src),3):
        try:
            # text = item['text']
            # print(text)
            format_of_response = f'''Скороти та перевразуй цю новину до 4-5 речень і до 1000 символів. Результат виведи в цьому форматі:
                                ===Новина===
                                (тут текст 1)
                                ===Новина==='
                                (тут текст 2)
                                ===Новина==='
                                (тут текст 3)
                                1){src[item]['text']}

                                2){src[item+1]['text']} 

                                3){src[item+2]['text']} '''
            response = model.generate_content(format_of_response)
            # item['text'] = response.text.strip()
            count+=1
            print(count)
            print(response.text.strip())
            list_of_news = response.text.split('===Новина===')
            print(list_of_news)
            src[item]['text'] = list_of_news[1]
            src[item+1]['text'] = list_of_news[2]
            src[item+2]['text'] = list_of_news[3]

        except:
            print('try again')
            try:
                format_of_response = f'''Скороти та перевразуй цю новину до 4-5 речень і до 1000 символів. Результат виведи в цьому форматі:
                                ===Новина===
                                (тут текст 1)
                                ===Новина==='
                                (тут текст 2)
                                1){src[item]['text']}

                                2){src[item+1]['text']} '''
                response = model.generate_content(format_of_response)
                # item['text'] = response.text.strip()
                count+=1
                print(count)
                print(response.text.strip())
                list_of_news = response.text.split('===Новина===')
                print(list_of_news)
                src[item]['text'] = list_of_news[1]
                src[item+1]['text'] = list_of_news[2]
            except:
                print('try again')
                try:
                    format_of_response = f'''Скороти та перевразуй цю новину до 4-5 речень і до 1000 символів. Результат виведи в цьому форматі:
                                ===Новина===
                                (тут текст 1)
                                1){src[item]['text']} '''
                    response = model.generate_content(format_of_response)
                    # item['text'] = response.text.strip()
                    count+=1
                    print(count)
                    print(response.text.strip())
                    list_of_news = response.text.split('===Новина===')
                    print(list_of_news)
                    src[item]['text'] = list_of_news[1]
                except:
                    print('Error')

    with open(f'data{date}/data{date}gemini.json','w', encoding='utf-8') as file:
        json.dump(src, file, indent=4, ensure_ascii=False)
    # print(response.text)
