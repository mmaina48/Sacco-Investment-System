from flask import Flask, render_template,session,g
from flask import  render_template,url_for,redirect,flash,request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from main import app,db
from forms import addexpense,addcontribution,addmember,editcontribution,editmember,LoginForm,RegisterForm,allroles,editexpense
from models import Expense,Member,Contribution,User
import time,datetime
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps


login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_request
def before_request():
    g.user = current_user

# functions to DEFINE PERMISSIONS
def required_roles(*roles):
   def wrapper(f):
      @wraps(f)
      def wrapped(*args, **kwargs):
         if get_current_user_role() not in roles:
            flash(f'Please ,You Dont Have previlege to that page','danger')
            return redirect(url_for('dashboard'))
         return f(*args, **kwargs)
      return wrapped
   return wrapper
 
def get_current_user_role():
    return g.user.role

   

@app.route('/')
@app.route('/login/', methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=True)
                return redirect(url_for('dashboard'))
            else:
                flash(f'Incorrect Username or password','danger')
        return redirect(url_for('login'))
    return render_template('login.html',form=form)  

@app.route('/signup/',methods=['GET','POST'])
@login_required
@required_roles('Admin')
def signup():
    form=RegisterForm()
    if form.validate_on_submit():
        hashed_password= generate_password_hash(form.password.data, method='sha256')
        newuser = User(username=form.username.data,role=dict(allroles).get(form.memberrole.data), password=hashed_password )
        db.session.add(newuser)
        try:
            db.session.commit()
            flash(f' {newuser.username} Successfully Added!', 'success')
            return redirect(url_for('dashboard'))
        except IntegrityError:
            db.session.rollback()
            flash(f'This User already exists','danger')
            return redirect(url_for('signup'))
    return render_template('AddUser.html', form=form)


@app.route('/members/')
@login_required
def dashboard():
    page= request.args.get('page',1, type=int)
    exp = Expense.query.all()
    members=Member.query.paginate(page=page,per_page=5)
    explist=[]
    member=[]
    savings=[]
    for e in exp:
        explist.append(e.amount)
    totalexp=sum(explist)
    for m in members.items:
        member.append(m.membername)
        savings.append(m.amount)

    totalmembers=len(member)
    totalcontri=sum(savings)
    totalsave=totalcontri-totalexp
    return render_template('dashboard.html', members=members , totalexp=totalexp,totalmembers=totalmembers,totalcontri=totalcontri,totalsave=totalsave)

#Create a new member
@app.route('/new/member/', methods=['GET','POST'])
@login_required
@required_roles('Leader','Admin')
def newMembers():
    form = addmember()
    if form.validate_on_submit() and request.method == 'POST':
        newmeb = Member(membername=form.membername.data,memberphone=form.memberphone.data,amount=form.amount.data)
        db.session.add(newmeb)
        try:
            db.session.commit()
            flash(f' {newmeb.membername} Successfully Added!', 'success')
            return redirect(url_for('dashboard'))
        except IntegrityError:
            db.session.rollback()
            flash(f'This Member already exists','danger')
            return redirect(url_for('newMembers'))
    else:
        return render_template('AddMember.html',form = form)

@app.route('/new/member/<int:member_id>/edit/', methods = ['GET', 'POST'])
@login_required
@required_roles('Leader','Admin')
def editmemb(member_id):
    form = editmember()
    editedItem = Member.query.filter_by(id =member_id).one()
    if request.method == 'POST':
        if form.editmembername.data:
          editedItem.membername = form.editmembername.data
        if form.editamount.data:
          editedItem.amount = form.editamount.data
        db.session.add(editedItem)
        db.session.commit() 
        flash(f'{form.editmembername.data}  has been updated!', 'success')
        return redirect(url_for('dashboard'))
    else:
        return render_template('editmember.html',member_id=member_id,d = editedItem,form=form)

@app.route('/members/<int:member_id>/delete/', methods=['GET', 'POST'])
@login_required
@required_roles('Admin')
def deleteMember(member_id):
    Membertodelete = Member.query.filter_by(id=member_id).one()
    if request.method == 'POST':
        db.session.delete(Membertodelete)
        db.session.commit()
        flash(f'{Membertodelete.membername}  has been deleted!', 'warning')
        return redirect(url_for('dashboard'))
    else:
        return render_template('deleteMember.html', member=Membertodelete)
# All Contribution 
@app.route('/members/<int:member_id>/')
@app.route('/members/<int:member_id>/contributions/')
@login_required
def showContributions(member_id):
    member=Member.query.filter_by(id=member_id).one()
    contributions=Contribution.query.filter_by(member_id=member_id).all()
    exists= bool(Contribution.query.filter_by(member_id=member_id).all())
    if exists == False:
        flash(f'No Contribution made for {member.membername}!','success')
    return render_template('AllContributions.html',member=member,contributions=contributions,member_id=member_id)

