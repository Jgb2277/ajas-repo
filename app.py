from flask import Flask, render_template, request, redirect, session, url_for
from models import db, User, Subject, Module, Question, Assessment,Result,ChatMessage
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_socketio import SocketIO, emit

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///EduPath.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)

socketio = SocketIO(app, cors_allowed_origins="*")

db.init_app(app)

with app.app_context():
    db.create_all()

def classify_module(easy_correct, intermediate_correct, advanced_correct):

    # ADVANCED
    if easy_correct >= 3 and intermediate_correct >= 4 and advanced_correct >= 3:
        return "Advanced"

    # INTERMEDIATE
    if easy_correct >= 3:
        return "Intermediate"

    # BASIC
    return "Basic"


@socketio.on('chat_message')
def handle_message(data):
    username = data['username']
    message = data['message']


    chat = ChatMessage(username=username, message=message)
    db.session.add(chat)
    db.session.commit()

    emit('message', {
        'username': username,
        'message': message
    }, broadcast=True)



@app.route('/profile')
def profile():
    return "<h2>Profile Page</h2>"


@app.route('/timetable')
def timetable():
    return "<h2>Time Table Page</h2>"


@app.route('/assessment')
def assessment_page():
    return "<h2>Assessment Page</h2>"


@app.route('/chat')
def chat():
    if 'user_name' not in session:
        return redirect('/')

    # Get previous messages (old → new)
    messages = ChatMessage.query.order_by(ChatMessage.timestamp.asc()).all()

    return render_template('chat.html', messages=messages)



# ---------------- LOGIN PAGE ----------------
@app.route('/')
def login():
    return render_template('login1.html')


# ---------------- SIGNUP PAGE ----------------
@app.route('/signup')
def signup():
    return render_template('signup1.html')


# ---------------- ADD USER ----------------
@app.route('/add_user', methods=['POST'])
def add_user():

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    password = request.form.get('password')

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return render_template('signup1.html', error="Email already registered!")

    full_name = fname + " " + lname

    new_user = User(
        name=full_name,
        email=email,
        password_hash=generate_password_hash(password)   # temporarily plain text
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect('/')


# ---------------- LOGIN VALIDATION ----------------
@app.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        session['user_email'] = user.email
        session['user_name'] = user.name
        return redirect('/home')
    else:
        return redirect('/')

# ---------------- HOME ----------------
@app.route('/home')
def home():
    if 'user_email' not in session:
        return redirect('/')

    return render_template(
        'home.html',
        fname=session['user_name'],
        email=session['user_email']
    )


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# ---------------- SHOW MODULES ----------------
@app.route('/subject/<int:subject_id>')
def show_modules(subject_id):
    modules = Module.query.filter_by(subject_id=subject_id).all()
    
    user = User.query.filter_by(email=session['user_email']).first()
    
    # Get list of module IDs already attempted by this user
    completed = Result.query.filter_by(user_id=user.id).all()
    completed_module_ids = [r.module_id for r in completed]
    
    return render_template('modules.html', 
                           modules=modules,
                           completed_module_ids=completed_module_ids)


# ---------------- START QUIZ ----------------
@app.route('/quiz/<int:module_id>')
def start_quiz(module_id):

    easy = Question.query.filter_by(
        module_id=module_id,
        difficulty="Easy"
    ).all()

    intermediate = Question.query.filter_by(
        module_id=module_id,
        difficulty="Intermediate"
    ).all()

    advanced = Question.query.filter_by(
        module_id=module_id,
        difficulty="Advanced"
    ).all()

    questions = easy + intermediate + advanced

    return render_template("quiz.html",
                           questions=questions,
                           module_id=module_id)


# ---------------- SUBMIT QUIZ ----------------
@app.route('/submit_quiz/<int:module_id>', methods=['POST'])
def submit_quiz(module_id):

    if 'user_email' not in session:
        return redirect('/')

    user = User.query.filter_by(email=session['user_email']).first()

    questions = Question.query.filter_by(module_id=module_id).all()

    easy_correct = 0
    intermediate_correct = 0
    advanced_correct = 0
    score = 0
    attempted = 0

    for question in questions:
        selected = request.form.get(str(question.id))

        if not selected:
            continue

        attempted += 1

        if selected == question.correct_answer:
            score += 1

            if question.difficulty == "Easy":
                easy_correct += 1
            elif question.difficulty == "Intermediate":
                intermediate_correct += 1
            elif question.difficulty == "Advanced":
                advanced_correct += 1

    # 🧠 Module Classification
    level = classify_module(easy_correct, intermediate_correct, advanced_correct)

    # Save result in DB
    result = Result(
        user_id=user.id,
        module_id=module_id,
        score=score,
        level=level
    )

    db.session.add(result)
    db.session.commit()

    return redirect(url_for('show_notes',
                            module_id=module_id,
                            level=level,
                            score=score,
                            attempted=attempted))

# ---------------- NOTES ----------------
@app.route('/notes/<int:module_id>/<level>')
def show_notes(module_id, level):
    score     = request.args.get("score", 0)
    attempted = request.args.get("attempted", 0)
    return render_template('notes.html',
                           level=level,
                           score=score,
                           attempted=attempted)


if __name__ == '__main__':
    socketio.run(app,debug=True)
