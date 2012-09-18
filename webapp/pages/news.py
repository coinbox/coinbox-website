# -*- coding: utf-8 *-*

from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash

from webapp import app, db
from webapp.models import *


@app.route("/news/<slug>")
def news(slug):
    return render_template('news.html')
