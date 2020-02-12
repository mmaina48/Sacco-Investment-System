from main import db,app
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime


login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

class User(UserMixin, db.Model):  
    """ User model """  
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    role = db.Column(db.String(), nullable=False)

class Expense(db.Model):  
    """ Expenses model """  
    __tablename__ = "expenses"
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.Date(), default=datetime.utcnow)
    expensename= db.Column(db.String(25),  nullable=False)
    amount=db.Column(db.Integer, nullable=False)
    
class Member(db.Model):  
    """ Members model """  
    __tablename__ = "member"
    id = db.Column(db.Integer, primary_key=True)
    membername= db.Column(db.String(25), unique=True, nullable=False)
    created_on = db.Column(db.Date(), default=datetime.utcnow)
    memberphone= db.Column(db.String(25), unique=True,nullable=False)
    amount=db.Column(db.Integer,default=0)
    contribution = db.relationship('Contribution', backref='member')
    
class Contribution(db.Model):
    """contributions model """  
    __tablename__ = "contribution"
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.Date(), default=datetime.utcnow)
    membername = db.Column(db.String(25), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    member_id = db.Column(db.Integer(), db.ForeignKey('member.id'))  # Foreign keyp

     