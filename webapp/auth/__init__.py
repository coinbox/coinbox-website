# -*- coding: utf-8 *-*

from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, Blueprint
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user

from webapp import app, db
from webapp.models import *

login_manager = LoginManager()
login_manager.login_view = "auth.index"
login_manager.setup_app(app)

bp = Blueprint('auth', __name__, template_folder='templates')


@login_manager.user_loader
def load_user(userid):
    return db.session.query(User).filter(User.id == userid).first()


from wtforms import Form, TextField, TextAreaField, FileField, PasswordField, \
     validators


# Login form
class LoginForm(Form):
    """Form used to login into the system"""
    username = TextField('Username', [validators.required()])
    password = PasswordField('Password', [validators.required()])


@bp.route("/")
def index():
    next_url = request.args.get("next")
    if current_user.is_authenticated():
        description = 'Coin.Box is a POS Software'
        keywords = ['pos', 'point-of-sale', 'software']
        return render_template("auth/index.html", user=current_user,
                    meta={'description': description, 'keywords': keywords})
    else:
        return redirect(url_for('auth.login', next=next_url))


@bp.route("/login", methods=["GET", "POST"])
def login():
    next_url = request.args.get("next")
    if not next_url:
        next_url = url_for("auth.index")

    if current_user.is_authenticated():
        return redirect(next_url)

    form = LoginForm()

    if request.method == 'POST':
        form.process(request.form, username='', password='')
        if form.validate():
            user = db.session.query(User) \
                    .filter_by(username=request.form['username'],
                        password=User.encode(request.form['username'],
                                             request.form['password'])) \
                    .first()
            if user:
                login_user(user)
                flash("Logged in successfully.")
                return redirect(next_url)
            else:
                flash('Invalid username/password.', 'error')

    description = 'Coin.Box is a POS Software'
    keywords = ['pos', 'point-of-sale', 'software']
    return render_template("auth/login.html", form=form,
                meta={'description': description, 'keywords': keywords})


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for("index"))

app.register_blueprint(bp, url_prefix='/users')
