from flask import Blueprint, request, jsonify, redirect, url_for, flash, render_template
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_login import login_user, logout_user, login_required, current_user
from .. import db
from ..models import User, Message
from werkzeug.security import generate_password_hash

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('auth/register.html')
    
    data = request.form if request.form else request.get_json()
    
    if User.query.filter_by(email=data['email']).first():
        flash('Email already registered', 'error')
        return redirect(url_for('auth.register'))
        
    if User.query.filter_by(username=data['username']).first():
        flash('Username already taken', 'error')
        return redirect(url_for('auth.register'))
    
    user = User(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        phone=data.get('phone')
    )
    
    db.session.add(user)
    db.session.commit()
    
    flash('Registration successful! Please login.', 'success')
    return redirect(url_for('auth.login'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
    
    data = request.form if request.form else request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and user.check_password(data['password']):
        login_user(user)
        access_token = create_access_token(identity=user.id)
        flash('Login successful!', 'success')
        return redirect(url_for('main.index'))
    
    flash('Invalid email or password', 'error')
    return redirect(url_for('auth.login'))

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@bp.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    unread_messages = 0
    received_messages = []
    
    if current_user.is_authenticated and current_user.id == user.id:
        unread_messages = Message.query.filter_by(recipient_id=user.id, is_read=False).count()
        received_messages = Message.query.filter_by(recipient_id=user.id).order_by(Message.created_at.desc()).all()
    
    return render_template('auth/profile.html', 
                         user=user, 
                         unread_messages=unread_messages,
                         received_messages=received_messages)

@bp.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    username = request.form.get('username')
    email = request.form.get('email')
    phone = request.form.get('phone')
    password = request.form.get('password')
    
    if not username or not email:
        flash('Username and email are required.', 'error')
        return redirect(url_for('auth.profile', username=current_user.username))
    
    # Check if username is taken by another user
    user = User.query.filter_by(username=username).first()
    if user and user.id != current_user.id:
        flash('Username is already taken.', 'error')
        return redirect(url_for('auth.profile', username=current_user.username))
    
    # Check if email is taken by another user
    user = User.query.filter_by(email=email).first()
    if user and user.id != current_user.id:
        flash('Email is already registered.', 'error')
        return redirect(url_for('auth.profile', username=current_user.username))
    
    current_user.username = username
    current_user.email = email
    current_user.phone = phone
    
    if password:
        current_user.password = generate_password_hash(password)
    
    db.session.commit()
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('auth.profile', username=current_user.username)) 