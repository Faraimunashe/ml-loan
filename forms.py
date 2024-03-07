from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Login')
    

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    
class LoanForm(FlaskForm):
    edu_choices = [('Not Educated', 'Not Educated'),
               ('O Level', 'O Level'),
               ('A Level', 'A Level'),
               ('Bachelor', 'Bachelor'),
               ('Masters', 'Masters'),
               ('PHD', 'PHD')]
    emp_choices = [('Employed', 'Employed'),
               ('Unemployed', 'Unemployed')]
    income = DecimalField('Income', validators=[DataRequired(), NumberRange(min=0.01)])
    credit_history = IntegerField('Credit History', validators=[DataRequired(), NumberRange(min=0, max=1)])
    employment_status = SelectField('Employment Status', choices=emp_choices)
    debt_to_income_ratio = IntegerField('Debt To Income Ratio', validators=[DataRequired(), NumberRange(min=1, max=100)])
    credit_score = IntegerField('Credit Score', validators=[DataRequired(), NumberRange(min=200, max=800)])
    loan_amount = DecimalField('Loan Amount', validators=[DataRequired(), NumberRange(min=0.01)])
    level_of_education = SelectField('Level Of Education', choices=edu_choices)
    submit = SubmitField('Apply Loan')