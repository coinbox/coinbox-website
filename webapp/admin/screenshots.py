# -*- coding: utf-8 *-*

from flask.ext import wtf

from werkzeug import secure_filename
import os.path

from webapp import app, db
from webapp.models import *
from webapp.admin import admin, AuthFileAdmin, AuthModelView


class ScreenshotView(AuthModelView):
    can_create = True

    # Override displayed fields
    list_columns = ('title', 'filename', 'alt')

    form_columns = ('title', 'alt', 'filename')
    form_overrides = dict(filename=wtf.FileField)

    def __init__(self, session, **kwargs):
        super(ScreenshotView, self).__init__(Screenshot, session, **kwargs)

    def create_model(self, form):
        upload = form.filename.data
        path = os.path.join(app.root_path, 'static', 'screenshots')
        thumb_path = os.path.join(app.root_path, 'static', 'screenshots',
                                    'thumb')

        filename = secure_filename(upload.filename)
        filepath = os.path.join(path, filename)
        thumb_filepath = os.path.join(thumb_path, filename)

        from PIL import Image
        upload.save(filepath)
        img = Image.open(filepath)
        thumb = img.resize((100, 100))
        thumb.save(thumb_filepath)

        form.filename.data = filename

        return super(ScreenshotView, self).create_model(form)


class ScreenshotFilesView(AuthFileAdmin):

    def __init__(self, **kwargs):
        path = os.path.join(app.root_path, 'static', 'screenshots')
        super(ScreenshotFilesView, self).__init__(path, '/static/screenshots/',
                                                    **kwargs)

admin.add_view(ScreenshotView(db.session, name='Manage', endpoint='screenshots',
                            category='Screenshots'))
admin.add_view(ScreenshotFilesView(name='Files', endpoint='screenshot-files',
                            category='Screenshots'))
