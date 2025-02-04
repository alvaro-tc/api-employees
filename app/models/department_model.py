from flask_sqlalchemy import SQLAlchemy
from database import db

class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    employees = db.relationship('Employee', back_populates='department')

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Department.query.all()

    @staticmethod
    def get_by_id(id):
        return Department.query.get(id)

    def update(self, name=None):
        if name is not None:
            self.name = name
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }