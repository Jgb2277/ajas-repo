import json
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from models import db, Subject, Module, Question, Assessment

student_bp = Blueprint('student', __name__)

@student_bp.route('/subjects', methods=['GET'])
def get_subjects():
    subjects = Subject.query.all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'exam_date': s.exam_date.strftime('%Y-%m-%d') if s.exam_date else None
    } for s in subjects])

@student_bp.route('/subjects/<int:subject_id>/modules', methods=['GET'])
def get_modules(subject_id):
    modules = Module.query.filter_by(subject_id=subject_id).all()
    return jsonify([{
        'id': m.id,
        'name': m.name
    } for m in modules])

@student_bp.route('/modules/<int:module_id>/questions', methods=['GET'])
def get_questions(module_id):
    questions = Question.query.filter_by(module_id=module_id).all()
    # In a real app we'd randomize and limit these based on basic/intermediate/advanced distribution
    return jsonify([{
        'id': q.id,
        'text': q.text,
        'difficulty': q.difficulty,
        'options': json.loads(q.options),
        # Do not send correct_option to frontend to prevent cheating
    } for q in questions])

@student_bp.route('/assessments', methods=['POST'])
def submit_assessment():
    data = request.json
    user_id = data.get('user_id')
    subject_id = data.get('subject_id')
    answers = data.get('answers') # Expected: List of dicts [{'question_id': x, 'selected_option': y}]
    
    basic_score = 0
    inter_score = 0
    adv_score = 0
    
    if answers:
        for ans in answers:
            q = Question.query.get(ans['question_id'])
            if q and q.correct_option == ans['selected_option']:
                if q.difficulty == 'basic':
                    basic_score += 1
                elif q.difficulty == 'intermediate':
                    inter_score += 1
                elif q.difficulty == 'advanced':
                    adv_score += 1
                
    # Level assigning logic per user rules
    level = "Basic"
    if basic_score >= 4:
        if inter_score >= 5 and adv_score >= 4:
            level = "Advanced"
        elif inter_score >= 5 or adv_score >= 5:
            level = "Intermediate"
        elif inter_score < 5 and adv_score < 5:
            level = "Basic"
            
    assessment = Assessment(
        user_id=user_id,
        subject_id=subject_id,
        score_basic=basic_score,
        score_intermediate=inter_score,
        score_advanced=adv_score,
        level_assigned=level
    )
    db.session.add(assessment)
    db.session.commit()
    
    return jsonify({
        'message': 'Assessment submitted successfully',
        'level': level,
        'scores': {
            'basic': basic_score,
            'intermediate': inter_score,
            'advanced': adv_score
        }
    }), 201

@student_bp.route('/timetable/<int:user_id>', methods=['GET'])
def get_timetable(user_id):
    """
    Generate timetable entries for the user's subjects with 4+ days remaining.
    """
    assessments = Assessment.query.filter_by(user_id=user_id).order_by(Assessment.timestamp.desc()).all()
    
    # Get the latest assessment level for each subject
    latest_assessments = {}
    for a in assessments:
        if a.subject_id not in latest_assessments:
            latest_assessments[a.subject_id] = a
            
    timetable = []
    today = datetime.now().date()
    
    # Iterate through unique assessed subjects
    for subject_id, a in latest_assessments.items():
        subject = Subject.query.get(subject_id)
        if subject and subject.exam_date:
            days_until_exam = (subject.exam_date - today).days
            
            # Formulate schedule if min 4 days gap
            if days_until_exam >= 4:
                daily_hours = 0
                resources = []
                
                modules = Module.query.filter_by(subject_id=subject.id).all()
                for mod in modules:
                    if a.level_assigned == 'Basic' and (mod.basic_pdf or mod.basic_yt):
                        resources.append({"module": mod.name, "pdf": mod.basic_pdf, "yt": mod.basic_yt})
                    elif a.level_assigned == 'Intermediate' and (mod.intermediate_pdf or mod.intermediate_yt):
                        resources.append({"module": mod.name, "pdf": mod.intermediate_pdf, "yt": mod.intermediate_yt})
                    elif a.level_assigned == 'Advanced' and (mod.advanced_pdf or mod.advanced_yt):
                        resources.append({"module": mod.name, "pdf": mod.advanced_pdf, "yt": mod.advanced_yt})

                if a.level_assigned == 'Basic':
                    daily_hours = 3 
                elif a.level_assigned == 'Intermediate':
                    daily_hours = 2 
                elif a.level_assigned == 'Advanced':
                    daily_hours = 1 
                    
                timetable.append({
                    'subject': subject.name,
                    'exam_date': subject.exam_date.strftime('%Y-%m-%d'),
                    'days_remaining': days_until_exam,
                    'level': a.level_assigned,
                    'daily_study_hours': daily_hours,
                    'resources': resources,
                    'id': str(subject.id)
                })
                
    return jsonify(timetable)

@student_bp.route('/history/<int:user_id>', methods=['GET'])
def get_history(user_id):
    assessments = Assessment.query.filter_by(user_id=user_id).order_by(Assessment.timestamp.desc()).limit(10).all()
    return jsonify([{
        'id': a.id,
        'subject': a.subject.name,
        'level': a.level_assigned,
        'date': a.timestamp.strftime('%Y-%m-%d')
    } for a in assessments])
    
