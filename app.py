from datetime import date
from os import link
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class newsletter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String)
    date =  db.Column(db.String)

@app.route('/')
def index():
    db_data = newsletter.query.order_by(desc(newsletter.id))
    return render_template('home.html', db_data = db_data)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if request.method == 'POST':
        newsletter_link = request.form['link']
        newsletter_date = request.form['date']
        new_newsletter = newsletter(link=newsletter_link, date=newsletter_date)
        db.session.add(new_newsletter)
        db.session.commit()
        return redirect('/admin')
    else:
        db_data = newsletter.query.order_by(desc(newsletter.id))
        return render_template('admin.html', db_data = db_data)

@app.route('/update/<int:id>', methods=["POST","GET"])
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
def logout():
    pass

if __name__ == "__main__":
    app.run(debug=True)