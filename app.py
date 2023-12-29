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
from datetime import datetime

app = Flask(__name__)

#replace 'postgres' to 'postgresql'
heroku_config_databaseurl_env = os.getenv("DATABASE_URL")
database_uri = re.sub(r'(postgres)', r'\1ql', heroku_config_databaseurl_env)

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"

@login_manager.user_loader
def load_user(user_id):
    """get user from database"""
    return Passcode.query.get(int(user_id))


# define models


"""
 Newsletter table datamodel object
 """
class Newsletter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String)
    date =  db.Column(db.String)

"""
Passcode table datamodel object
"""
class Passcode(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String)

"""
Login form object
"""
class LoginForm(FlaskForm):
    passcode = PasswordField(
        validators=[InputRequired()],
        render_kw={"placeholder":" Enter passcode"}
    )
    submit = SubmitField("Login")


# helper functions


def format_date(date: str) -> str:
    if date != "" and date != None:
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        return date_obj.strftime("%a %d %B %Y")
    return ""

def fmt_newsletter_dates(newsletters):
    for newsletter in newsletters:
            modded_date = format_date(newsletter.date)
            newsletter.date = modded_date

    return newsletters

def get_fmt_newsletters() -> list:
    return fmt_newsletter_dates(db.session.execute(db.select(Newsletter).order_by(desc(Newsletter.date))).scalars().all())


# views


"""
Home Page
"""
@app.route('/')
def index():
    newsletters = get_fmt_newsletters()
    return render_template('home.html', db_data = newsletters[:14])

"""
Login Page
"""
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    user = Passcode.query.get_or_404(1)
    if form.validate_on_submit():
        if bcrypt.check_password_hash(user.password, form.passcode.data):
            login_user(user)
            return redirect('/admin')
        flash("Wrong Passcode")
    return render_template('login.html', form=form)

"""
Admin Page
"""
@app.route('/admin', methods=['POST', 'GET'])
@login_required
def admin():
    if request.method == 'POST':
        newsletter_link = request.form['link']
        newsletter_date = request.form['date']
        new_newsletter = Newsletter(link=newsletter_link, date=newsletter_date)
        db.session.add(new_newsletter)
        db.session.commit()
        return redirect('/admin')
    newsletters = get_fmt_newsletters()
    return render_template('admin.html', db_data = newsletters[:14])

"""
Update Newsletter Page
"""
@app.route('/update/<int:id>', methods=["POST","GET"])
# @login_required
def update(id):
    data = Newsletter.query.get_or_404(id)
    if request.method == 'POST':
        data.link = request.form['link']
        data.date = request.form['date']
        db.session.commit()
        return redirect('/admin')
    else:
        return render_template('update.html', db_data=data)

"""
Delete Newsletter Page
"""
@app.route('/delete/<int:id>', methods=["POST","GET"])
# @login_required
def delete(id):
    pass

"""
Logout Page
"""
@app.route('/logout')
# @login_required
def logout():
    logout_user()
    return redirect("/login")


# start app

# FIXME remove debug=True
if __name__ == "__main__":
    app.run(debug=True)
