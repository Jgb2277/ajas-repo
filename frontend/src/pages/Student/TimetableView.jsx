import React, { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import { AuthContext } from '../../context/AuthContext';

export default function TimetableView() {
    const { user } = useContext(AuthContext);
    const [timetable, setTimetable] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        axios.get(`http://localhost:5000/api/student/timetable/${user.id}`)
            .then(res => {
                setTimetable(res.data);
                setLoading(false);
            })
            .catch(err => {
                console.error('Failed fetching timetable', err);
                setLoading(false);
            });
    }, [user.id]);

    if (loading) return <div>Loading intelligent timetable...</div>;

    return (
        <div>
            <h3 style={{ marginBottom: '0.5rem', color: 'var(--text-dark)', fontSize: '1.4rem' }}>Smart Study Timetable</h3>
            <p style={{ marginBottom: '2rem', color: 'var(--text-light)', fontSize: '0.95rem' }}>
                Your dynamic study plan based on assessment results. High proficiency requires less daily study time, while lower scores assign extra time.
            </p>

            {timetable.length === 0 ? (
                <div style={{ padding: '3rem', textAlign: 'center', backgroundColor: '#f9f9f9', borderRadius: '12px', border: '1px dashed #ccc' }}>
                    <p style={{ fontWeight: '500', fontSize: '1.1rem', marginBottom: '0.5rem' }}>No study timetable available yet.</p>
                    <p style={{ fontSize: '0.95rem', color: 'var(--text-light)' }}>
                        This is generated automatically after you take module assessments for subjects that have an exam date scheduled at least 4 days away.
                    </p>
                </div>
            ) : (
                <div style={{ overflowX: 'auto', borderRadius: '12px', border: '1px solid rgba(0,0,0,0.08)' }}>
                    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                        <thead>
                            <tr style={{ backgroundColor: '#fafafa', borderBottom: '2px solid #eaeaea' }}>
                                <th style={{ padding: '1.25rem 1rem', textAlign: 'left', fontWeight: 'bold', color: 'var(--text-light)', textTransform: 'uppercase', fontSize: '0.8rem', letterSpacing: '1px' }}>Subject</th>
                                <th style={{ padding: '1.25rem 1rem', textAlign: 'left', fontWeight: 'bold', color: 'var(--text-light)', textTransform: 'uppercase', fontSize: '0.8rem', letterSpacing: '1px' }}>Exam Date</th>
                                <th style={{ padding: '1.25rem 1rem', textAlign: 'left', fontWeight: 'bold', color: 'var(--text-light)', textTransform: 'uppercase', fontSize: '0.8rem', letterSpacing: '1px' }}>Days Left</th>
                                <th style={{ padding: '1.25rem 1rem', textAlign: 'left', fontWeight: 'bold', color: 'var(--text-light)', textTransform: 'uppercase', fontSize: '0.8rem', letterSpacing: '1px' }}>Level</th>
                                <th style={{ padding: '1.25rem 1rem', textAlign: 'left', fontWeight: 'bold', color: 'var(--text-light)', textTransform: 'uppercase', fontSize: '0.8rem', letterSpacing: '1px' }}>Daily Plan</th>
                                <th style={{ padding: '1.25rem 1rem', textAlign: 'left', fontWeight: 'bold', color: 'var(--text-light)', textTransform: 'uppercase', fontSize: '0.8rem', letterSpacing: '1px' }}>Action Plan & Notes</th>
                            </tr>
                        </thead>
                        <tbody>
                            {timetable.map((item, idx) => (
                                <tr key={idx} style={{ borderBottom: '1px solid #eaeaea' }}>
                                    <td style={{ padding: '1.25rem 1rem', fontWeight: '600', color: 'var(--text-dark)' }}>{item.subject}</td>
                                    <td style={{ padding: '1.25rem 1rem' }}>{item.exam_date}</td>
                                    <td style={{ padding: '1.25rem 1rem' }}>{item.days_remaining} days</td>
                                    <td style={{ padding: '1.25rem 1rem' }}>
                                        <span style={{
                                            padding: '6px 12px',
                                            borderRadius: '20px',
                                            fontSize: '0.8rem',
                                            fontWeight: 'bold',
                                            backgroundColor: item.level === 'Advanced' ? '#d4edda' : item.level === 'Intermediate' ? '#fff3cd' : '#f8d7da',
                                            color: item.level === 'Advanced' ? '#155724' : item.level === 'Intermediate' ? '#856404' : '#721c24'
                                        }}>
                                            {item.level}
                                        </span>
                                    </td>
                                    <td style={{ padding: '1.25rem 1rem', fontWeight: 'bold', color: 'var(--primary)' }}>
                                        {item.daily_study_hours} Hours
                                    </td>
                                    <td style={{ padding: '1.25rem 1rem', color: 'var(--text-light)', fontSize: '0.9rem' }}>
                                        {item.resources && item.resources.length > 0 ? (
                                            <ul style={{ listStyleType: 'none', padding: 0, margin: 0 }}>
                                                {item.resources.map((res, i) => (
                                                    <li key={i} style={{ marginBottom: '0.5rem' }}>
                                                        <strong>{res.module}:</strong>{' '}
                                                        {res.pdf && <a href={`http://localhost:5000${res.pdf}`} target="_blank" rel="noreferrer" style={{ color: 'var(--primary)', textDecoration: 'none', marginRight: '8px', fontWeight: 'bold' }}>[PDF]</a>}
                                                        {res.yt && <a href={res.yt} target="_blank" rel="noreferrer" style={{ color: '#ff0000', textDecoration: 'none', fontWeight: 'bold' }}>[YouTube]</a>}
                                                    </li>
                                                ))}
                                            </ul>
                                        ) : (
                                            "No specific resources for this level."
                                        )}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
}
