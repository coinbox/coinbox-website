# -*- coding: utf-8 *-*

from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, Blueprint
from flask.ext.markdown import Markdown

from webapp import app, db
from webapp.models import *

Markdown(app)

bp = Blueprint('documentation', __name__, template_folder='templates')


@bp.route("/")
def index():
    description = 'Coin.Box is a POS Software'
    keywords = ['pos', 'point-of-sale', 'software']
    return render_template('documentation.html', template='docs/index.md',
            title='Index',
            meta={'description': description, 'keywords': keywords})


@bp.route("/<path:slug>/")
def page(slug):
    description = 'Coin.Box is a POS Software'
    keywords = ['pos', 'point-of-sale', 'software']

    template_name = 'docs/' + slug + '.md'
    return render_template('documentation.html', template=template_name,
            title=slug.replace('-', ' ').title(),
            meta={'description': description, 'keywords': keywords})

app.register_blueprint(bp, url_prefix='/docs')
