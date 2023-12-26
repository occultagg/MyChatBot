import requests
import schedule
import time
import os

def get_weather(api_key, city_name):
    base_url = "https://restapi.amap.com/v3/weather/weatherInfo"
    city_code = {'Shunde': '440606', 'Liwan': '440103', 'Tianhe': '440106'}
    params = {
        'key': api_key,
        'city': city_code[city_name],
        'extensions': 'all',
        'output': 'JSON'
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            if data['status'] == '1':
                city = data['forecasts'][0]['city']
                tmr_weather = data['forecasts'][0]['casts'][1]
                date = tmr_weather['date']
                week = tmr_weather['week']
                dayweather = tmr_weather['dayweather']
                daytemp = tmr_weather['daytemp']
                daywind = tmr_weather['daywind']
                daypower = tmr_weather['daypower']
                return f"晚上好, 明天是{date}, 周{week}.{city}明天白天天气: {dayweather},气温: {daytemp}摄氏度,吹{daywind}风,风力{daypower}级.么么哒♥"
        else:
            return f"Error: {data['message']}"

    except Exception as e:
        return f"An error occurred: {e}"
    
def send_msg(msg, to_who, is_room=False):
    base_url = 'http://localhost:3001/webhook/msg'
    timeout = 2
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
        return "request timeout"
    except Exception as e:
        return f"An error occurred: {e}"

api_key = os.getenv('GAODE_API_KEY')

if __name__ == '__main__':
    liwan_weather = get_weather(api_key, 'Liwan')
    shunde_weather = get_weather(api_key, 'Shunde')
    job1 = schedule.every().day.at("23:00").do(send_msg(liwan_weather, 'Sharon'))
    job2 = schedule.every().day.at("23:00").do(send_msg(shunde_weather, 'Peter'))

    while True:
        schedule.run_pending()
        time.sleep(1)

        if job1.last_run is not None and job1.last_run.day != schedule.next_run.day:
            task_result = job1.result
            print(f"Result of last run: {task_result}")
        if job2.last_run is not None and job2.last_run.day != schedule.next_run.day:
            task_result = job2.result
            print(f"Result of last run: {task_result}")