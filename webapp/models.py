# -*- coding: utf-8 *-*
__all__ = ['NewsArticle', 'Screenshot', 'User']

import webapp

from flask import url_for

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property

webapp.app.config['SQLALCHEMY_ECHO'] = False
webapp.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:pass@localhost/coinboxweb'
db = webapp.db = SQLAlchemy(webapp.app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    status = db.Column(db.Integer, default=0)

    ACTIVE = 1
    ADMIN = 2

    @classmethod
    def encode(self, username, password):
        import sha
        s = username + webapp.app.config['SECRET_KEY'] + password
        encoded = sha.sha(s).hexdigest()
        return encoded

    @hybrid_property
    def active(self):
        return (self.status & User.ACTIVE) != 0

    @active.expression
    def active(self):
        return (self.status & User.ACTIVE) != 0

    @active.setter
    def active(self, prop):
        if prop:
            self.status |= self.ACTIVE
        else:
            self.status ^= self.ACTIVE

    @hybrid_property
    def admin(self):
        return (self.status & User.ADMIN) != 0

    @admin.expression
    def admin(self):
        return (self.status & User.ADMIN) != 0

    @admin.setter
    def admin(self, prop):
        if prop:
            self.status |= self.ADMIN
        else:
            self.status ^= self.ADMIN

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)


class NewsArticle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(255))
    title = db.Column(db.String(255), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=db.func.now())

    def __init__(self, *args, **kwargs):
        super(NewsArticle, self).__init__(*args, **kwargs)

    @hybrid_property
    def time_diff(self):
        from datetime import datetime
        now = datetime.now()
        return now - self.date_created

    def time_ago(self):
        diff = self.time_diff

        if diff.days > 1:
            return '%d days ago' % (diff.days,)
        elif diff.days == 1:
            return 'yesterday'

        hours = round(diff.seconds / 3600.0)
        if hours > 1:
            return '%d hours ago' % (hours,)
        elif hours == 1:
            return 'an hour ago'

        minutes = round(diff.seconds / 60.0)
        if minutes > 1:
            return '%d minutes ago' % (minutes,)
        elif minutes == 1:
            return 'a minute ago'

        return 'few moments ago'


class Screenshot(db.Model):
    filename = db.Column(db.String(255), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    alt = db.Column(db.String(255), nullable=False)

    @hybrid_property
    def thumb_url(self):
        return url_for('static', filename='screenshots/thumb/' + self.filename)

    @hybrid_property
    def image_url(self):
        return url_for('static', filename='screenshots/' + self.filename)
