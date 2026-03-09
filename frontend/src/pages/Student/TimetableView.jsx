import React, { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import { AuthContext } from '../../context/AuthContext';

export default function TimetableView() {
    const { user } = useContext(AuthContext);
    const [timetable, setTimetable] = useState([]);
    const [loading, setLoading] = useState(true);
    const [expanded, setExpanded] = useState({});   // { subjectId: bool }

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

    const toggleExpand = (id) => {
        setExpanded(prev => ({ ...prev, [id]: !prev[id] }));
    };

    const levelStyle = (level) => ({
        padding: '5px 12px',
        borderRadius: '20px',
        fontSize: '0.8rem',
        fontWeight: 'bold',
        backgroundColor: level === 'Advanced' ? '#d4edda' : level === 'Intermediate' ? '#fff3cd' : '#f8d7da',
        color: level === 'Advanced' ? '#155724' : level === 'Intermediate' ? '#856404' : '#721c24'
    });

    if (loading) return <div>Loading intelligent timetable...</div>;

    return (
        <div>
            <h3 style={{ marginBottom: '0.5rem', color: 'var(--text-dark)', fontSize: '1.4rem' }}>Smart Study Timetable</h3>
            <p style={{ marginBottom: '2rem', color: 'var(--text-light)', fontSize: '0.95rem' }}>
                Your dynamic study plan based on assessment results. Each subject shows per-module notes and YouTube links.
            </p>

            {timetable.length === 0 ? (
                <div style={{ padding: '3rem', textAlign: 'center', backgroundColor: '#f9f9f9', borderRadius: '12px', border: '1px dashed #ccc' }}>
                    <p style={{ fontWeight: '500', fontSize: '1.1rem', marginBottom: '0.5rem' }}>No study timetable available yet.</p>
                    <p style={{ fontSize: '0.95rem', color: 'var(--text-light)' }}>
                        This is generated automatically after you complete module quizzes for subjects with an exam date at least 4 days away.
                    </p>
                </div>
            ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
                    {timetable.map((item, idx) => (
                        <div key={idx} style={{
                            border: '1px solid rgba(0,0,0,0.08)',
                            borderRadius: '14px',
                            overflow: 'hidden',
                            backgroundColor: '#fff',
                            boxShadow: '0 2px 8px rgba(0,0,0,0.04)'
                        }}>
                            {/* Subject header row */}
                            <div style={{
                                display: 'grid',
                                gridTemplateColumns: '2fr 1fr 1fr 1fr 1fr auto',
                                alignItems: 'center',
                                padding: '1.25rem 1.5rem',
                                backgroundColor: '#fafafa',
                                borderBottom: expanded[item.id] ? '1px solid #eaeaea' : 'none',
                                gap: '1rem'
                            }}>
                                <div>
                                    <div style={{ fontWeight: '700', fontSize: '1.05rem', color: 'var(--text-dark)', marginBottom: '2px' }}>
                                        {item.subject}
                                    </div>
                                    <div style={{ fontSize: '0.8rem', color: 'var(--text-light)' }}>📅 Exam: {item.exam_date}</div>
                                </div>
                                <div style={{ fontSize: '0.9rem' }}>
                                    <span style={{ color: 'var(--text-light)', fontSize: '0.75rem', display: 'block', marginBottom: '2px' }}>DAYS LEFT</span>
                                    <strong>{item.days_remaining}</strong>
                                </div>
                                <div>
                                    <span style={levelStyle(item.level)}>{item.level}</span>
                                </div>
                                <div style={{ fontSize: '0.9rem' }}>
                                    <span style={{ color: 'var(--text-light)', fontSize: '0.75rem', display: 'block', marginBottom: '2px' }}>DAILY</span>
                                    <strong style={{ color: 'var(--primary)' }}>{item.daily_study_hours}h</strong>
                                </div>
                                <div style={{ fontSize: '0.8rem', color: 'var(--text-light)' }}>
                                    {item.resources.length} module{item.resources.length !== 1 ? 's' : ''} with resources
                                </div>
                                <button
                                    onClick={() => toggleExpand(item.id)}
                                    style={{
                                        background: 'none',
                                        border: '1px solid #ddd',
                                        borderRadius: '8px',
                                        padding: '6px 12px',
                                        cursor: 'pointer',
                                        fontSize: '0.8rem',
                                        color: 'var(--text-light)',
                                        transition: 'all 0.2s',
                                        whiteSpace: 'nowrap'
                                    }}
                                >
                                    {expanded[item.id] ? '▲ Hide Notes' : '▼ Show Notes'}
                                </button>
                            </div>

                            {/* Per-module resources — collapsible */}
                            {expanded[item.id] && (
                                <div style={{ padding: '1.25rem 1.5rem' }}>
                                    {item.resources.length === 0 ? (
                                        <p style={{ color: 'var(--text-light)', fontSize: '0.9rem', margin: 0 }}>
                                            No specific resources uploaded for this subject yet.
                                        </p>
                                    ) : (
                                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
                                            {item.resources.map((res, i) => (
                                                <div key={i} style={{
                                                    display: 'flex',
                                                    alignItems: 'center',
                                                    justifyContent: 'space-between',
                                                    padding: '0.85rem 1.1rem',
                                                    backgroundColor: '#f9f9f9',
                                                    borderRadius: '10px',
                                                    border: '1px solid #f0f0f0',
                                                    flexWrap: 'wrap',
                                                    gap: '0.5rem'
                                                }}>
                                                    <div>
                                                        <strong style={{ fontSize: '0.9rem', color: 'var(--text-dark)' }}>{res.module}</strong>
                                                        <span style={{
                                                            marginLeft: '8px',
                                                            ...levelStyle(res.level),
                                                            fontSize: '0.72rem',
                                                            padding: '2px 8px'
                                                        }}>{res.level}</span>
                                                    </div>
                                                    <div style={{ display: 'flex', gap: '0.6rem' }}>
                                                        {res.pdf && (
                                                            <a
                                                                href={`http://localhost:5000${res.pdf}`}
                                                                target="_blank"
                                                                rel="noreferrer"
                                                                style={{
                                                                    padding: '5px 12px',
                                                                    backgroundColor: '#fff3e0',
                                                                    color: '#e65100',
                                                                    borderRadius: '8px',
                                                                    fontSize: '0.8rem',
                                                                    fontWeight: 'bold',
                                                                    textDecoration: 'none'
                                                                }}
                                                            >
                                                                📄 PDF Notes
                                                            </a>
                                                        )}
                                                        {res.yt && (
                                                            <a
                                                                href={res.yt}
                                                                target="_blank"
                                                                rel="noreferrer"
                                                                style={{
                                                                    padding: '5px 12px',
                                                                    backgroundColor: '#ffebee',
                                                                    color: '#c62828',
                                                                    borderRadius: '8px',
                                                                    fontSize: '0.8rem',
                                                                    fontWeight: 'bold',
                                                                    textDecoration: 'none'
                                                                }}
                                                            >
                                                                ▶ YouTube
                                                            </a>
                                                        )}
                                                        {!res.pdf && !res.yt && (
                                                            <span style={{ fontSize: '0.8rem', color: 'var(--text-light)' }}>No links uploaded</span>
                                                        )}
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
