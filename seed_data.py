from app import app
from models import db, Subject, Module

with app.app_context():

    # Reset DB (since currently empty)
    db.drop_all()
    db.create_all()

    # Insert Subjects
    subject_names = ["AAD", "IEFT", "PYTHON", "CG", "CD", "ML"]

    subjects = []

    for name in subject_names:
        subject = Subject(subject_name=name)
        db.session.add(subject)
        subjects.append(subject)

    db.session.commit()

    # Insert 5 Modules for each subject
    for subject in subjects:
        for i in range(1, 6):
            module = Module(
                module_name=f"Module {i}",
                subject_id=subject.id
            )
            db.session.add(module)

    db.session.commit()

    print("Subjects and Modules inserted successfully!")
