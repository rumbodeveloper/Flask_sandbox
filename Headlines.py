#! /usr/bin/env python
# -*- coding: UTF-8 -*-

#
# This program does:
# Flask --> website Headlines, a RSS aggregator
#
#Author: Rumbo181
#
#Date: '13/5/16'

import feedparser
from flask import Flask, render_template

app = Flask(__name__)



RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn':'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol':'http://www.iol.co.za/cmlink/1.640',
             'elpais':'feed://ep00.epimg.net/rss/elpais/portada.xml',
             'elmundo':'feed://estaticos.elmundo.es/elmundo/rss/portada.xml'}



@app.route('/')
@app.route("/<publication>")
def get_news(publication='elpais'):
    feed = feedparser.parse(RSS_FEEDS[publication])
    return render_template("home.html",
                           articles = feed['entries'][:5],
                           )

if __name__ == '__main__':
    app.run(port=5000, debug=True)

