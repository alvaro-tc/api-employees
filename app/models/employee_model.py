from database import db
from models.department_model import Department

class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    ci = db.Column(db.Integer, nullable=False)
    
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    department = db.relationship('Department', back_populates='employees')

    def __init__(self, name, lastname, ci, department_id):
        self.name = name
        self.lastname = lastname
        self.ci = ci
        department = Department.get_by_id(department_id)
        if not department:
            raise ValueError("Departamento no encontrado")
        self.department_id = department_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Employee.query.all()

    @staticmethod
    def get_by_id(id):
        return Employee.query.get(id)

    def update(self, name=None, lastname=None, ci=None, department_id=None):
        if name is not None:
            self.name = name
        if lastname is not None:
            self.lastname = lastname
        if ci is not None:
            self.ci = ci
        if department_id is not None:
            department = Department.get_by_id(department_id)
            if not department:
                raise ValueError("Departamento no encontrado")
            self.department_id = department_id
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            "ci": self.ci,
            "department_id": self.department_id
        }