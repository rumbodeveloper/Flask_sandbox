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
import datetime
import json
import feedparser
from flask import  render_template, request, make_response, send_from_directory
from os.path import join
import urllib2
import urllib

from . import main





RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn':'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'elpais':'feed://ep00.epimg.net/rss/elpais/portada.xml',
             'confi': 'http://rss.elconfidencial.com/espana/',
             'mercados': 'http://rss.elconfidencial.com/mercados/',}

DEFAULTS = {'publication': 'elpais',
            'city': 'Madrid,SPAIN',
            'currency_from':'BTC',
            'currency_to':'EUR',}



@main.route('/')
@main.route("/<publication>")
def home():


    #obtener noticias de ultima hora customizadas
    publication = get_value_with_fallback("publication")
    articles = get_news(publication)
    publications = sorted(RSS_FEEDS.keys())

    #obtener el tiempo customizado
    city = get_value_with_fallback('city')
    weather = get_weather(city)

    #obtener un ratio de cambio customizado
    currency_from = get_value_with_fallback('currency_from')
    currency_to = get_value_with_fallback('currency_to')
    rate,currencies = get_rates(currency_from,currency_to)

    #renderizamos la pagina
    response = make_response(render_template("home.html",
                           publications =publications,
                           articles=articles,
                           weather=weather,
                           currency_from=currency_from,
                           currency_to=currency_to,
                           rate=rate,
                           currencies=sorted(currencies)))
    expires = datetime.datetime.now()+datetime.timedelta(days=7)
    response.set_cookie("publication",publication,expires=expires)
    response.set_cookie("city",city,expires=expires)
    response.set_cookie("currency_from",currency_from,expires=expires)
    response.set_cookie("currency_to",currency_to,expires=expires)
    return response


@main.route("/politica_de_cookies")
def politica_de_cookies():
    ''' pagina con la politica de cookies'''
    return render_template("cookie_policy.html")

@main.route("/robots.txt")
def robots():
    ''' devuelve el fichero robots.txt '''
    return send_from_directory(join(app.static_folder,"txt"),"robots.txt")

@main.route('/favicon.ico')
def favicon():
    '''devuelve un favicon propio'''
    return send_from_directory(join(app.static_folder, 'favicon'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')






def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publication']
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries'][:8]

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
    return ("{:.2f}".format(to_rate/frm_rate),parsed.keys())

def get_value_with_fallback(key):
    '''Function to handle retrieved cookies
    its simply an ordereded loop-up'''
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]





