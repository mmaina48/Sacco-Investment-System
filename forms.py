from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SelectField,SubmitField,PasswordField,BooleanField
from wtforms.validators import DataRequired,NumberRange,InputRequired,Length



class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=80)])
    remember = BooleanField('remember me')


allroles=[('1','Member'),('2','Leader'),('3','Admin')]
class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=80)])
    memberrole = SelectField('Select Role',choices=allroles)
    submit = SubmitField('Save Changes')

class addexpense(FlaskForm):
    expensename = StringField('Expense Name', validators=[DataRequired()])
    amount= IntegerField('Amount', validators=[NumberRange(min=1, max=1000000),DataRequired()])
    expensubmit = SubmitField('Save Changes')

class editexpense(FlaskForm):
    editexpensename = StringField('Expense Name', validators=[DataRequired()])
    editamount = IntegerField('Amount', validators=[NumberRange(min=0, max=1000000)])
    editsubmit = SubmitField('Save Changes')

class addcontribution(FlaskForm):
    membername = StringField('Member Name', validators=[DataRequired()])
    amount= IntegerField('Amount', validators=[NumberRange(min=1, max=1000000),DataRequired()])
    addcontrib= SubmitField('Save Changes')

class editcontribution(FlaskForm):
    editmembername = StringField('Member Name', validators=[DataRequired()])
    editamount = IntegerField('Amount', validators=[NumberRange(min=1, max=1000000),DataRequired()])
    editsubmit = SubmitField('Save Changes')
    cancel = SubmitField('Cancel')

class addmember(FlaskForm):
    membername = StringField('Member Name', validators=[DataRequired()])
    memberphone = StringField('Phone Number', validators=[DataRequired()])
    amount = IntegerField('Amount', validators=[NumberRange(min=0, max=1000000)])
    membersubmit = SubmitField('Save Changes')

class editmember(FlaskForm):
    editmembername = StringField('Member Name', validators=[DataRequired()])
    editphone = StringField('Phone Number', validators=[DataRequired()])
    editamount = IntegerField('Amount', validators=[NumberRange(min=0, max=1000000)])
    editsubmit = SubmitField('Save Changes')

class searchmember(FlaskForm):
    membername = StringField('Member Name', validators=[DataRequired()])
    searchprod= SubmitField('Search')