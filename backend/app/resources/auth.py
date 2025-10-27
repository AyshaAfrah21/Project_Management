from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import User, RoleEnum
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data.get('email') or not data.get('password') or not data.get('full_name'):
        return {'msg':'Missing fields'}, 400
    if User.query.filter_by(email=data['email']).first():
        return {'msg':'Email exists'}, 400
    user = User(
        full_name=data['full_name'],
        email=data['email'],
        password=generate_password_hash(data['password']),
        role=data.get('role')
    )
    db.session.add(user)
    db.session.commit()
    return {'msg':'created'}, 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    # --- DEBUG PRINTS START (Check these in your terminal) ---
    print(f"\nLogin Attempt - Email: {email}, Password: {password}")

    user = User.query.filter_by(email=email).first()
    
    # 1. Check if user exists (use the exact error message the frontend expects)
    if not user:
        print("Login Failure: User not found.")
        # Frontend likely expects a specific error message, ensure it matches what the frontend displays.
        return {'msg':'Invalid credentials'}, 401 
    
    # 2. Check password hash
    is_password_correct = check_password_hash(user.password, password)
    print(f"Password Check Result: {is_password_correct}")
    
    if not is_password_correct:
        print("Login Failure: Password mismatch.")
        # Ensure this message matches what the frontend is expecting (e.g., 'Invalid credentials')
        return {'msg':'Invalid credentials'}, 401 

    # --- SUCCESS ---
    token = create_access_token(identity={'id': user.id, 'role': user.role})
    print(f"Login Success for user: {user.email}")
    return {'access_token': token, 'user': {'id': user.id, 'full_name': user.full_name, 'role': user.role}}, 200