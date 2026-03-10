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
    module_id = data.get('module_id')   # NEW – per-module submission
    answers = data.get('answers')       # List of dicts [{'question_id': x, 'selected_option': y}]

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

    # Level assigning logic
    level = "Basic"
    if basic_score >= 4:
        if inter_score >= 5 and adv_score >= 4:
            level = "Advanced"
        elif inter_score >= 5 or adv_score >= 5:
            level = "Intermediate"
        elif inter_score < 5 and adv_score < 5:
            level = "Basic"

    # If a previous assessment exists for this user+subject+module, update it.
    # Otherwise insert a new record.
    existing = None
    if module_id:
        existing = Assessment.query.filter_by(
            user_id=user_id, subject_id=subject_id, module_id=module_id
        ).first()

    if existing:
        existing.score_basic = basic_score
        existing.score_intermediate = inter_score
        existing.score_advanced = adv_score
        existing.level_assigned = level
        existing.timestamp = datetime.utcnow()
        assessment = existing
    else:
        assessment = Assessment(
            user_id=user_id,
            subject_id=subject_id,
            module_id=module_id,
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
    Build one timetable entry per subject.
    - For each subject, take the LATEST assessment per module.
    - Determine the overall subject level from those latest module assessments
      (mode/aggregate: if any module is Advanced, subject is Advanced; else Intermediate if any; else Basic).
    - Collect per-module resources matching that module's own level.
    - If the same subject was reassessed, only the latest data per module is used
      (old module results are overwritten in submit_assessment, so this is automatic).
    - All subjects the student has ever assessed are shown (no disabling).
    """
    today = datetime.now().date()

    # All assessments for this user
    all_assessments = Assessment.query.filter_by(user_id=user_id).order_by(Assessment.timestamp.desc()).all()

    # Group by subject_id → module_id → latest assessment
    # Structure: { subject_id: { module_id: assessment } }
    per_subject_modules = {}
    for a in all_assessments:
        sid = a.subject_id
        mid = a.module_id  # may be None for old records
        if sid not in per_subject_modules:
            per_subject_modules[sid] = {}
        key = mid if mid is not None else 'legacy'
        if key not in per_subject_modules[sid]:
            per_subject_modules[sid][key] = a   # ordered desc so first is latest

    timetable = []
    for subject_id, module_map in per_subject_modules.items():
        subject = Subject.query.get(subject_id)
        if not subject or not subject.exam_date:
            continue

        days_until_exam = (subject.exam_date - today).days
        if days_until_exam < 4:
            continue

        # Determine overall subject level: use "worst" level so study plan is safe.
        # Priority: Basic > Intermediate > Advanced (Basic means most study needed)
        level_order = {'Basic': 0, 'Intermediate': 1, 'Advanced': 2}
        levels = [a.level_assigned for a in module_map.values()]
        overall_level = min(levels, key=lambda l: level_order.get(l, 0))

        # Daily hours based on overall level
        if overall_level == 'Basic':
            daily_hours = 3
        elif overall_level == 'Intermediate':
            daily_hours = 2
        else:
            daily_hours = 1

        # Build per-module resources using each module's own assessed level
        resources = []
        all_modules = Module.query.filter_by(subject_id=subject_id).all()
        for mod in all_modules:
            # Find the assessment for this module
            mod_assessment = module_map.get(mod.id) or module_map.get('legacy')
            if mod_assessment is None:
                continue
            lvl = mod_assessment.level_assigned
            pdf = None
            yt = None
            if lvl == 'Basic':
                pdf = mod.basic_pdf
                yt = mod.basic_yt
            elif lvl == 'Intermediate':
                pdf = mod.intermediate_pdf
                yt = mod.intermediate_yt
            elif lvl == 'Advanced':
                pdf = mod.advanced_pdf
                yt = mod.advanced_yt

            if pdf or yt:
                resources.append({
                    "module": mod.name,
                    "level": lvl,
                    "pdf": pdf,
                    "yt": yt
                })

        timetable.append({
            'subject': subject.name,
            'exam_date': subject.exam_date.strftime('%Y-%m-%d'),
            'days_remaining': days_until_exam,
            'level': overall_level,
            'daily_study_hours': daily_hours,
            'resources': resources,
            'id': str(subject_id)
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
