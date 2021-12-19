#!/usr/bin/env python3
from datetime import datetime, timedelta
from skyfield import almanac, api
from skyfield.api import N, S, W, E, wgs84, load
from skyfield.searchlib import find_discrete
import numpy as np
# https://en.wikipedia.org/wiki/Belt_of_Venus

eph = load('de421.bsp')
ts = load.timescale()
locations = {'Pergamino': wgs84.latlon(33.893021 * S, 60.572294 * W),
             'Córdoba': wgs84.latlon(31.414747 * S, 64.186753 * W)}

selected = 'Pergamino' # 'Córdoba'
sun, moon, earth = eph['sun'], eph['moon'], eph['earth']
place = earth + locations[selected]

def moon_in_venus_belt(ts):

    civil_twilight = almanac.dark_twilight_day(eph, locations[selected])(ts) == 3
    moon_alt, moon_az, _ = place.at(ts).observe(moon).apparent().altaz()
    _, sun_az, _ = place.at(ts).observe(sun).apparent().altaz()
    return  civil_twilight & \
            (0 < moon_alt.degrees) & \
            (moon_alt.degrees < 20) & \
            (((sun_az.degrees > 180) & (moon_az.degrees < 180)) | ((sun_az.degrees < 180) & (moon_az.degrees > 180)))

moon_in_venus_belt.step_days = 1 / (24*60) # every minute

t1 = ts.now()
t2 = t1 + timedelta(days=60) # ts.utc(2022)
t, values = find_discrete(t1, t2, moon_in_venus_belt)

print(f'Próximos tránsitos de la Luna por el cinturón de Venus para ver desde {selected}:')
for t, v in zip(t, values):
    if v == 1: 
        print(t.astimezone(tz=None).strftime("%Y-%m-%d %H:%M"))
