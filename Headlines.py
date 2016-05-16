#! /usr/bin/env python
# -*- coding: UTF-8 -*-

#
# This program does:
# Flask --> website Headlines, a RSS aggregator
#
#Author: Rumbo181
#
#Date: '13/5/16'

from constants import OPENWHEATHER_API_KEY
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
            'city': 'Madrid,SPAIN'}



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
    #renderizamos la pagina
    return render_template("home.html", articles=articles, weather=weather)





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




if __name__ == '__main__':
    app.run(port=5000, debug=True)


