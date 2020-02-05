from main import db,app
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime



class Expense(db.Model):  
    """ Expenses model """  
    __tablename__ = "expenses"
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.Date(), default=datetime.utcnow)
    expensename= db.Column(db.String(25),  nullable=False)
    desc= db.Column(db.String(25), nullable=False)
    amount=db.Column(db.Integer, nullable=False)
    
