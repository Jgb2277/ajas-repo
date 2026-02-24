from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ---------------- USERS ----------------
class User(db.Model):
    __tablename__ = "users"

    email = db.Column(db.String(100), primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    password = db.Column(db.String(200), nullable=False)


# ---------------- SUBJECT ----------------
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)


# ---------------- MODULE ----------------
class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))


# ---------------- QUESTION ----------------
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text)
    option1 = db.Column(db.String(200))
    option2 = db.Column(db.String(200))
    option3 = db.Column(db.String(200))
    option4 = db.Column(db.String(200))
    correct_answer = db.Column(db.String(200))
    difficulty = db.Column(db.String(20))  # Easy / Intermediate / Advanced
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))


# ---------------- RESULT ----------------
class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(100), db.ForeignKey('users.email'))
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    score = db.Column(db.Integer)
    level = db.Column(db.String(20))
