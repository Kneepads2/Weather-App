#Made by Kneepads 2
#5/31/2024 - 6/16/2024
#A weather app made using html, python, and css
#very messy but does the job

from flask import Flask, request, render_template, url_for
import requests
import datetime

app = Flask(__name__)

S3_BUCKET_URL = "https://weather-bucket-mine.s3.us-east-1.amazonaws.com"

@app.route('/')
def index():
    selected_city = int(request.args.get('city', 1))
    cities = ["Brampton", "Guelph", "Mississauga", "Niagara Falls", "Oakville", "Ottawa", "Toronto", "Waterloo"]
    api_urls = [
        "https://api.open-meteo.com/v1/forecast?latitude=43.68341&longitude=-79.76633&current=temperature_2m,is_day,weather_code&hourly=temperature_2m,apparent_temperature,precipitation_probability,weather_code,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=America%2FNew_York",
        "https://api.open-meteo.com/v1/forecast?latitude=43.5448&longitude=-80.2482&current=temperature_2m,is_day,weather_code&hourly=temperature_2m,apparent_temperature,precipitation_probability,weather_code,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=America%2FNew_York",
        "https://api.open-meteo.com/v1/forecast?latitude=43.5789&longitude=-79.6583&current=temperature_2m,is_day,weather_code&hourly=temperature_2m,apparent_temperature,precipitation_probability,weather_code,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=America%2FNew_York",
        "https://api.open-meteo.com/v1/forecast?latitude=43.0896&longitude=-79.0849&current=temperature_2m,is_day,weather_code&hourly=temperature_2m,apparent_temperature,precipitation_probability,weather_code,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=America%2FNew_York",
        "https://api.open-meteo.com/v1/forecast?latitude=43.4669381322&longitude=-79.6857955901&current=temperature_2m,is_day,weather_code&hourly=temperature_2m,apparent_temperature,precipitation_probability,weather_code,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=America%2FNew_York",
        "https://api.open-meteo.com/v1/forecast?latitude=45.4201&longitude=-75.7003&current=temperature_2m,is_day,weather_code&hourly=temperature_2m,apparent_temperature,precipitation_probability,weather_code,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=America%2FNew_York",
        "https://api.open-meteo.com/v1/forecast?latitude=43.70011&longitude=-79.4163&current=temperature_2m,is_day,weather_code&hourly=temperature_2m,apparent_temperature,precipitation_probability,weather_code,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=America%2FNew_York",
        "https://api.open-meteo.com/v1/forecast?latitude=43.4668&longitude=-80.51639&current=temperature_2m,is_day,weather_code&hourly=temperature_2m,apparent_temperature,precipitation_probability,weather_code,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=America%2FNew_York"
    ]

    #Get weather data from OpenMeteo
    response = requests.get(api_urls[selected_city])
    weather_data = response.json()
    temp = weather_data['hourly']['temperature_2m']
    wind_speed = weather_data['hourly']['wind_speed_10m']
    precipitation = weather_data['hourly']['precipitation_probability']
    weather_status = weather_data['hourly']['weather_code']
    hours = weather_data['hourly']['time']
    feels = weather_data['hourly']['apparent_temperature']
    dates = weather_data['daily']['time']
    
    #Get logos from a json file made by Stellasphere
    logo_url = "https://gist.githubusercontent.com/stellasphere/9490c195ed2b53c707087c8c2db4ec0c/raw/76b0cb0ef0bfd8a2ec988aa54e30ecd1b483495d/descriptions.json"
    logo_response = requests.get(logo_url)
    logo_data = logo_response.json()
    
    #Get the current date and time
    now = datetime.datetime.now()
    current_date = now.strftime('%Y-%m-%d')
    
    current_hour = now.strftime('%H')
    current_time = f"{current_date}T{current_hour}:00"
    
    #Get the day's max and min temp
    max_temp = weather_data['daily']['temperature_2m_max']
    min_temp = weather_data['daily']['temperature_2m_min']
    
    #Get the weekdays
    current_weekday = datetime.datetime.today().weekday()
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    #Rearrange the weekdays list so that it starts from today to the next weekday if that makes sense??
    selected_day = int(request.args.get('day', 0))
    main_weekday = weekdays[(current_weekday + selected_day) % 7]
    
    #Make a list of hour stamps of the day
    daily_temps = [[] for _ in range(7)]
    hour_of_day = ["12 AM", "1 AM", "2 AM", "3 AM", "4 AM", "5 AM", "6 AM", "7 AM", "8 AM", "9 AM", "10 AM", "11 AM",
                   "12 PM", "1 PM", "2 PM", "3 PM", "4 PM", "5 PM", "6 PM", "7 PM", "8 PM", "9 PM", "10 PM", "11 PM"]
    
    current_hour_temp = ""
    current_hour_feels = ""
    current_wind_speed = ""
    current_precipitation = ""
    current_weather_status = ""
    
    #Get the current weather stats of the hour
    for i, hour in enumerate(hours):
        if hour == current_time and selected_day == 0:
            current_hour_temp = f"{temp[i]}°C"
            current_hour_feels = f"Feels like {feels[i]}°C"
            current_wind_speed = f"{wind_speed[i]} km/h"
            current_precipitation = f"{precipitation[i]}%"
            sun_or_moon = "night" if i < 6 or i > 20 else "day"
            current_weather_status = logo_data[str(weather_status[i])][sun_or_moon]['description']
            hour_of_day[i % 24] = "NOW"
            break

    #Gets the current hour, temp, weather code of this hour and will display NOW instead of the hour stamp (like 5 PM)
    for i, hour in enumerate(hours):
        day_index = i // 24
        hour_index = i % 24
        sun_or_moon = "night" if hour_index < 6 or hour_index > 20 else "day"
        daily_temps[day_index].append({
            'hours': hour_of_day[hour_index],
            'temperature': temp[i],
            'logos': logo_data[str(weather_data['hourly']['weather_code'][i])][sun_or_moon]['image'],
            'is_now': hour_of_day[hour_index] == "NOW"
        })

    #??
    hourly_temp = daily_temps[selected_day]
    weekday_list = [weekdays[(current_weekday + i) % 7] for i in range(7)]
    
    #Get all the dates of the week and format them into like Month Day (ex: June 15)
    date_objects = [datetime.datetime.strptime(date, '%Y-%m-%d') for date in dates]
    formatted_dates = [date.strftime('%B, %d') for date in date_objects]
    
    # Change Background images depending on the weather
    current_weather_code = weather_data['current']['weather_code']
    current_is_day = weather_data['current']['is_day']
    
    if current_weather_code in [0, 1]:
        bg_image = f"{S3_BUCKET_URL}/images/sunny.jpg" if current_is_day == 1 else f"{S3_BUCKET_URL}/images/night.jpeg"
    elif current_weather_code in [2, 3]:
        bg_image = f"{S3_BUCKET_URL}/images/cloudy.jpg"
    elif current_weather_code in [45, 48]:
        bg_image = f"{S3_BUCKET_URL}/images/foggy.jpg"
    elif current_weather_code in [51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82]:
        bg_image = f"{S3_BUCKET_URL}/images/rainy.jpeg"
    elif current_weather_code in [71, 73, 75, 77, 85, 86]:
        bg_image = f"{S3_BUCKET_URL}/images/snowy.jpg"
    elif current_weather_code in [95, 96, 99]:
        bg_image = f"{S3_BUCKET_URL}/images/thunderstorm.jpg"
    #else:
    #    bg_image = url_for('static', filename='default.jpg')   Default background image if no condition matches

    return render_template('index.html', current_hour_temp=current_hour_temp, hourly_temp=hourly_temp, 
                           selected_day=selected_day, main_weekday=main_weekday, weekday_list=weekday_list, 
                           max_temp=max_temp, min_temp=min_temp, city=cities[selected_city],
                           current_hour_feels=current_hour_feels, formatted_dates=formatted_dates,
                           current_wind_speed=current_wind_speed, current_precipitation=current_precipitation,
                           current_weather_status=current_weather_status, bg_image=bg_image)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
