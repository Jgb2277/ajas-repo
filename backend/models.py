from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student') # student or admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    exam_date = db.Column(db.Date, nullable=True)
    modules = db.relationship('Module', backref='subject', lazy=True, cascade='all, delete-orphan')

class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    basic_yt = db.Column(db.String(255), nullable=True)
    basic_pdf = db.Column(db.Text, nullable=True)
    intermediate_yt = db.Column(db.String(255), nullable=True)
    intermediate_pdf = db.Column(db.Text, nullable=True)
    advanced_yt = db.Column(db.String(255), nullable=True)
    advanced_pdf = db.Column(db.Text, nullable=True)
    questions = db.relationship('Question', backref='module', lazy=True, cascade='all, delete-orphan')

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(20), nullable=False) # basic, intermediate, advanced
    options = db.Column(db.Text, nullable=False) # JSON encoded list of strings
    correct_option = db.Column(db.String(100), nullable=False)

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=True)
    score_basic = db.Column(db.Integer, default=0)
    score_intermediate = db.Column(db.Integer, default=0)
    score_advanced = db.Column(db.Integer, default=0)
    level_assigned = db.Column(db.String(20), nullable=False) # basic, intermediate, advanced
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    subject = db.relationship('Subject', backref=db.backref('assessments', lazy=True))
    module = db.relationship('Module', backref=db.backref('assessments', lazy=True))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('messages', lazy=True))
