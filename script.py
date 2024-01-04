from gtts import gTTS
from metar_gg import MetarGG
from tokenizer import Tokenizer
from types import SimpleNamespace
from utils import Utils

import datetime
import json
import os
import requests

utils = Utils()

airport_code = os.getenv('ICAO', 'KIND')
weather_url = 'https://aviationweather.gov/api/data/metar?ids={}&format=json'.format(airport_code)
data = requests.get(weather_url)
weather = json.loads(data.text, object_hook=lambda d: SimpleNamespace(**d))[0]

# Location
start = MetarGG().location(airport_code)
start += 'Automated weather observation. '

# Observation time
observation_timestamp = datetime.datetime.fromtimestamp(weather.obsTime)

observation_tts_string = '{}{} zulu. '.format(
  utils.zero_pad(observation_timestamp.hour), \
  utils.zero_pad(observation_timestamp.minute)
)

# Wind
wind_degrees = weather.wdir

if isinstance(wind_degrees, str):
  wind_degrees = wind_degrees.replace('VRB', 'variable')

wind_speed = utils.zero_pad(weather.wspd)
wind_tts_string = 'Wind {} at {}. '.format(wind_degrees, wind_speed)

# Visibility
vis = utils.zero_pad(weather.visib)
vis_tts_string = 'Visibility {}. '.format(vis)

# Sky conditions (clouds)
clouds_tts_string = 'Sky conditions '

for sky_cond in weather.clouds:
  cover = sky_cond.cover.replace('BKN', 'broken') \
    .replace('FEW', 'few') \
    .replace('OVC', 'overcast') \
    .replace('SCT', 'scattered') \

  base = sky_cond.base
  uom = 'feet'

  if sky_cond.base >= 1000:
    base = int(sky_cond.base / 1000)
    uom = 'thousand'

  clouds_tts_string += '{} at {} {}.'.format(cover, base, uom)

clouds_tts_string += '.'

# Temperature
temp = utils.zero_pad(round(weather.temp), True)
temp_tts_string = 'Temperature {} Celsius. '.format(temp)

# Dewpoint
dewpoint = utils.zero_pad(round(weather.dewp), True)
dewpoint_tts_string = 'Dewpoint {} Celsius. '.format(dewpoint)

# Pressure
altimeter = round(weather.altim * 0.02952998057228486, 2)
alt_string = str(altimeter).replace('.', '')
alt_tts_string = 'Altimeter {}. '.format(alt_string)

# Remarks (density altitude)

output_text = start \
  + observation_tts_string \
  + wind_tts_string \
  + vis_tts_string \
  + clouds_tts_string \
  + temp_tts_string \
  + dewpoint_tts_string \
  + alt_tts_string

output_text = Tokenizer().tokenize(output_text)

tts = gTTS(output_text, slow=False)

tts.save('output.mp3')
