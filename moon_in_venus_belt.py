#!/usr/bin/env python3
from datetime import datetime, timedelta
from skyfield import almanac, api
from skyfield.api import N, S, W, E, wgs84, load

# https://en.wikipedia.org/wiki/Belt_of_Venus

eph = load('de421.bsp')
ts = load.timescale()
locations = {'Pergamino': wgs84.latlon(33.893021 * S, 60.572294 * W),
             'Córdoba': wgs84.latlon(31.414747 * S, 64.186753 * W)}

selected = 'Córdoba'
sun, moon, earth = eph['sun'], eph['moon'], eph['earth']
place = earth + locations[selected]


def is_civil_twilight(t):
    return almanac.dark_twilight_day(eph, locations[selected])(t) == 3

def is_moon_under_20_deg(t):
    moon_astrometric = place.at(t).observe(moon)
    moon_apparent = moon_astrometric.apparent()
    moon_alt, moon_az, _ = moon_apparent.altaz()
    sun_astrometric = place.at(t).observe(sun)
    sun_apparent = sun_astrometric.apparent()
    _, sun_az, _ = sun_apparent.altaz()
    return (0 < moon_alt.degrees < 20) and (((sun_az.degrees > 180) and (moon_az.degrees < 180)) or ((sun_az.degrees < 180) and (moon_az.degrees > 180)))

conditions = []
conditions.append(is_civil_twilight)
conditions.append(is_moon_under_20_deg)

t = datetime.now(api.utc)

q = 10
found = []
print(f'Próximos {q} tránsitos de la Luna por el cinturón de Venus para ver desde {selected}:')
while len(found) < q:
    if all(f(ts.utc(t)) for f in conditions):
        found.append(t)
        print(f'Hora local: {t.astimezone()}')
        t += timedelta(hours=1) # Esto se puede optimizar bastante haciendo deducciones geométricas
    else:
        t += timedelta(minutes=1)
