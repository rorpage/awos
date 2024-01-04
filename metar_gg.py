from types import SimpleNamespace

import json
import requests

class MetarGG:
  def _query_metargg(self, data):
    url = 'https://api.metar.gg/graphql'
    data = requests.post(url, json=data)

    return json.loads(data.text, object_hook=lambda d: SimpleNamespace(**d))

  def location(self, airport_code):
    data = {'query': 'fragment AirportSearch on Airport { name } query GetSingleAirport($identifier: String!) { getAirport(identifier: $identifier) { ...AirportSearch }}', 'variables': {'identifier': airport_code}}
    weather = self._query_metargg(data)

    name = weather.data.getAirport.name.replace('Airpark', 'air park')

    return '{}. '.format(name)
