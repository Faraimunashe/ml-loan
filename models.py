from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import datetime

db = SQLAlchemy()

#from .models import User
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    role = db.Column(db.Integer)

    def __init__(self, email, password, name, role):
        self.email=email
        self.password=password
        self.name=name
        self.role=role

class LoanApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    income = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    credit_history = db.Column(db.Integer, nullable=False)
    employment_status = db.Column(db.String(20), nullable=False)
    debt_to_income_ratio = db.Column(db.Integer, nullable=False)
    credit_score = db.Column(db.Integer, nullable=False)
    loan_amount = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    level_of_education = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now())

    def __init__(self, user_id, income, credit_history, employment_status, debt_to_income_ratio, credit_score, loan_amount, status, level_of_education, created_at):
        self.user_id = user_id
        self.income = income
        self.credit_history = credit_history
        self.employment_status = employment_status
        self.debt_to_income_ratio = debt_to_income_ratio
        self.credit_score = credit_score
        self.loan_amount = loan_amount
        self.level_of_education = level_of_education
        self.status = status
        self.created_at = created_at
