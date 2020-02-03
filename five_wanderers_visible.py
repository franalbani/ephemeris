#!/usr/bin/env python3

from skyfield import api, almanac
from datetime import datetime, timedelta

ts = api.load.timescale()

ephemeris = api.load('de421.bsp')

my_position  = api.Topos('34.606 S', '58.419 W')

# Only naked-eye visible planets:
planets = 'Mercury Venus Mars Jupiter Saturn'.split()

# Collect all boolean functions in one list:
ras = [almanac.risings_and_settings(ephemeris, ephemeris[p + '_barycenter'], my_position)
       for p in planets]

# Append one for checking that the Sun is down:
is_sun_down = lambda t: not almanac.sunrise_sunset(ephemeris, my_position)(t)
ras.append(is_sun_down)

delta = timedelta(hours=1) # days=0.5)
t = datetime.now(api.utc)

while not all(f(ts.utc(t)) for f in ras):
    t += delta
print(t)

# TODO: allow a minimum elevation
# TODO: take into account Mercury distance from the Sun, to avoid being dazzled by it.
