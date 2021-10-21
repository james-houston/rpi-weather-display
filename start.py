from get_weather import handle_weather
from update_display import update_display
from time_of_day_brightness import update_brightness

from threading import Thread
from queue import Queue


dynamic_temperature_png = "dynamic-temperature.png"
dynamic_condition_gif = "dynamic-condition.gif"

def main():
    q = Queue()

    brightnessThread = Thread(target = update_brightness, args=(q,))
    weatherThread = Thread(target = handle_weather, args=(dynamic_condition_gif, dynamic_temperature_png))
    displayThread = Thread(target = update_display, args=(dynamic_condition_gif, dynamic_temperature_png, q))

    brightnessThread.start()
    weatherThread.start()  
    displayThread.start()

    brightnessThread.join()
    weatherThread.join()
    displayThread.join()

main()