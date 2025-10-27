# backend/app/resources/users.py
from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import User, RoleEnum
from ..schemas import UserSchema
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity

users_bp = Blueprint('users', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

def is_admin(identity):
    return identity and identity.get('role') == RoleEnum.ADMIN.value

def is_manager(identity):
    return identity and identity.get('role') == RoleEnum.MANAGER.value

@users_bp.route('/', methods=['GET'])
@jwt_required()
def list_users():
    """
    List all users.
    Admins and Managers can list all users.
    Developers can only see their own user (use /me).
    """
    identity = get_jwt_identity()
    if is_admin(identity) or is_manager(identity):
        users = User.query.all()
        return users_schema.dump(users), 200
    # if developer, return only their user
    user = User.query.get(identity.get('id'))
    if not user:
        return {'msg': 'User not found'}, 404
    return user_schema.dump(user), 200

@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """
    Get a single user by id.
    Admins and Managers can fetch any user.
    Developers can fetch only their own profile.
    """
    identity = get_jwt_identity()
    if not (is_admin(identity) or is_manager(identity)):
        # developer: allow only if same id
        if identity.get('id') != user_id:
            return {'msg': 'Forbidden'}, 403

    u = User.query.get_or_404(user_id)
    return user_schema.dump(u), 200

@users_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    """Return current authenticated user's profile"""
    identity = get_jwt_identity()
    u = User.query.get_or_404(identity.get('id'))
    return user_schema.dump(u), 200

@users_bp.route('/', methods=['POST'])
@jwt_required()
def create_user():
    """
    Create a user (Admin only).
    Payload: { full_name, email, password, role }
    """
    identity = get_jwt_identity()
    if not is_admin(identity):
        return {'msg': 'Only admins can create users'}, 403

    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')
    role = data.get('role', RoleEnum.DEVELOPER.value)

    if not email or not password or not full_name:
        return {'msg': 'Missing fields (full_name, email, password required)'}, 400

    if User.query.filter_by(email=email).first():
        return {'msg': 'Email already exists'}, 400

    user = User(
        full_name=full_name,
        email=email,
        password=generate_password_hash(password),
        role=role
    )
    db.session.add(user)
    db.session.commit()
    return user_schema.dump(user), 201

@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """
    Update user fields.
    Admins can update any user.
    Users can update their own profile (but not role).
    Payload allowed: full_name, password, role (admin only)
    """
    identity = get_jwt_identity()
    u = User.query.get_or_404(user_id)

    data = request.get_json() or {}

    # If not admin, only allow updating own profile and disallow role changes
    if not is_admin(identity):
        if identity.get('id') != user_id:
            return {'msg': 'Forbidden'}, 403
        # remove role if present to prevent privilege escalation
        data.pop('role', None)

    # Apply updates
    if 'full_name' in data:
        u.full_name = data.get('full_name') or u.full_name
    if 'password' in data and data.get('password'):
        u.password = generate_password_hash(data.get('password'))
    if 'role' in data and is_admin(identity):
        # Only admin can set role; validate
        requested_role = data.get('role')
        if requested_role not in (r.value for r in RoleEnum):
            return {'msg': 'Invalid role'}, 400
        u.role = requested_role

    db.session.commit()
    return user_schema.dump(u), 200

@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """
    Delete a user. Admin only.
    """
    identity = get_jwt_identity()
    if not is_admin(identity):
        return {'msg': 'Only admins can delete users'}, 403

    u = User.query.get_or_404(user_id)
    db.session.delete(u)
    db.session.commit()
    return {}, 204
