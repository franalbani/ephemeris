#!/usr/bin/env python3
from datetime import datetime, timedelta
from skyfield import almanac, api
from skyfield.api import N, S, W, E, wgs84, load

# https://en.wikipedia.org/wiki/Belt_of_Venus

eph = load('de421.bsp')
ts = load.timescale()
locations = {'pergamino': wgs84.latlon(33.893021 * S, 60.572294 * W),
             'cordoba': wgs84.latlon(31.414747 * S, 64.186753 * W)}

selected = 'cordoba'
moon, earth = eph['moon'], eph['earth']
place = earth + locations[selected]


def is_civil_twilight(t):
    return almanac.dark_twilight_day(eph, locations[selected])(t) == 3

def is_moon_under_20_deg(t):
    astrometric = place.at(t).observe(moon)
    apparent = astrometric.apparent()
    alt, az, distance = apparent.altaz()
    return 0 < alt.degrees and alt.degrees < 20

conditions = []
conditions.append(is_civil_twilight)
conditions.append(is_moon_under_20_deg)

t = datetime.now(api.utc)

delta = timedelta(minutes=1) # days=0.5)
while not all(f(ts.utc(t)) for f in conditions):
    t += delta
print(t)
