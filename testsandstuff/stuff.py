__author__ = 'nunosilva'

from json_recent import SteamJsonRecent
from http import SteamBotHttp
import time

i = 0
http = SteamBotHttp()
js = SteamJsonRecent()
times = []

def median(lst):
    lst = sorted(lst)
    if len(lst) < 1:
            return None
    if len(lst) %2 == 1:
            return lst[((len(lst)+1)/2)-1]
    else:
            return float(sum(lst[(len(lst)/2)-1:(len(lst)/2)+1]))/2.0

while i is not 200:
    start = time.clock()
    recent = {}
    recent = http.urlQueryRecent()
    js.getRecentTotalReady(recent)
    js.getfinalrecentlist()
    i += 1
    print i
    time.sleep(0.5)
    elapsed = time.clock()
    elapsed = elapsed - start
    print elapsed
    times.append(elapsed)

print median(times)