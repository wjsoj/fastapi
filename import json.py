import json

dic = {
    '修炼爱情 林俊杰':'3244328',
}

# store the music list
with open('music.json','w',encoding='utf-8') as f:
        json.dump(dic, f, ensure_ascii=False, indent=4)