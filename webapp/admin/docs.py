# -*- coding: utf-8 *-*

import os.path

from webapp import app, db
from webapp.models import *
from webapp.admin import admin, AuthFileAdmin, AuthModelView, AuthBaseView

from flask import redirect, url_for, request, flash
from flask.ext.admin import expose
from flask.ext.admin.actions import action

from wtforms import Form, TextField, TextAreaField, FileField, PasswordField, \
     validators


class EditForm(Form):
    content = TextAreaField('Content', [validators.required()])


class DocsFilesView(AuthFileAdmin):

    allowed_extensions = ('md', 'html')

    def __init__(self, **kwargs):
        super(DocsFilesView, self).__init__(self.docs_path(''),
                                            None,
                                            **kwargs)

    def get_base_url(self):
        if self.base_url is None:
            return url_for(".edit", path='')
        else:
            return self.base_url

    def docs_path(self, path=None):
        path = '' if path is None else path
        return os.path.join(app.root_path, 'docs', 'templates', 'docs', path)

    @expose('/edit/<path:path>', methods=('GET', 'POST'))
    # TODO: gettext integration
    @action('edit', 'Edit')
    def edit(self, path):
        next_url = None
        if not path:
            return redirect(url_for('.index'))
        elif isinstance(path, (list, tuple)):
            if len(path) > 1:
                next_url = url_for('.edit', path='|'.join(path[1:]))
            path = path[0]
        else:
            path = path.split('|')
            if len(path) > 1:
                next_url = url_for('.edit', path='|'.join(path[1:]))
            path = path[0]

        base_path, full_path, path = self._normalize_path(path)
        dir_url = self._get_dir_url('.index', os.path.dirname(path))
        next_url = next_url or dir_url

        form = EditForm()
        if request.method == 'POST':
            form.process(request.form, content='')
            if form.validate():
                try:
                    with open(full_path, 'w') as f:
                        f.write(request.form['content'])
                except IOError:
                    flash("Error saving changes to file!", 'error')
                else:
                    flash("Changes saved successfully!")
                    return redirect(next_url)
        else:
            with open(full_path, 'r') as f:
                form.content.data = f.read()
        return self.render('edit_docs.html', dir_url=dir_url, form=form,
                            path=path)

admin.add_view(DocsFilesView(name='Docs', endpoint='docs'))
