from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SelectField,SubmitField,PasswordField,BooleanField
from wtforms.validators import DataRequired,NumberRange,InputRequired,Length


class addexpense(FlaskForm):
    expensename = StringField('Expense Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    amount= IntegerField('Amount', validators=[NumberRange(min=1, max=1000000),DataRequired()])
    expensubmit = SubmitField('Save Changes')
