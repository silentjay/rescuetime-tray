# coding: utf-8
import json
import urllib2
from datetime import date, timedelta

import pandas as pd

from rescuetime.api.service import Service
from rescuetime.api.access import AnalyticApiKey


def get_apikey():
    with open("apikey", "r") as fileo:
        key = fileo.read().rstrip('\n')
	print key
    return key


apikey = get_apikey()


def get_efficiency():
    try:
        todays_date = date.today().strftime("%Y-%m-%d")
        data = urllib2.urlopen("https://www.rescuetime.com/anapi/data?key=%s&restrict_kind=efficiency&resolution_time=day&restrict_begin=%s&restrict_end=%s&format=json&perspective=interval" % (apikey, todays_date, todays_date)).read()
        data = json.loads(data)
        print data
        prod_pulse = data['rows'][0][4]
        print 'prod_pulse: %s' % prod_pulse
        #return int(prod_pulse), str(time_logged)
        return int(prod_pulse)
    except Exception as e:
        print e
        print "returning 'F'"
        return "F"


# def update_stats():


    # self.title = prod_pulse
    # self.menu['Logged'].title = seconds_to_datestr(time_logged)
    # return prod_pulse, seconds_to_datestr(time_logged)

def seconds_to_datestr(seconds):
  m, s = divmod(seconds, 60)
  h, m = divmod(m, 60)
  return "%d:%02d:%02d" % (h, m, s)
