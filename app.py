import os
from flask import Flask, render_template, request, flash
from flask.helpers import flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
from sqlalchemy import desc
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import  InputRequired
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://vptwrfkdnoaciq:4b873f593cba6369ef236'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '&_ux{2&4?GLQ8@y7'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"

@login_manager.user_loader
def load_user(user_id):
    return passcode.query.get(int(user_id))

class newsletter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String)
    date =  db.Column(db.String)

class passcode(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(80))

class LoginForm(FlaskForm):
    passcode = PasswordField(validators=[InputRequired()],render_kw={"placeholder":" Enter passcode"})
    submit = SubmitField("Login")


@app.route('/')
def index():
    db_data = newsletter.query.order_by(desc(newsletter.id))
    return render_template('home.html', db_data = db_data[:14])

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    user = passcode.query.get_or_404(2)
    if form.validate_on_submit():
        if bcrypt.check_password_hash(user.password, form.passcode.data):
            login_user(user)
            return redirect('/admin')
        else:
            flash("Wrong Passcode")
    return render_template('login.html', form=form)

@app.route('/admin', methods=['POST', 'GET'])
@login_required
def admin():
    if request.method == 'POST':
        newsletter_link = request.form['link']
        newsletter_date = request.form['date']
        new_newsletter = newsletter(link=newsletter_link, date=newsletter_date)
        db.session.add(new_newsletter)
        db.session.commit()
        # db_data = newsletter.query.all()
        return redirect('/admin')
    else:
        db_data = newsletter.query.order_by(desc(newsletter.id))
        return render_template('admin.html', db_data = db_data[:14])

@app.route('/update/<int:id>', methods=["POST","GET"])
@login_required
def update(id):
    data = newsletter.query.get_or_404(id)
    if request.method == 'POST':
        data.link = request.form['link']
        data.date = request.form['date']
        db.session.commit()
        return redirect('/admin')
    else:
        return render_template('update.html', db_data=data)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)