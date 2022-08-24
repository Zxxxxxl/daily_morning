from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
love_date = os.environ['LOVE_DATE']  # 相恋日
goh_date = os.environ['GOH_DATE']  # 相恋日
love200_date = os.environ['LOVE200_DATE']  # 恋爱200天
love365_date = os.environ['LOVE365_DATE']  # 恋爱一周年

city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    res = requests.get(url).json()
    weather = res['data']['list'][0]
    return weather['weather'], math.floor(weather['temp'])


def get_count():
    delta = today - datetime.strptime(love_date, "%Y-%m-%d")
    return delta.days


def get_Love200():
    delta = datetime.strptime(love200_date, "%Y-%m-%d") - today
    return delta.days


def get_Love365():
    delta = datetime.strptime(love365_date, "%Y-%m-%d") - today
    return delta.days

def get_gthz():
    delta = datetime.strptime(goh_date, "%Y-%m-%d") - today
    return delta.days



def get_birthday():
    next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days


def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {
    "weather": {"value": wea},
    "temperature": {"value": temperature},
    "love_days": {"value": get_count()},
    "love100_days": {"value": get_Love200()},
    "love365_days": {"value": get_Love365()},
    "goh": {"value": get_gthz()},
    "birthday_left": {"value": get_birthday()},
    "words": {"value": get_words(),
              "color": get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
