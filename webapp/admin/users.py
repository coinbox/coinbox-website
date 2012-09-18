# -*- coding: utf-8 *-*

from webapp import app, db
from webapp.models import *
from webapp.admin import admin, AuthFileAdmin, AuthModelView

from wtforms import Form, TextField, TextAreaField, FileField, PasswordField, \
     BooleanField, SelectField, validators


class UsersView(AuthModelView):
    can_create = True

    list_columns = ('username', 'admin', 'active')
    form_columns = ('username', 'password', 'status')

    form_overrides = dict(password=PasswordField, status=SelectField)
    form_args = dict(
        password=dict(
            default=''
        ),
        status=dict(
            choices=[
                (str(0), 'Not Active'),
                (str(User.ACTIVE), 'Active Not Admin'),
                (str(User.ADMIN), 'Admin Not Active'),
                (str(User.ADMIN | User.ACTIVE), 'Admin And Active')
                ]
            )
        )

    def __init__(self, session, **kwargs):
        super(UsersView, self).__init__(User, session, **kwargs)

    def create_model(self, form):
        if form.data['password'] != '':
            form.password.data = User.encode(form.data['username'],
                                                form.data['password'])
        return super(UsersView, self).create_model(form)

admin.add_view(UsersView(db.session, name='Users', endpoint='users'))
