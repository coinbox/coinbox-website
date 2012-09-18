# -*- coding: utf-8 *-*

from webapp import app, db
from webapp.models import *
from webapp.admin import admin, AuthFileAdmin, AuthModelView

from unicodedata import normalize

# Slug (https://gist.github.com/1428479)
# https://bitbucket.org/r0sk/flaskblog/src/2f57d47347fd/blog.py#cl-46
def make_slug(text, encoding=None,
         permitted_chars='abcdefghijklmnopqrstuvwxyz0123456789-'):
    if isinstance(text, str):
        text = text.decode(encoding or 'utf-8')
    clean_text = text.strip().replace(' ', '-').lower()
    while '--' in clean_text:
        clean_text = clean_text.replace('--', '-')
    ascii_text = normalize('NFKD', clean_text).encode('ascii', 'ignore')
    strict_text = map(lambda x: x if x in permitted_chars else '', ascii_text)
    return unicode(''.join(strict_text))


class NewsView(AuthModelView):
    can_create = True

    list_columns = ('title', 'slug', 'date_created')
    form_columns = ('slug', 'title', 'summary')

    def __init__(self, session, **kwargs):
        super(NewsView, self).__init__(NewsArticle, session, **kwargs)

    def create_model(self, form):
        if form.data['slug'] == '':
            form.slug.data = make_slug(form.data['title'])
        return super(NewsView, self).create_model(form)

admin.add_view(NewsView(db.session, name='News', endpoint='news'))
