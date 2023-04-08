from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
headers = {
    'Cookie': '_ga=GA1.2.387593542.1617107630; _gid=GA1.2.1534665002.1617107630; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1617107630,1617109657; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1617110185; kw_token=QUE6LY91RKT',
    'csrf': 'QUE6LY91RKT',
    'Host': 'www.kuwo.cn',
    'Referer': 'http://www.kuwo.cn/search/list?key=fuck',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
}
app = FastAPI()

origins = [
    "http://music.wjsphy.top",
    "https://music.wjsphy.top",
    "http://localhost",
    "http://localhost:20201",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World. Welcome to FastAPI!"}

@app.get("/music")
async def music(id: str):
    detail = requests.get(
        url='https://netease-api.wjsphy.top//song/detail',
        params={
            'ids': id,
        }
    )
    name = detail.json()['songs'][0]['name']
    response = requests.get(
        url='http://www.kuwo.cn/api/www/search/searchMusicBykeyWord',
        params={
            'key': name,
            'pn': 1,
            'rn': 10,
            'httpsStatus': 1,
            'reqId': 'f0830500-9158-11eb-b0a1-83f9d69777f7'
        },
        headers=headers
    )
    song_list = response.json()['data']['list']
    rid = None
    for song in song_list:
        if song['name']==detail.json()['songs'][0]['name'] and detail.json()['songs'][0]['ar'][0]['name'] in song['artist']:
            rid = song['rid']
            break
    if rid is None:
        rid = song_list[0]['rid']
    urll = requests.get(
        url=f'http://www.kuwo.cn/api/v1/www/music/playUrl?mid={rid}&type=url&httpsStatus=1',
    )
    # print(urll.json()['data']['url'])
    return urll.json()['data']['url']