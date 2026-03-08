import React, { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';
import { AuthContext } from '../../context/AuthContext';

export default function AssessmentView() {
    const { subjectId, moduleId } = useParams();
    const { user } = useContext(AuthContext);
    const navigate = useNavigate();

    const [questions, setQuestions] = useState([]);
    const [answers, setAnswers] = useState({}); // { question_id: selected_option }
    const [loading, setLoading] = useState(true);
    const [submitting, setSubmitting] = useState(false);
    const [result, setResult] = useState(null);

    useEffect(() => {
        // Fetch questions for module
        if (moduleId) {
            axios.get(`http://localhost:5000/api/student/modules/${moduleId}/questions`)
                .then(res => {
                    setQuestions(res.data);
                    setLoading(false);
                })
                .catch(err => {
                    console.error('Error fetching questions:', err);
                    setLoading(false);
                });
        }
    }, [moduleId]);

    const handleOptionSelect = (questionId, option) => {
        setAnswers(prev => ({
            ...prev,
            [questionId]: option
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setSubmitting(true);

        // Format answers array
        const formattedAnswers = Object.entries(answers).map(([qId, option]) => ({
            question_id: parseInt(qId),
            selected_option: option
        }));

        try {
            const res = await axios.post('http://localhost:5000/api/student/assessments', {
                user_id: user.id,
                subject_id: parseInt(subjectId),
                answers: formattedAnswers
            });
            setResult(res.data);
        } catch (err) {
            console.error('Submission failed', err);
            alert('Failed to submit assessment.');
        }
        setSubmitting(false);
    };

    if (loading) return <div>Loading Assessment...</div>;

    if (result) {
        return (
            <div style={{ maxWidth: '600px', margin: '0 auto', textAlign: 'center', padding: '3rem 2rem', backgroundColor: '#f9f9f9', borderRadius: '16px', border: '1px solid #eaeaea' }}>
                <div style={{ fontSize: '4rem', marginBottom: '1rem', color: result.level === 'Advanced' ? '#28a745' : result.level === 'Intermediate' ? '#ffc107' : '#dc3545' }}>
                    {result.level === 'Advanced' ? '🏆' : result.level === 'Intermediate' ? '📈' : '📚'}
                </div>
                <h2 style={{ color: 'var(--text-dark)', marginBottom: '1rem' }}>Assessment Complete!</h2>
                <p style={{ fontSize: '1.2rem', marginBottom: '2rem' }}>You have been assigned to the <strong>{result.level}</strong> level based on algorithmic evaluation.</p>

                <div style={{ display: 'flex', justifyContent: 'center', gap: '2rem', marginBottom: '2.5rem' }}>
                    <div style={{ textAlign: 'center' }}>
                        <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{result.scores.basic}</div>
                        <div style={{ fontSize: '0.85rem', color: 'var(--text-light)', textTransform: 'uppercase' }}>Basic</div>
                    </div>
                    <div style={{ textAlign: 'center' }}>
                        <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{result.scores.intermediate}</div>
                        <div style={{ fontSize: '0.85rem', color: 'var(--text-light)', textTransform: 'uppercase' }}>Intermediate</div>
                    </div>
                    <div style={{ textAlign: 'center' }}>
                        <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{result.scores.advanced}</div>
                        <div style={{ fontSize: '0.85rem', color: 'var(--text-light)', textTransform: 'uppercase' }}>Advanced</div>
                    </div>
                </div>

                <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
                    <button className="btn btn-secondary" onClick={() => navigate('/student')}>Back to Home</button>
                    <button className="btn" onClick={() => navigate('/student/timetable')}>View New Timetable</button>
                </div>
            </div>
        );
    }

    return (
        <div style={{ maxWidth: '800px', margin: '0 auto' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '2rem', borderBottom: '1px solid #eaeaea', paddingBottom: '1rem' }}>
                <h3>Knowledge Assessment Quiz</h3>
                <span style={{ padding: '6px 12px', backgroundColor: '#ffebee', color: 'var(--primary)', borderRadius: '20px', fontSize: '0.85rem', fontWeight: 'bold' }}>
                    {questions.length} Questions
                </span>
            </div>

            {questions.length === 0 ? (
                <p>No questions have been added for this module yet.</p>
            ) : (
                <form onSubmit={handleSubmit}>
                    {questions.map((q, i) => (
                        <div key={q.id} style={{ marginBottom: '2rem', padding: '1.5rem', backgroundColor: '#fdfdfd', border: '1px solid #eaeaea', borderRadius: '12px' }}>
                            <h4 style={{ marginBottom: '1rem', fontWeight: '600', fontSize: '1.05rem' }}>
                                <span style={{ color: 'var(--primary)', marginRight: '8px' }}>{i + 1}.</span>
                                {q.text}
                            </h4>
                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                                {q.options && q.options.map((opt, idx) => (
                                    <label key={idx} style={{
                                        display: 'flex',
                                        alignItems: 'center',
                                        padding: '1rem',
                                        border: answers[q.id] === opt ? '2px solid var(--primary)' : '1px solid #ddd',
                                        borderRadius: '8px',
                                        cursor: 'pointer',
                                        backgroundColor: answers[q.id] === opt ? '#fffafa' : 'white',
                                        transition: 'all 0.2s',
                                        fontWeight: answers[q.id] === opt ? '600' : '400'
                                    }}>
                                        <input
                                            type="radio"
                                            name={`question_${q.id}`}
                                            value={opt}
                                            onChange={() => handleOptionSelect(q.id, opt)}
                                            required
                                            style={{ marginRight: '10px' }}
                                        />
                                        {opt}
                                    </label>
                                ))}
                            </div>
                        </div>
                    ))}

                    <div style={{ textAlign: 'right', marginTop: '2rem', borderTop: '1px solid #eaeaea', paddingTop: '2rem' }}>
                        <button type="submit" className="btn" style={{ padding: '1rem 3rem', fontSize: '1.1rem' }} disabled={submitting || questions.length === 0}>
                            {submitting ? 'Auto-Evaluating...' : 'Submit Assessment'}
                        </button>
                    </div>
                </form>
            )}
        </div>
    );
}
