from flask import Blueprint, request, jsonify
from models import db, Subject, Module, Question

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/subjects', methods=['GET', 'POST'])
def manage_subjects():
    if request.method == 'POST':
        data = request.json
        name = data.get('name')
        exam_date_str = data.get('exam_date')
        
        from datetime import datetime
        exam_date = datetime.strptime(exam_date_str, '%Y-%m-%d').date() if exam_date_str else None
        
        subject = Subject(name=name, exam_date=exam_date)
        db.session.add(subject)
        db.session.commit()
        return jsonify({'message': 'Subject created', 'id': subject.id}), 201
        
    subjects = Subject.query.all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'exam_date': s.exam_date.strftime('%Y-%m-%d') if s.exam_date else None
    } for s in subjects])

@admin_bp.route('/modules', methods=['GET', 'POST'])
def manage_modules():
    if request.method == 'GET':
        subject_id = request.args.get('subject_id')
        if not subject_id:
            return jsonify([])
        modules = Module.query.filter_by(subject_id=subject_id).all()
        return jsonify([{'id': m.id, 'name': m.name, 'subject_id': m.subject_id} for m in modules])

    data = request.json
    subject_id = data.get('subject_id')
    name = data.get('name')
    
    module = Module(subject_id=subject_id, name=name)
    db.session.add(module)
    db.session.commit()
    return jsonify({'message': 'Module created', 'id': module.id}), 201

@admin_bp.route('/modules/<int:module_id>', methods=['DELETE'])
def delete_module(module_id):
    module = Module.query.get(module_id)
    if not module:
        return jsonify({'error': 'Module not found'}), 404
    # Delete associated questions first
    Question.query.filter_by(module_id=module_id).delete()
    db.session.delete(module)
    db.session.commit()
    return jsonify({'message': 'Module deleted successfully'}), 200

@admin_bp.route('/questions', methods=['POST'])
def add_question():
    data = request.json
    import json
    question = Question(
        module_id=data.get('module_id'),
        text=data.get('text'),
        difficulty=data.get('difficulty'),
        options=json.dumps(data.get('options')),
        correct_option=data.get('correct_option')
    )
    db.session.add(question)
    db.session.commit()
    return jsonify({'message': 'Question created', 'id': question.id}), 201

import os
from werkzeug.utils import secure_filename
from flask import current_app

@admin_bp.route('/notes', methods=['POST'])
def upload_notes():
    module_id = request.form.get('module_id')
    level = request.form.get('level') # 'basic', 'intermediate', 'advanced'
    yt_link = request.form.get('yt_link', '')
    
    module = Module.query.get(module_id)
    if not module or level not in ['basic', 'intermediate', 'advanced']:
        return jsonify({'error': 'Invalid module or level'}), 400

    pdf_files = request.files.getlist('pdf_files')
    new_paths = []
    for pdf_file in pdf_files:
        if pdf_file and pdf_file.filename:
            import uuid
            unique_id = uuid.uuid4().hex[:8]
            filename = secure_filename(f"{module_id}_{level}_{unique_id}_{pdf_file.filename}")
            save_path = os.path.join(current_app.root_path, 'uploads', 'pdfs', filename)
            pdf_file.save(save_path)
            new_paths.append(f"/files/{filename}")

    if level == 'basic':
        module.basic_yt = yt_link
        if new_paths:
            existing = module.basic_pdf or ''
            all_paths = [p for p in existing.split(',') if p] + new_paths
            module.basic_pdf = ','.join(all_paths)
    elif level == 'intermediate':
        module.intermediate_yt = yt_link
        if new_paths:
            existing = module.intermediate_pdf or ''
            all_paths = [p for p in existing.split(',') if p] + new_paths
            module.intermediate_pdf = ','.join(all_paths)
    elif level == 'advanced':
        module.advanced_yt = yt_link
        if new_paths:
            existing = module.advanced_pdf or ''
            all_paths = [p for p in existing.split(',') if p] + new_paths
            module.advanced_pdf = ','.join(all_paths)

    db.session.commit()
    return jsonify({'message': f'{level.capitalize()} notes updated successfully', 'pdf_count': len(new_paths)}), 200
