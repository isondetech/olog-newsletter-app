"""
This module serves olognewsletter.heroku.com pages
"""
import os
import re

from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
from sqlalchemy import desc
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import  InputRequired
from flask_bcrypt import Bcrypt

import fmtdate

app = Flask(__name__)

#FIXME this can be changed in Heroku
#replace 'postgres' to 'postgresql'
heroku_config_databaseurl_env = os.getenv("DATABASE_URL")
database_uri = re.sub(r'(postgres)', r'\1ql', heroku_config_databaseurl_env)

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#FIXME add as variable in heroku
app.config['SECRET_KEY'] = '&_ux{2&4?GLQ8@y7'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"

@login_manager.user_loader
def load_user(user_id):
    """get user from database"""
    return Passcode.query.get(int(user_id))

class Newsletter(db.Model):
    """newsletter datamodel object"""
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String)
    date =  db.Column(db.String)

class Passcode(db.Model, UserMixin):
    """passcode datamodel object"""
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String)

class LoginForm(FlaskForm):
    """login form object"""
    passcode = PasswordField(
        validators=[InputRequired()],
        render_kw={"placeholder":" Enter passcode"}
    )
    submit = SubmitField("Login")


@app.route('/')
def index():
    """Home page"""
    db_data = Newsletter.query.order_by(desc(Newsletter.id))
    return render_template('home.html', db_data = db_data[:14])

@app.route('/login', methods=['GET','POST'])
def login():
    """Login page"""
    form = LoginForm()
    user = Passcode.query.get_or_404(1)
    if form.validate_on_submit():
        if bcrypt.check_password_hash(user.password, form.passcode.data):
            login_user(user)
            return redirect('/admin')
    flash("Wrong Passcode")
    return render_template('login.html', form=form)

@app.route('/admin', methods=['POST', 'GET'])
@login_required
def admin():
    """Admin page"""
    if request.method == 'POST':
        newsletter_link = request.form['link']
        newsletter_date = fmtdate.format_date(request.form['date'])
        new_newsletter = Newsletter(link=newsletter_link, date=newsletter_date)
        db.session.add(new_newsletter)
        db.session.commit()
        return redirect('/admin')
    db_data = Newsletter.query.order_by(desc(Newsletter.id))
    return render_template('admin.html', db_data = db_data[:14])

@app.route('/update/<int:id>', methods=["POST","GET"])
@login_required
def update(id):
    """update page"""
    data = Newsletter.query.get_or_404(id)
    if request.method == 'POST':
        data.link = request.form['link']
        data.date = fmtdate.format_date(request.form['date'])
        db.session.commit()
        return redirect('/admin')
    else:
        return render_template('update.html', db_data=data)

@app.route('/logout')
@login_required
def logout():
    """Logout a user"""
    logout_user()
    return redirect("/login")

if __name__ == "__main__":
    app.run()
