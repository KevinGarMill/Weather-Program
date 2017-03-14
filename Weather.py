#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf8 :

import sys
import urllib2
import json
from optparse import OptionParser

api_key = None


class WeatherClient(object):

    url_base = "http://api.wunderground.com/api/"
    url_service = {
        "hourly": "/hourly/q/Spain/",
        "astronomy": "/astronomy/q/Spain/",
        "conditions": "/conditions/q/Spain/"
    }

    def __init__(self, arg):
        super(WeatherClient, self).__init__()
        self.api_key = api_key

    def get_json(self, location, feacture):
                url = WeatherClient.url_base + self.api_key + \
                    WeatherClient.url_service[feacture] + location + ".json"
                f = urllib2.urlopen(url)
                data = f.read()
                f.close()
                return json.loads(data)

    def hourly_forecast(self, location):
        # adquirir datos de la pagina web
        data = self.get_json(location, "hourly")
        hourly_forecast = []

        # procesar resultados
        for element in data["hourly_forecast"]:
            tmp_list = []
            tmp_list.append(element["FCTTIME"]["civil"])
            tmp_list.append(element["temp"]["metric"])
            tmp_list.append(element["condition"])
            hourly_forecast.append(tmp_list)

        # devolver resultados
        print "Forecast for the next hours:"
        for hour in hourly_forecast:
            print "    Time: " + hour[0]
            print "        Temperature: " + hour[1]
            print "        Forecast: " + hour[2] + "\n"

    def astronomy(self, location):
        data = self.get_json(location, "astronomy")
        astronomy = []

        # procesar resultados
        astronomy.append(data["moon_phase"]["sunrise"])
        astronomy.append(data["moon_phase"]["sunset"])
        astronomy.append(data["moon_phase"]["moonrise"])
        astronomy.append(data["moon_phase"]["moonset"])

        # devolver resultados
        print "Astronomy, Sun phase and Moon phase:"
        print "    Sunrise for today: " + astronomy[0]["hour"] + ":" + astronomy[0]["minute"]
        print "    Sunset for today: " + astronomy[1]["hour"] + ":" + astronomy[1]["minute"]
        print "    Moonrise for today: " + astronomy[2]["hour"] + ":"+astronomy[2]["minute"]
        print "    Moonset for today: " + astronomy[3]["hour"] + ":"+astronomy[3]["minute"] + "\n"

    def conditions(self, location):
        # adquirir datos de la pagina web
        data = self.get_json(location, "conditions")
        conditions = []

        # procesar resultados
        conditions.append(data["current_observation"]["observation_time_rfc822"])
        conditions.append(data["current_observation"]["relative_humidity"])
        conditions.append(data["current_observation"]["wind_string"])
        conditions.append(data["current_observation"]["pressure_mb"])

        # devolver resultados
        print "Conditions:"
        print "    Time of observation: " + conditions[0]
        print "    Humidity: " + conditions[1]
        print "    Wind information: " + conditions[2]
        print "    Presure in millibars: " + conditions[3]


if __name__ == "__main__":
    usage = "ussage: %Weather.py -k arg1 [options]"
    parser = OptionParser(usage=usage)

    parser.add_option("-f", action="store_true", dest="hourly",
        default=False, help="show a forecast for the next hours")
    parser.add_option("-a", action="store_true", dest="astronomy",
        default=False, help="show the sunrise, sunset, moonrise and moonset")
    parser.add_option("-c", action="store_true", dest="conditions",
        default=False, help="show some weather conditions")
    parser.add_option("-k", action="store", type="string", dest="key",
        help="key necesary to connect with the api")

    (options, args) = parser.parse_args()

    if not options.key:
        parser.error("A key is necesary, introduce: 'Weather.py -k <api_key>'")
    if not (options.astronomy or options.hourly or options.conditions):
        parser.error("Introduce atleast one option: '-a' '-c' '-f'")

    active_hourly = options.hourly
    active_astronomy = options.astronomy
    active_conditions = options.conditions
    api_key = options.key

    wc = WeatherClient(api_key)

    if active_hourly:
        wc.hourly_forecast("Lleida")

    if active_astronomy:
        wc.astronomy("Lleida")

    if active_conditions:
        wc.conditions("Lleida")
