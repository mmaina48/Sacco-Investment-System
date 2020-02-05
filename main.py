from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///saccodb.sqlite3'
app.config['SECRET_KEY'] = 'Secterettttbayy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db= SQLAlchemy(app)

from routes import *

db.create_all()
db.session.commit()