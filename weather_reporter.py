# -*- coding: utf-8 -*-
import requests
import schedule
import time
import os

def get_location_id(location, api_key):
    url = 'https://geoapi.qweather.com/v2/city/lookup'
    params = {"location": location, "key": api_key}

    response = requests.get(url, params=params)

    if response.ok:
        data = response.json()
        print(data)
        if len(data["location"]) == 1:
            return data["location"][0]["id"], data["location"][0]["name"]
        else:
            return f"搜索到多于1个location,请检查."
    else:
        print(f"localtion ID请求失败，状态码: {response.status_code}")
        return response.text

def get_tmr_weather(api_key, city_id, locate):
    base_url = "https://devapi.qweather.com/v7/weather/3d"
    params = {
        'key': api_key,
        'location': city_id
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        if response.ok:
            tmr_weather = data["daily"][1]
            date = tmr_weather["fxDate"]
            day_weather = tmr_weather["textDay"]
            tem_max = tmr_weather["tempMax"]
            tem_min = tmr_weather["tempMin"]
            day_wind_dir = tmr_weather["windDirDay"]
            day_wind_scale = tmr_weather["windScaleDay"]
            humidity = tmr_weather["humidity"]
            print(f"天气信息获取成功:{data}")
            return f"晚上好!明天{date},{locate}白天{day_weather},最高温{tem_max}摄氏度,最低温{tem_min}摄氏度.吹{day_wind_scale}级的{day_wind_dir}.相对湿度{humidity}%.\n么么哒~"
        else:
            return "Error: 天气预报获取失败."

    except Exception as e:
        return f"An error occurred: {e}"
    
def send_msg(msg, to_who, is_room=False):
    timeout = 2
    base_url = 'http://localhost:3001/webhook/msg'
    headers = {'Content-Type': 'application/json'}
    body = {
        'to': to_who,
        'isRoom': is_room,
        'type': 'text',
        'content': msg
    }

    try:
        response = requests.post(base_url, headers=headers, json=body, timeout=timeout)
        data = response.json()
        return data
    except requests.Timeout:
        return f"Request Timeout."
    except Exception as e:
        return f"An error occurred: {e}"
    
def reporter(location, api_key, to_who, is_room=False):
    id, locate = get_location_id(location, api_key)
    print(f"city_id:{id}")
    tmr_weather = get_tmr_weather(api_key, id, locate)
    reporter_result = send_msg(tmr_weather, to_who, is_room)
    print(reporter_result)

if __name__ == '__main__':
    api_key = os.getenv('HEFENG_API_KEY')
    schedule.every().day.at("20:00").do(reporter, "shunde", api_key, "Peter")
    schedule.every().day.at("20:00").do(reporter, "liwan", api_key, "Sharon")
    schedule.every().thursday.at("08:00").do(reporter, "tianhe", api_key, "AI潘炜健", True)
    while True:
        schedule.run_pending()
        time.sleep(1)


