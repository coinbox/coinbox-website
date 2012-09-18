# -*- coding: utf-8 *-*

from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
import twitter

from webapp import app, db
from webapp.models import *


@app.route("/")
def index():
    mission = '''
We at Coin Box POS desire to create an elegant yet advanced business tool.
We want to accomplish this by simplicity, and flexibility.
By simplicity creating an easy user environment that "just makes sense";
and by flexibility creating software that is helpful for many business types,
but also customizable.
'''
    description = 'Coin.Box is a POS Software'
    keywords = ['pos', 'point-of-sale', 'software']
    news = db.session.query(NewsArticle) \
            .order_by(NewsArticle.date_created.desc()) \
            .limit(5)
    #tweets = twitter.Api().GetSearch(term='#flask OR @flask', per_page=5)

    screenshots = db.session.query(Screenshot) \
            .limit(20)

    return render_template('index.html',
            mission=mission,
            meta={'description': description, 'keywords': keywords},
            news=news, gallery=screenshots)
