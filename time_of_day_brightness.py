from datetime import datetime, time
import time as sleep_time


brightness_time_map = {
    6: 20,
    8: 50,
    20: 20,
    21: 1,
}

def update_brightness(in_q):
    new_day = False
    mem = -1     # we want to put in the most recent value before waiting for the next value at boot
    while True:
        for hour in brightness_time_map:
            now = datetime.now().time()
            print("current time %s" % now.strftime("%H:%M:%S"))
            if new_day:
                print("next tick is tomorrow")
                # The final setting of the day has run and we need to wait until the next setting tomorrow
                if mem != -1:
                    print("we have something to put in the queue %d" % mem)
                    in_q.put(brightness_time_map[mem])
                    mem = -1
                seconds_until_update = ((24 - now.hour - 1) * 60 * 60 ) + (hour * 60 * 60) + ((60 - now.minute) * 60) + (60 - now.second)
                print("sleeping %d seconds until %d" % (seconds_until_update, hour))
                sleep_time.sleep(seconds_until_update)
                print("putting brightness value %d into the queue" % (brightness_time_map[hour], ))
                in_q.put(brightness_time_map[hour])
            if now > time(hour, 0):
                print("time is after %d" % hour)
                mem = hour
                continue
            else:
                sleep_time.sleep(5)
                print("putting in mem value for hour %d" % mem)
                if mem != -1:
                    in_q.put(brightness_time_map[mem])
                    mem = -1
                # - 1 extra hour because time is inclusive (e.g. 8.30 to 9.00 is 0 hours and 30 minutes)
                seconds_until_update = ((hour - now.hour - 1) * 60 * 60 )+ ((60 - now.minute) * 60) + (60 - now.second)
                print("sleeping %d seconds until %d" % (seconds_until_update, hour))
                sleep_time.sleep(seconds_until_update)
                print("putting brightness value %d into the queue" % (brightness_time_map[hour], ))
                in_q.put(brightness_time_map[hour])
        new_day = True
        print("next time is tomorrow")