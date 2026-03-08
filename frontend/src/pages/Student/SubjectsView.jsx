import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export default function SubjectsView() {
    const [subjects, setSubjects] = useState([]);
    const [selectedSubject, setSelectedSubject] = useState(null);
    const [modules, setModules] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        axios.get('http://localhost:5000/api/student/subjects')
            .then(res => setSubjects(res.data))
            .catch(err => console.error('Failed fetching subjects', err));
    }, []);

    const handleSubjectClick = (subj) => {
        setSelectedSubject(subj);
        axios.get(`http://localhost:5000/api/student/subjects/${subj.id}/modules`)
            .then(res => setModules(res.data))
            .catch(err => console.error('Failed fetching modules', err));
    };

    if (selectedSubject) {
        return (
            <div>
                <button className="btn btn-secondary" onClick={() => setSelectedSubject(null)} style={{ marginBottom: '1.5rem', display: 'inline-block' }}>
                    &larr; Back to Subject Selection
                </button>
                <h3 style={{ marginBottom: '0.5rem' }}>{selectedSubject.name}</h3>
                <p style={{ marginBottom: '2rem', color: 'var(--text-light)' }}>Exam Date: {selectedSubject.exam_date || 'No Date Set'}</p>

                <h4 style={{ marginBottom: '1rem', color: 'var(--text-light)', fontSize: '0.9rem', letterSpacing: '1px' }}>MODULES & ASSESSMENTS</h4>
                <div className="card-grid">
                    {modules.map(mod => (
                        <div className="card" key={mod.id} onClick={() => navigate(`/student/assessment/take/${selectedSubject.id}/${mod.id}`)}>
                            <div style={{ fontSize: '1.1rem' }}>{mod.name}</div>
                            <div style={{ marginTop: '15px', padding: '6px 12px', background: '#ffebee', color: 'var(--primary)', borderRadius: '20px', fontSize: '0.8rem', fontWeight: 'bold' }}>
                                Take Module Quiz &rarr;
                            </div>
                        </div>
                    ))}
                    {modules.length === 0 && <p style={{ gridColumn: '1 / -1' }}>No modules available for this subject.</p>}
                </div>
            </div>
        );
    }

    return (
        <div>
            <h3 style={{ marginBottom: '1.5rem', color: 'var(--text-light)', fontSize: '0.9rem', letterSpacing: '1px' }}>BROWSE SUBJECTS</h3>
            <div className="card-grid">
                {subjects.map(subj => (
                    <div className="card" key={subj.id} onClick={() => handleSubjectClick(subj)}>
                        <div style={{ fontSize: '1.2rem', marginBottom: '8px' }}>{subj.name}</div>
                        <div style={{ fontSize: '0.85rem', color: 'var(--text-light)' }}>
                            📅 {subj.exam_date || 'No Date'}
                        </div>
                    </div>
                ))}
                {subjects.length === 0 && <p style={{ gridColumn: '1 / -1' }}>No subjects have been added by the admin yet.</p>}
            </div>
        </div>
    );
}
