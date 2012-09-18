# -*- coding: utf-8 *-*
from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = '1238qjwidj4t8ijdfsasd'

from .models import *
from .pages import *
from .docs import *
from .admin import *

from .auth import *

def run(*args, **kwargs):
    app.run(*args, **kwargs)
