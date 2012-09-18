# -*- coding: utf-8 *-*

from flask.ext.admin import Admin, BaseView, AdminIndexView, expose
from flask.ext.admin.contrib.sqlamodel import ModelView
from flask.ext.admin.contrib.fileadmin import FileAdmin
from flask.ext.login import current_user
from flask import current_app

from webapp import app, db
from webapp.models import *


class AuthMixin(object):

    def is_accessible(self):
        return current_user.is_authenticated() and current_user.admin

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return current_app.login_manager.unauthorized()


class AuthBaseView(AuthMixin, BaseView):
    pass


class AuthModelView(AuthMixin, ModelView):
    pass


class AuthFileAdmin(AuthMixin, FileAdmin):
    pass


class AuthAdminIndexView(AuthMixin, AdminIndexView):
    pass

admin = Admin(app, name='Coin.Box POS', index_view=AuthAdminIndexView())

from .screenshots import *
from .news import *
from .docs import *
from .users import *
