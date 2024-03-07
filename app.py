from flask import Flask, jsonify, request, redirect, render_template, url_for, flash, session,wrappers
from flask_session import Session
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import os
from models import *
from functools import wraps
from forms import LoginForm, RegistrationForm, LoanForm
from passlib.hash import sha256_crypt



app = Flask(__name__)
app.config['SECRET_KEY'] = 'ProfessorSecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/loan_db'

db.init_app(app)


login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

def admin_role(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        user = User.query.filter_by(id=session['userid']).first()
        if user.role == 1:
            return f(*args, **kwargs)
        else:
            return redirect("/")
    return decorated_func

@app.route('/', methods=['GET', 'POST'])
def index():
    
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash('Invalid login details.')
            return redirect(url_for('login'))
        if sha256_crypt.verify(password, user.password):
            login_user(user)
            session['userid'] = user.id
            return redirect(url_for('dashboard'))

        flash('Invalid login details.')
        return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        passwordata = sha256_crypt.encrypt(password)

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Error email already exists!')
            return redirect(url_for('register'))
        new_user = User(email=email, password=passwordata, name=name, role=2)
        db.session.add(new_user)
        db.session.commit()

        flash('Successfully registered new user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():

    return render_template('dashboard.html')


@app.route('/apply-loan', methods=['GET', 'POST'])
@login_required
def apply_loan():
    form = LoanForm()
    print("Here now")
    if form.validate_on_submit():
        income = form.income.data
        credit_history = form.credit_history.data
        employment_status = form.employment_status.data
        debt_to_income_ratio = form.debt_to_income_ratio.data
        credit_score = form.credit_score.data
        loan_amount = form.loan_amount.data
        level_of_education = form.level_of_education.data
        
        
        new_application = LoanApplication(
            user_id=session['userid'],
            income=income,
            credit_history=credit_history,
            employment_status=employment_status,
            debt_to_income_ratio=debt_to_income_ratio,
            credit_score=credit_score,
            loan_amount=loan_amount,
            level_of_education=level_of_education,
            status='pending',
            created_at=datetime.datetime.now()
        )
        db.session.add(new_application)
        db.session.commit()
        
        flash('Successfully applied for loan!')
        return redirect(url_for('apply_loan'))

    return render_template('apply_loan.html', form=form)


@app.route('/loan-history', methods=['GET'])
@login_required
def loan_history():
    loan_applications = LoanApplication.query.filter_by(user_id=session['userid']).all()
    return render_template('loan_history.html', loan_applications=loan_applications)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    g=None
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
