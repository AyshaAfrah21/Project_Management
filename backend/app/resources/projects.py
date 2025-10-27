from flask import Blueprint, request
from ..extensions import db
from ..models import Project, User
from ..schemas import ProjectSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Task 


projects_bp = Blueprint('projects', __name__)
project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)

@projects_bp.route('/', methods=['POST'])
@jwt_required()
def create_project():
    data = request.get_json()
    p = Project(title=data['title'], description=data.get('description'))
    # add members if provided
    member_ids = data.get('member_ids', [])
    for uid in member_ids:
        u = User.query.get(uid)
        if u:
            p.members.append(u)
    db.session.add(p)
    db.session.commit()
    return project_schema.dump(p), 201

@projects_bp.route('/', methods=['GET'])
@jwt_required()
def list_projects():
    projects = Project.query.all()
    return projects_schema.dump(projects), 200

@projects_bp.route('/<int:project_id>', methods=['GET','PUT','DELETE'])
@jwt_required()
def project_detail(project_id):
    p = Project.query.get_or_404(project_id)
    if request.method == 'GET':
        return project_schema.dump(p)
    if request.method == 'PUT':
        data = request.get_json()
        p.title = data.get('title', p.title)
        p.description = data.get('description', p.description)
        db.session.commit()
        return project_schema.dump(p)
    if request.method == 'DELETE':
        db.session.delete(p)
        db.session.commit()
        return {}, 204
    
@projects_bp.route('/metrics', methods=['GET'])
@jwt_required()
def metrics():
    from datetime import date
    total_tasks = Task.query.count()
    overdue = Task.query.filter(Task.deadline < date.today(), Task.status != 'Done').count()
    by_status = {s: Task.query.filter_by(status=s).count() for s in ['To Do','In Progress','Done']}
    return {'total_tasks':total_tasks, 'overdue':overdue, 'by_status':by_status}
