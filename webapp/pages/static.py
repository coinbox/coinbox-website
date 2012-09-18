# -*- coding: utf-8 *-*

from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash

from webapp import app, db
from webapp.models import *


@app.route("/about")
def about():
    description = 'Coin.Box is a POS Software'
    keywords = ['pos', 'point-of-sale', 'software']

    return render_template('about.html',
            meta={'description': description, 'keywords': keywords})


@app.route("/download")
def download():
    description = 'Coin.Box is a POS Software'
    keywords = ['pos', 'point-of-sale', 'software']

    class Download(object):
        version = '1.1.0'
        size = '2MB'
        platform = 'win32'
        format = 'zip'
    download = Download()

    return render_template('download.html',
            meta={'description': description, 'keywords': keywords},
            latest=download)


@app.route("/download/<version>")
@app.route("/download/<platform>")
def direct_download(version=None, platform=None):
    return 'Not Found Here!', 404

@app.route("/help")
def faq():
    description = 'Coin.Box is a POS Software'
    keywords = ['pos', 'point-of-sale', 'software']

    return render_template('faq.html',
                meta={'description': description, 'keywords': keywords}
                )


@app.route("/support")
def support():
    description = 'Coin.Box is a POS Software'
    keywords = ['pos', 'point-of-sale', 'software']

    return render_template('faq.html',
                meta={'description': description, 'keywords': keywords}
                )