#Add Contribution
@app.route('/members/<int:member_id>/contributions/new/', methods=['GET', 'POST'])
@login_required
@required_roles('Leader','Admin')
def newMemberContribution(member_id):
    form=addcontribution()
    memberToAddcontrib = Member.query.filter_by(id=member_id).one()
    if request.method == 'POST':
        memberToAddcontrib.amount = memberToAddcontrib.amount + int(form.amount.data)    
        newItem = Contribution(membername=form.membername.data,amount=form.amount.data,member_id=member_id)
        db.session.add(memberToAddcontrib)
        db.session.add(newItem)
        try:
            db.session.commit()
            db.session.commit()
            flash(f' {newItem.membername} Contribution Successfully Added!', 'success')
            return redirect(url_for('showContributions',member_id=member_id))
        except IntegrityError:
            db.session.rollback()
            flash(f'Try Again ','danger')
            return redirect(url_for('newMemberContribution'))
    else:
        return render_template('AddContribution.html', member_id=member_id,memberToAddcontrib=memberToAddcontrib,form=form)

# Edit Contribution
@app.route('/members/<int:member_id>/contributions/<int:contributions_id>/edit',methods=['GET', 'POST'])
@login_required
@required_roles('Leader','Admin')
def editMemberContribution(member_id,contributions_id):
    form = editcontribution()
    editedItem = Contribution.query.filter_by(id =contributions_id).one()
    if request.method == 'POST':
        if form.editmembername.data:
          editedItem.membername = form.editmembername.data
        if form.editamount.data:
          editedItem.amount = form.editamount.data
        db.session.add(editedItem)
        db.session.commit() 
        flash(f'{form.editmembername.data}  has been updated!', 'success')
        return redirect(url_for('showContributions'))
    else:
        return render_template('editcontribution.html',d = editedItem,form=form)

@app.route('/members/<int:member_id>/contributions/<int:contributions_id>/delete',methods=['GET', 'POST'])
@login_required
@required_roles('Admin')
def deleteMemberContribution(member_id, contributions_id):
    MemberContributionToDelete = Contribution.query.filter_by(id=contributions_id).one()
    memberAmounttodelete = Member.query.filter_by(id=member_id).one()
    if request.method == 'POST':
        memberAmounttodelete.amount=memberAmounttodelete.amount - MemberContributionToDelete.amount
        db.session.add(memberAmounttodelete)
        db.session.delete(MemberContributionToDelete)
        db.session.commit()
        db.session.commit()
        return redirect(url_for('showContributions',member_id=member_id))
    else:
        return render_template('deleteMemberContribution.html', contrib=MemberContributionToDelete)

# Expenses

@app.route('/Allexpenses/')
@login_required
def allexpenses():
    page= request.args.get('page',1, type=int)
    expenses = Expense.query.paginate(page=page,per_page=5)
    return render_template('allexpenses.html', expenses = expenses)  


#Create an expense
@app.route('/expense/', methods=['GET','POST'])
@login_required
@required_roles('Leader','Admin')
def addExpense():
    form = addexpense()
    if form.validate_on_submit() and request.method == 'POST':
        newItem = Expense(expensename=form.expensename.data,amount=form.amount.data)
        db.session.add(newItem)
        try:
            db.session.commit()
            flash(f' {newItem.expensename} Successfully Added!', 'success')
            return redirect(url_for('allexpenses'))
        except IntegrityError:
            db.session.rollback()
            flash(f'Try Again ','danger')
            return redirect(url_for('addexpense'))
    else:
        return render_template('expense.html',form = form)


@app.route('/expense/<int:expense_id>/edit/', methods = ['GET', 'POST'])
@login_required
@required_roles('Leader','Admin')
def editexpe(expense_id):
    form = editexpense()
    editedItem = Expense.query.filter_by(id =expense_id).one()
    if request.method == 'POST':
        if form.editexpensename.data:
          editedItem.expensename = form.editexpensename.data
        if form.editamount.data:
          editedItem.amount = form.editamount.data
        db.session.add(editedItem)
        db.session.commit() 
        flash(f'{form.editexpensename.data}  has been updated!', 'success')
        return redirect(url_for('allexpenses'))
    else:
        return render_template('editexpense.html',d = editedItem,form=form)

@app.route('/new/expense/<int:expense_id>/delete/', methods=['GET', 'POST'])
@login_required
@required_roles('Admin')
def deleteExpense(expense_id):
    expensetodelete = Expense.query.filter_by(id=expense_id).one()
    if request.method == 'POST':
        db.session.delete(expensetodelete)
        db.session.commit()
        flash(f'Expense  deleted','danger')
        return redirect(url_for('dashboard'))
    else:
        return render_template('deleteexpense.html', expense=expensetodelete)

@app.route('/finacialstatement')
@login_required
def finacialState():
    exp = Expense.query.all()
    members=Member.query.all()
    explist=[]
    member=[]
    savings=[]
    for e in exp:
        explist.append(e.amount)
    totalexp=sum(explist)
    for m in members:
        member.append(m.membername)
        savings.append(m.amount)

    totalmembers=len(member)
    totalcontri=sum(savings)
    totalsave=totalcontri-totalexp
    return render_template('FinacialStatement.html', members=members , totalexp=totalexp,totalmembers=totalmembers,totalcontri=totalcontri,totalsave=totalsave)

@app.route('/logout')
@required_roles('Leader','Member','Admin')
def logout():
    logout_user()
    return redirect(url_for('login'))
