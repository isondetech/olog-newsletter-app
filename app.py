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
    link = db.Column(db.String, default ="null")
    date =  db.Column(db.Date, default="null")

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/admin', methods=['POST', 'GET'])
def admin():
    return render_template('admin.html')

@app.route('/update', methods=["POST","GET"])
def update():
    return render_template('update.html')

@app.route('/logout')
def logout():
    pass

if __name__ == "__main__":
    app.run(debug=True)