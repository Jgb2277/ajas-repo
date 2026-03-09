import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export default function SubjectsView() {
    const [subjects, setSubjects] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        axios.get('http://localhost:5000/api/student/subjects')
            .then(res => setSubjects(res.data))
            .catch(err => console.error('Failed fetching subjects', err));
    }, []);

    return (
        <div>
            <h3 style={{ marginBottom: '1.5rem', color: 'var(--text-light)', fontSize: '0.9rem', letterSpacing: '1px' }}>BROWSE SUBJECTS</h3>
            <div className="card-grid">
                {subjects.map(subj => (
                    <div className="card" key={subj.id} onClick={() => navigate(`/student/assessment/take/${subj.id}`)}>
                        <div style={{ fontSize: '1.2rem', marginBottom: '8px' }}>{subj.name}</div>
                        <div style={{ fontSize: '0.85rem', color: 'var(--text-light)' }}>
                            📅 {subj.exam_date || 'No Date'}
                        </div>
                        <div style={{ marginTop: '15px', padding: '6px 12px', background: '#ffebee', color: 'var(--primary)', borderRadius: '20px', fontSize: '0.8rem', fontWeight: 'bold', display: 'inline-block' }}>
                            Start Full Quiz →
                        </div>
                    </div>
                ))}
                {subjects.length === 0 && <p style={{ gridColumn: '1 / -1' }}>No subjects have been added by the admin yet.</p>}
            </div>
        </div>
    );
}
