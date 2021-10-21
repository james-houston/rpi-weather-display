import requests
from shutil import copyfile
import time
import im_combine


url = "http://api.weatherapi.com/v1/forecast.json?key=%s&q=%s&days=1&aqi=no&alerts=yes"
api_key = "YOUR_API_KEY"
city = "YOUR_CITY"
use_celsius = True

weather_update_freq_seconds = 600

image_files = {
    "coudy": "img/cloudy.gif",
    "partly cloudy": "img/partly-cloudy.gif",
    "rain": "img/rain.gif",
    "snowy": "img/snowy.gif",
    "sunny": "img/sunny.gif",
    "lightning": "img/lightning.gif",
    "no image": "img/no-image.gif"
}

# Map weather condition codes from weatherapi.com to our available gifs
cloudy = [1006, 1009, 1030, 1135, 1147]
partly_cloudy = [1003, ]
rain = [1063, 1072, 1150, 1153, 1168, 1171, 1180, 1183, 1186, 1189, 1192, 
        1195, 1198, 1201, 1240, 1243, 1246, 1261, 1264]
snowy = [1066, 1069, 1114, 1117, 1204, 1207, 1210, 1213, 1216, 1219, 
        1222, 1225, 1237, 1249, 1252, 1255, 1258]
sunny = [1000, ]
lightning = [1087, 1273, 1276, 1279, 1282]

def handle_weather(dynamic_conditions_gif, dynamic_temperature_png):
    populated_url = url.format(api_key, city)
    while True:
        min, max, curr, img = get_weather(use_celsius, populated_url)
        copyfile(img, dynamic_conditions_gif)
        im_combine.build_image(min, max, curr, dynamic_temperature_png)
        time.sleep(weather_update_freq_seconds)

def get_weather(useCelsius, url):
    resp = requests.get(url=url)
    data = resp.json()
    min, max, curr, condition = parse_api_call(data, useCelsius)
    img = condition_code_to_image(condition)
    return min, max, curr, img
    
def parse_api_call(data, useCelsius):
    if useCelsius:
        min = data['forecast']['forecastday'][0]['day']['mintemp_c']
        max = data['forecast']['forecastday'][0]['day']['maxtemp_c']
        curr = data['current']['temp_c']
    else:
        min = data['forecast']['forecastday'][0]['day']['mintemp_f']
        max = data['forecast']['forecastday'][0]['day']['maxtemp_f']
        curr = data['current']['temp_f']
    condition = data['forecast']['forecastday'][0]['day']['condition']['code']
    return min, max, curr, condition


def condition_code_to_image(code):
    # Examine weather_conditions.json to see the weatherapi.com documentation on what each code represents
    if code in cloudy:
        return image_files['coudy']
    elif code in partly_cloudy:
        return image_files['partly cloudy']
    elif code in rain:
        return image_files['rain']
    elif code in snowy:
        return image_files['snowy']
    elif code in sunny:
        return image_files['sunny']
    elif code in lightning:
        return image_files['lightning']
    else:
        return image_files['no image']