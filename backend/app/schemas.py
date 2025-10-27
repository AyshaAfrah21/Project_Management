from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .models import User, Project, Task
from .extensions import db

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_relationships = True
        sqla_session = db.session
        exclude = ("password",)

class ProjectSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Project
        load_instance = True
        include_fk = True
        sqla_session = db.session

class TaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        load_instance = True
        include_fk = True
        sqla_session = db.session
