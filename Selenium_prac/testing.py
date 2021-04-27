import time
import json

with open('./time_table.json') as f:
    time_table = json.load(f)

real_hour, real_minute = map(int, tuple(time.strftime("%H %M", time.localtime()).split()))
weekday = time.strftime("%A", time.localtime())

target_hour, target_minute = map(int, tuple(list(time_table[weekday].keys())[0].split(':')))
print(target_hour, target_minute)
