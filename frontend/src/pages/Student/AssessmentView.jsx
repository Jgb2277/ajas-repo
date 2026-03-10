import React, { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';
import { AuthContext } from '../../context/AuthContext';

export default function AssessmentView() {
    const { subjectId } = useParams();          // only subjectId in URL now
    const { user } = useContext(AuthContext);
    const navigate = useNavigate();

    const [modules, setModules] = useState([]);
    const [currentModuleIndex, setCurrentModuleIndex] = useState(0);
    const [questions, setQuestions] = useState([]);
    const [answers, setAnswers] = useState({});
    const [loading, setLoading] = useState(true);
    const [submitting, setSubmitting] = useState(false);
    const [moduleResults, setModuleResults] = useState([]);  // result per module
    const [allDone, setAllDone] = useState(false);           // all modules submitted

    // Load all modules for the subject
    useEffect(() => {
        axios.get(`http://localhost:5000/api/student/subjects/${subjectId}/modules`)
            .then(res => {
                setModules(res.data);
                setLoading(false);
            })
            .catch(err => {
                console.error('Error fetching modules:', err);
                setLoading(false);
            });
    }, [subjectId]);

    // Load questions whenever the current module changes
    useEffect(() => {
        if (modules.length === 0) return;
        const mod = modules[currentModuleIndex];
        if (!mod) return;
        setLoading(true);
        setAnswers({});
        axios.get(`http://localhost:5000/api/student/modules/${mod.id}/questions`)
            .then(res => {
                setQuestions(res.data);
                setLoading(false);
            })
            .catch(err => {
                console.error('Error fetching questions:', err);
                setLoading(false);
            });
    }, [modules, currentModuleIndex]);

    const handleOptionSelect = (questionId, option) => {
        setAnswers(prev => ({ ...prev, [questionId]: option }));
    };

    const handleSubmitModule = async (e) => {
        e.preventDefault();
        setSubmitting(true);
        const mod = modules[currentModuleIndex];

        const formattedAnswers = Object.entries(answers).map(([qId, option]) => ({
            question_id: parseInt(qId),
            selected_option: option
        }));

        try {
            const res = await axios.post('http://localhost:5000/api/student/assessments', {
                user_id: user.id,
                subject_id: parseInt(subjectId),
                module_id: mod.id,
                answers: formattedAnswers
            });

            const result = { ...res.data, moduleName: mod.name };
            const updatedResults = [...moduleResults, result];
            setModuleResults(updatedResults);

            // Advance to next module or mark done
            if (currentModuleIndex + 1 < modules.length) {
                setCurrentModuleIndex(prev => prev + 1);
            } else {
                setAllDone(true);
            }
        } catch (err) {
            console.error('Submission failed', err);
            alert('Failed to submit module assessment.');
        }
        setSubmitting(false);
    };

    // ─── All modules done — Summary screen ───────────────────────────────────
    if (allDone) {
        const levelColor = (lvl) =>
            lvl === 'Advanced' ? '#28a745' : lvl === 'Intermediate' ? '#ffc107' : '#dc3545';
        const levelIcon = (lvl) =>
            lvl === 'Advanced' ? '🏆' : lvl === 'Intermediate' ? '📈' : '📚';

        return (
            <div style={{ maxWidth: '680px', margin: '0 auto', padding: '2rem 1rem' }}>
                <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
                    <div style={{ fontSize: '3.5rem', marginBottom: '0.75rem' }}>✅</div>
                    <h2 style={{ color: 'var(--text-dark)', marginBottom: '0.5rem' }}>All Modules Complete!</h2>
                    <p style={{ color: 'var(--text-light)', fontSize: '0.95rem' }}>
                        Here's a summary of your performance across all modules.
                    </p>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginBottom: '2.5rem' }}>
                    {moduleResults.map((r, idx) => (
                        <div key={idx} style={{
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'space-between',
                            padding: '1.25rem 1.5rem',
                            border: '1px solid #eaeaea',
                            borderRadius: '12px',
                            backgroundColor: '#fdfdfd'
                        }}>
                            <div>
                                <div style={{ fontWeight: '600', marginBottom: '4px' }}>{r.moduleName}</div>
                                <div style={{ fontSize: '0.82rem', color: 'var(--text-light)' }}>
                                    Basic: {r.scores.basic} &nbsp;|&nbsp; Inter: {r.scores.intermediate} &nbsp;|&nbsp; Adv: {r.scores.advanced}
                                </div>
                            </div>
                            <div style={{
                                display: 'flex',
                                alignItems: 'center',
                                gap: '6px',
                                padding: '6px 14px',
                                borderRadius: '20px',
                                fontSize: '0.85rem',
                                fontWeight: 'bold',
                                backgroundColor: r.level === 'Advanced' ? '#d4edda' : r.level === 'Intermediate' ? '#fff3cd' : '#f8d7da',
                                color: levelColor(r.level)
                            }}>
                                {levelIcon(r.level)} {r.level}
                            </div>
                        </div>
                    ))}
                </div>

                <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
                    <button className="btn btn-secondary" onClick={() => navigate('/student')}>Back to Home</button>
                    <button className="btn" onClick={() => navigate('/student/timetable')}>View Timetable →</button>
                </div>
            </div>
        );
    }

    // ─── Loading state ────────────────────────────────────────────────────────
    if (loading) return <div>Loading Assessment...</div>;
    if (modules.length === 0) return <div style={{ padding: '2rem' }}>No modules found for this subject.</div>;

    const currentModule = modules[currentModuleIndex];

    // ─── Quiz screen ──────────────────────────────────────────────────────────
    return (
        <div style={{ maxWidth: '800px', margin: '0 auto' }}>
            {/* Progress header */}
            <div style={{ marginBottom: '1.5rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
                    <h3 style={{ margin: 0 }}>Module Quiz — {currentModule.name}</h3>
                    <span style={{ padding: '6px 12px', backgroundColor: '#ffebee', color: 'var(--primary)', borderRadius: '20px', fontSize: '0.85rem', fontWeight: 'bold' }}>
                        {currentModuleIndex + 1} / {modules.length}
                    </span>
                </div>

                {/* Progress bar */}
                <div style={{ height: '6px', backgroundColor: '#f0f0f0', borderRadius: '3px', overflow: 'hidden' }}>
                    <div style={{
                        height: '100%',
                        width: `${((currentModuleIndex) / modules.length) * 100}%`,
                        backgroundColor: 'var(--primary)',
                        borderRadius: '3px',
                        transition: 'width 0.4s ease'
                    }} />
                </div>

                {/* Module breadcrumb */}
                <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.75rem', flexWrap: 'wrap' }}>
                    {modules.map((mod, idx) => (
                        <span key={mod.id} style={{
                            padding: '3px 10px',
                            borderRadius: '12px',
                            fontSize: '0.75rem',
                            fontWeight: idx === currentModuleIndex ? '700' : '400',
                            backgroundColor: idx < currentModuleIndex ? '#d4edda' : idx === currentModuleIndex ? '#ffebee' : '#f0f0f0',
                            color: idx < currentModuleIndex ? '#155724' : idx === currentModuleIndex ? 'var(--primary)' : 'var(--text-light)'
                        }}>
                            {idx < currentModuleIndex ? '✓ ' : ''}{mod.name}
                        </span>
                    ))}
                </div>
            </div>

            {/* Questions */}
            {questions.length === 0 ? (
                <div style={{ padding: '2rem', textAlign: 'center', border: '1px dashed #ccc', borderRadius: '12px' }}>
                    <p>No questions have been added for this module yet.</p>
                    <button className="btn" style={{ marginTop: '1rem' }} onClick={() => {
                        if (currentModuleIndex + 1 < modules.length) {
                            setCurrentModuleIndex(prev => prev + 1);
                        } else {
                            setAllDone(true);
                        }
                    }}>
                        {currentModuleIndex + 1 < modules.length ? 'Skip to Next Module →' : 'Finish'}
                    </button>
                </div>
            ) : (
                <form onSubmit={handleSubmitModule}>
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem', borderBottom: '1px solid #eaeaea', paddingBottom: '1rem' }}>
                        <span style={{ color: 'var(--text-light)', fontSize: '0.9rem' }}>Knowledge Assessment Quiz</span>
                        <span style={{ padding: '6px 12px', backgroundColor: '#f0f0f0', borderRadius: '20px', fontSize: '0.85rem' }}>
                            {questions.length} Questions
                        </span>
                    </div>

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
                                            style={{ marginRight: '10px' }}
                                        />
                                        {opt}
                                    </label>
                                ))}
                            </div>
                        </div>
                    ))}

                    <div style={{ textAlign: 'right', marginTop: '2rem', borderTop: '1px solid #eaeaea', paddingTop: '2rem' }}>
                        <button type="submit" className="btn" style={{ padding: '1rem 3rem', fontSize: '1.1rem' }} disabled={submitting}>
                            {submitting ? 'Submitting...' : currentModuleIndex + 1 < modules.length ? `Submit & Next Module →` : 'Submit Final Module ✓'}
                        </button>
                    </div>
                </form>
            )}
        </div>
    );
}
