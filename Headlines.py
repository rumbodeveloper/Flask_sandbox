#! /usr/bin/env python
# -*- coding: UTF-8 -*-

#
# This program does:
# Flask --> website Headlines, a RSS aggregator
#
#Author: Rumbo181
#
#Date: '13/5/16'

from constants import OPENWHEATHER_API_KEY, OPENEXHANGE_API_KEY
import json
import feedparser
from flask import Flask, render_template, request
import urllib2
import urllib


app = Flask(__name__)



RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn':'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'elpais':'feed://ep00.epimg.net/rss/elpais/portada.xml',}

DEFAULTS = {'publication': 'elpais',
            'city': 'Madrid,SPAIN',
            'currency_from':'EUR',
            'currency_to':'USD',}



@app.route('/')
@app.route("/<publication>")
def home():
    #obtener noticias de ultima hora customizadas
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)
    #obtener el tiempo customizado
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
    #obtener un ratio de cambio customizado
    currency_from = request.args.get('currency_from')
    currency_to = request.args.get('currrency_to')
    if not currency_from:
        currency_from = DEFAULTS['currency_from']
    if not currency_to:
        currency_to = DEFAULTS['currency_to']
    rate,currencies = get_rates(currency_from,currency_to)

    #renderizamos la pagina
    return render_template("home.html",
                           articles=articles,
                           weather=weather,
                           currency_from=currency_from,
                           currency_to=currency_to,
                           rate=rate,
                           currencies=sorted(currencies)
                           )





def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publication']
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries'][:5]

def get_weather(query):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid="+OPENWHEATHER_API_KEY
    query = urllib.quote(query)
    url = api_url.format(query)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description": parsed["weather"][0]["description"],
                   "temperature": parsed["main"]["temp"],
                   "city": parsed["name"],
                   "country": parsed['sys']['country']}
    return weather


def get_rates(frm,to):
    currency_url="https://openexchangerates.org//api/latest.json?app_id={}".format(OPENEXHANGE_API_KEY)
    all_currency = urllib2.urlopen(currency_url).read()
    parsed = json.loads(all_currency).get('rates')
    frm_rate=parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return (to_rate/frm_rate,parsed.keys())




if __name__ == '__main__':
    app.run(port=5000, debug=True)


