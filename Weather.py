#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf8 :

import sys
import urllib2

import json

api_key = None


class WeatherClient(object):

    url_base = "http://api.wunderground.com/api/"
    url_service = {
        "hourly": "/hourly/q/Spain/"
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
            print "    Time: "+hour[0]
            print "        Temperature: "+hour[1]
            print "        Forecast: "+hour[2]+"\n"


if __name__ == "__main__":
    if not api_key:
        try:
            api_key = sys.argv[1]
        except IndexError:
            print "Api Key must be in CLI option"

    wc = WeatherClient(api_key)

    print wc.hourly_forecast("LLeida")
