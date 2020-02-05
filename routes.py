from flask import Flask, render_template
from flask import  render_template,url_for,redirect,flash,request
# from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from main import app,db
from forms import addexpense
from models import Expense
import time,datetime
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash




@app.route('/')
def dashboard():
    exp = Expense.query.all()
    explist=[]
    for e in exp:
        explist.append(e.amount)

    totalexp=sum(explist)
    return render_template('dashboard.html', exp=exp , totalexp=totalexp)

#Create an expense
@app.route('/Addexpense/', methods=['GET','POST'])
def addExpense():
    form = addexpense()
    if form.validate_on_submit() and request.method == 'POST':
        newItem = Expense(expensename=form.expensename.data,desc=form.description.data,amount=form.amount.data)
        db.session.add(newItem)
        try:
            db.session.commit()
            flash(f' {newItem.expensename} Successfully Added!', 'success')
            return redirect(url_for('dashboard'))
        except IntegrityError:
            db.session.rollback()
            flash(f'Try Again ','danger')
            return redirect(url_for('addexpense'))
    else:
        return render_template('expense.html',form = form)

@app.route('/Allexpenses/')
def allexpenses():
    page= request.args.get('page',1, type=int)
    expenses = Expense.query.paginate(page=page,per_page=5)
    return render_template('allexpenses.html', expenses = expenses)  
