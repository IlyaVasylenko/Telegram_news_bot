import json
import datetime
with open(f'data09.08.2025/data09.08.2025.json', 'r', encoding='utf-8') as file:
    file1 = json.loads(file.read())
    
with open(f'data09.08.2025/data09.08.2025.json', 'r', encoding='utf-8') as file:
    file2 = json.loads(file.read())

# print(file1)
list_titles = []
for i in file2:
    list_titles.append(i['title'])
print(list_titles)
count=0
for i in range(0,len(file1)):
    if file1[i]['title'] in list_titles :
        count+=1
    
print(count, len(file1), len(file2))

# with open('used_post.json','w', encoding='utf-8') as file:
#     json.dump([],file, indent=4, ensure_ascii=False)
print(datetime.datetime.now().strftime('%d.%m.%Y'))
print(datetime.datetime.now().strftime('%H'))