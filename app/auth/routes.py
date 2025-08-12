from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import Users

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def auth():
    return render_template('auth/auth.html')

@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    user = Users.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        return redirect(url_for('main.index'))
    else:
        flash('E-mail e/ou senha inválidos.', 'danger')
        return redirect(url_for('auth.auth'))

@auth_bp.route('/cadastro', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    
    existing_user = Users.query.filter(
        (Users.username == username) | (Users.email == email)
    ).first()
    if existing_user:
        flash('Usuario e/ou e-mail já esta em uso.', 'danger')
        return redirect(url_for('auth.auth'))
    
    new_user = Users(username = username, email = email, password = generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()

    flash('Usuario cadastrado com sucesso!', 'success')
    return redirect(url_for('auth.auth'))