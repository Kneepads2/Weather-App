from flask import Flask, request, render_template
import requests
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    selected_city = int(request.args.get('city', 1))
    cities = ["Brampton", "Mississauga", "Oakville", "Toronto"]
    api_urls = [
        "https://api.open-meteo.com/v1/forecast?latitude=43.68341&longitude=-79.76633&hourly=temperature_2m,apparent_temperature,precipitation_probability,weather_code,wind_speed_10m&daily=temperature_2m_max,temperature_2m_min&timezone=America%2FNew_York",
        "https://api.open-meteo.com/v1/forecast?latitude=43.5789&longitude=-79.6583&hourly=temperature_2m,apparent_temperature,precipitation_probability,weather_code,wind_speed_10m&daily=temperature_2m_max,temperature_2m_min&timezone=America%2FNew_York",
        "https://api.open-meteo.com/v1/forecast?latitude=43.4669381322&longitude=-79.6857955901&hourly=temperature_2m,apparent_temperature,precipitation_probability,weather_code,wind_speed_10m&daily=temperature_2m_max,temperature_2m_min&timezone=America%2FNew_York",
        "https://api.open-meteo.com/v1/forecast?latitude=43.70011&longitude=-79.4163&hourly=temperature_2m,apparent_temperature,precipitation_probability,weather_code,wind_speed_10m&daily=temperature_2m_max,temperature_2m_min&timezone=America%2FNew_York"
    ]

    response = requests.get(api_urls[selected_city])
    weather_data = response.json()
    temp = weather_data['hourly']['temperature_2m']
    hours = weather_data['hourly']['time']
    
    logo_url = "https://gist.githubusercontent.com/stellasphere/9490c195ed2b53c707087c8c2db4ec0c/raw/76b0cb0ef0bfd8a2ec988aa54e30ecd1b483495d/descriptions.json"
    logo_response = requests.get(logo_url)
    logo_data = logo_response.json()
    
    now = datetime.datetime.now()
    current_date = now.strftime('%Y-%m-%d')
    current_hour = now.strftime('%H')
    current_time = f"{current_date}T{current_hour}:00"
    
    max_temp = weather_data['daily']['temperature_2m_max']
    min_temp = weather_data['daily']['temperature_2m_min']
    
    current_weekday = datetime.datetime.today().weekday()
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    selected_day = int(request.args.get('day', 0))
    main_weekday = weekdays[(current_weekday + selected_day) % 7]
    
    daily_temps = [[] for _ in range(7)]
    hour_of_day = ["12 AM", "1 AM", "2 AM", "3 AM", "4 AM", "5 AM", "6 AM", "7 AM", "8 AM", "9 AM", "10 AM", "11 AM",
                   "12 PM", "1 PM", "2 PM", "3 PM", "4 PM", "5 PM", "6 PM", "7 PM", "8 PM", "9 PM", "10 PM", "11 PM"]
    
    current_hour_temp = ""
    for i, hour in enumerate(hours):
        if hour == current_time and selected_day == 0:
            current_hour_temp = f"{temp[i]}°C"
            hour_of_day[i % 24] = "NOW"
            break

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

    hourly_temp = daily_temps[selected_day]
    weekday_list = [weekdays[(current_weekday + i) % 7] for i in range(7)]

    return render_template('index.html', current_hour_temp=current_hour_temp, hourly_temp=hourly_temp, selected_day=selected_day, main_weekday=main_weekday, weekday_list=weekday_list, max_temp=max_temp, min_temp=min_temp, city=cities[selected_city])

if __name__ == '__main__':
    app.run(debug=True)
