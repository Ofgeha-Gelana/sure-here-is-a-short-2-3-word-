```python
# src/api.py

"""
File purpose: Application endpoints
Requirements: Production-ready quality, proper documentation, follow best practices
"""

from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import os

# Initialize Flask and SQLAlchemy objects
app = Flask(__name__)
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"Student('{self.name}', '{self.email}', '{self.age}')"

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    student = db.relationship('Student', backref=db.backref('courses', lazy=True))

    def __repr__(self):
        return f"Course('{self.name}')"

# API endpoints
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    result = []
    for student in students:
        student_dict = {}
        student_dict['id'] = student.id
        student_dict['name'] = student.name
        student_dict['email'] = student.email
        student_dict['age'] = student.age
        student_dict['registered_on'] = student.registered_on
        result.append(student_dict)
    return jsonify(result)

@app.route('/students/<int:id>', methods=['GET'])
def get_student_by_id(id):
    student = Student.query.get(id)
    if student is None:
        return jsonify({'message': 'Student not found'}), 404
    student_dict = {}
    student_dict['id'] = student.id
    student_dict['name'] = student.name
    student_dict['email'] = student.email
    student_dict['age'] = student.age
    student_dict['registered_on'] = student.registered_on
    return jsonify(student_dict)

@app.route('/students', methods=['POST'])
def create_student():
    name = request.json['name']
    email = request.json['email']
    age = request.json['age']
    registered_on = date.today()
    student = Student(name=name, email=email, age=age, registered_on=registered_on)
    db.session.add(student)
    db.session.commit()
    return jsonify({'message': 'Student created successfully'}), 201

@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get(id)
    if student is None:
        return jsonify({'message': 'Student not found'}), 404
    name = request.json['name']
    email = request.json['email']
    age = request.json['age']
    registered_on = date.today()
    student.name = name
    student.email = email
    student.age = age
    student.registered_on = registered_on
    db.session.commit()
    return jsonify({'message': 'Student updated successfully'}), 201

@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)
    if student is None:
        return jsonify({'message': 'Student not found'}), 404
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student deleted successfully'}), 201

@app.route('/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    result = []
    for course in courses:
        course_dict = {}
        course_dict['id'] = course.id
        course_dict['name'] = course.name
        course_dict['student_id'] = course.student_id
        result.append(course_dict)
    return jsonify(result)

@app.route('/courses/<int:id>', methods=['GET'])
def get_course_by_id(id):
    course = Course.query.get(id)
    if course is None:
        return jsonify({'message': 'Course not found'}), 404
    course_dict = {}
    course_dict['id'] = course.id
    course_dict['name'] = course.name
    course_dict['student_id'] = course.student_id
    return jsonify(course_dict)

@app.route('/courses', methods=['POST'])
def create_course():
    name = request.json['name']
    student_id = request.json['student_id']
    course = Course(name=name, student_id=student_id)
    db.session.add(course)
    db.session.commit()
    return jsonify({'message': 'Course created successfully'}), 201

@app.route('/courses/<int:id>', methods=['PUT'])
def update_course(id):
    course = Course.query.get(id)
    if course is None:
        return jsonify({'message': 'Course not found'}), 404
    name = request.json['name']
    student_id = request.json['student_id']
    course.name = name
    course.student_id = student_id
    db.session.commit()
    return jsonify({'message': 'Course updated successfully'}), 201

@app.route('/courses/<int:id>', methods=['DELETE'])
def delete_course(id):
    course = Course.query.get(id)
    if course is None:
        return jsonify({'message': 'Course not found'}), 404
    db.session.delete(course)
    db.session.commit()
    return jsonify({'message': 'Course deleted successfully'}), 201
```