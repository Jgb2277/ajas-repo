import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API = 'http://localhost:5000';

export function ManageSubjects() {
    const [subjects, setSubjects] = useState([]);
    const [name, setName] = useState('');
    const [examDate, setExamDate] = useState('');

    const fetchSubjects = () => {
        axios.get(`${API}/api/admin/subjects`)
            .then(res => setSubjects(res.data))
            .catch(console.error);
    };

    useEffect(() => fetchSubjects(), []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await axios.post(`${API}/api/admin/subjects`, { name, exam_date: examDate });
            setName('');
            setExamDate('');
            fetchSubjects();
            alert('Subject created successfully!');
        } catch (err) {
            console.error(err);
            alert('Failed to create subject.');
        }
    };

    return (
        <div>
            <h3 style={{ marginBottom: '1.5rem' }}>Manage Subjects &amp; Notes Link</h3>
            <form onSubmit={handleSubmit} style={{ maxWidth: '500px', display: 'flex', flexDirection: 'column', gap: '1rem', marginBottom: '2.5rem', padding: '1.5rem', backgroundColor: '#f9f9f9', borderRadius: '12px', border: '1px solid #eaeaea' }}>
                <div>
                    <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Subject Name</label>
                    <input className="input-field" value={name} onChange={e => setName(e.target.value)} required placeholder="e.g. Advanced Data Structures" />
                </div>
                <div>
                    <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Exam Date</label>
                    <input className="input-field" type="date" value={examDate} onChange={e => setExamDate(e.target.value)} required />
                </div>
                <button type="submit" className="btn" style={{ alignSelf: 'flex-start' }}>Add Subject</button>
            </form>

            <h4>Existing Subjects</h4>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Exam Date</th>
                    </tr>
                </thead>
                <tbody>
                    {subjects.map(s => (
                        <tr key={s.id}>
                            <td>{s.id}</td>
                            <td style={{ fontWeight: 'bold' }}>{s.name}</td>
                            <td>{s.exam_date || 'Not Set'}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export function ManageModules() {
    const [subjects, setSubjects] = useState([]);
    const [selectedSubject, setSelectedSubject] = useState('');
    const [moduleName, setModuleName] = useState('');
    const [modules, setModules] = useState([]);

    useEffect(() => {
        axios.get(`${API}/api/admin/subjects`).then(res => {
            setSubjects(res.data);
            if (res.data.length > 0) {
                setSelectedSubject(res.data[0].id);
                fetchModules(res.data[0].id);
            }
        });
    }, []);

    const fetchModules = (subjId) => {
        axios.get(`${API}/api/admin/modules?subject_id=${subjId}`).then(res => {
            setModules(res.data);
        }).catch(console.error);
    };

    const handleSubjectChange = (e) => {
        const val = e.target.value;
        setSelectedSubject(val);
        fetchModules(val);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await axios.post(`${API}/api/admin/modules`, {
                subject_id: selectedSubject,
                name: moduleName
            });
            setModuleName('');
            fetchModules(selectedSubject);
            alert('Module created successfully!');
        } catch (err) {
            console.error(err);
            alert('Failed to create module.');
        }
    };

    const handleDelete = async (moduleId, moduleName) => {
        if (!window.confirm(`Are you sure you want to delete "${moduleName}"? This will also remove all associated questions.`)) return;
        try {
            await axios.delete(`${API}/api/admin/modules/${moduleId}`);
            fetchModules(selectedSubject);
            alert('Module deleted successfully!');
        } catch (err) {
            console.error(err);
            alert('Failed to delete module.');
        }
    };

    const selectedSubjectName = subjects.find(s => String(s.id) === String(selectedSubject))?.name || '';

    return (
        <div>
            <h3 style={{ marginBottom: '1.5rem' }}>Create Module / Chapter</h3>
            <form onSubmit={handleSubmit} style={{ maxWidth: '600px', display: 'flex', flexDirection: 'column', gap: '1rem', padding: '1.5rem', backgroundColor: '#f9f9f9', borderRadius: '12px', border: '1px solid #eaeaea' }}>
                <div>
                    <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Select Subject</label>
                    <select className="input-field" value={selectedSubject} onChange={handleSubjectChange} required>
                        {subjects.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
                    </select>
                </div>
                <div>
                    <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Module Title</label>
                    <input className="input-field" value={moduleName} onChange={e => setModuleName(e.target.value)} required placeholder="e.g. Chapter 1: Sorting Algorithms" />
                </div>
                <button type="submit" className="btn" style={{ alignSelf: 'flex-start' }}>Add Module</button>
            </form>

            <div style={{ marginTop: '2.5rem' }}>
                <h4 style={{ marginBottom: '1rem' }}>
                    Modules for: <span style={{ color: 'var(--primary)' }}>{selectedSubjectName || '—'}</span>
                </h4>
                {modules.length === 0 ? (
                    <p style={{ color: 'var(--text-light)', fontStyle: 'italic' }}>No modules yet for this subject. Add one above.</p>
                ) : (
                    <div style={{ overflowX: 'auto' }}>
                        <table>
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Module Name</th>
                                    <th style={{ textAlign: 'center' }}>Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                {modules.map(m => (
                                    <tr key={m.id}>
                                        <td>{m.id}</td>
                                        <td style={{ fontWeight: 'bold' }}>{m.name}</td>
                                        <td style={{ textAlign: 'center' }}>
                                            <button
                                                onClick={() => handleDelete(m.id, m.name)}
                                                title="Delete module"
                                                style={{
                                                    background: 'none',
                                                    border: '1px solid #e74c3c',
                                                    color: '#e74c3c',
                                                    padding: '0.35rem 0.75rem',
                                                    borderRadius: '6px',
                                                    cursor: 'pointer',
                                                    fontSize: '0.85rem',
                                                    fontWeight: '600',
                                                    transition: 'all 0.2s ease',
                                                    display: 'inline-flex',
                                                    alignItems: 'center',
                                                    gap: '0.3rem',
                                                }}
                                                onMouseEnter={e => { e.target.style.background = '#e74c3c'; e.target.style.color = '#fff'; }}
                                                onMouseLeave={e => { e.target.style.background = 'none'; e.target.style.color = '#e74c3c'; }}
                                            >
                                                🗑️ Delete
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </div>
    );
}

export function AddQuestions() {
    const [subjects, setSubjects] = useState([]);
    const [modules, setModules] = useState([]);
    const [selectedSubject, setSelectedSubject] = useState('');
    const [selectedModule, setSelectedModule] = useState('');

    const [text, setText] = useState('');
    const [difficulty, setDifficulty] = useState('basic');
    const [optA, setOptA] = useState('');
    const [optB, setOptB] = useState('');
    const [optC, setOptC] = useState('');
    const [optD, setOptD] = useState('');
    const [correct, setCorrect] = useState('A');

    useEffect(() => {
        axios.get(`${API}/api/admin/subjects`).then(res => {
            setSubjects(res.data);
            if (res.data.length > 0) {
                setSelectedSubject(res.data[0].id);
                fetchModules(res.data[0].id);
            }
        });
    }, []);

    const fetchModules = (subjId) => {
        axios.get(`${API}/api/student/subjects/${subjId}/modules`).then(res => {
            setModules(res.data);
            if (res.data.length > 0) setSelectedModule(res.data[0].id);
            else setSelectedModule('');
        });
    };

    const handleSubjectChange = (e) => {
        const val = e.target.value;
        setSelectedSubject(val);
        fetchModules(val);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!selectedModule) return alert('Please select a module first');

        const options = [optA, optB, optC, optD];
        const correctVal = correct === 'A' ? optA : correct === 'B' ? optB : correct === 'C' ? optC : optD;

        try {
            await axios.post(`${API}/api/admin/questions`, {
                module_id: selectedModule,
                text,
                difficulty,
                options,
                correct_option: correctVal
            });
            setText(''); setOptA(''); setOptB(''); setOptC(''); setOptD('');
            alert('Question uploaded successfully!');
        } catch (err) {
            console.error(err);
            alert('Failed to upload question');
        }
    };

    return (
        <div>
            <h3 style={{ marginBottom: '1.5rem' }}>Add Quiz Questions</h3>
            <form onSubmit={handleSubmit} style={{ maxWidth: '700px', display: 'flex', flexDirection: 'column', gap: '1rem', padding: '1.5rem', backgroundColor: '#fdfdfd', borderRadius: '12px', border: '1px solid #eaeaea' }}>
                <div style={{ display: 'flex', gap: '1rem' }}>
                    <div style={{ flex: 1 }}>
                        <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Subject</label>
                        <select className="input-field" value={selectedSubject} onChange={handleSubjectChange} required>
                            {subjects.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
                        </select>
                    </div>
                    <div style={{ flex: 1 }}>
                        <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Module</label>
                        <select className="input-field" value={selectedModule} onChange={e => setSelectedModule(e.target.value)} required>
                            {modules.map(m => <option key={m.id} value={m.id}>{m.name}</option>)}
                            {modules.length === 0 && <option value="">No modules found</option>}
                        </select>
                    </div>
                </div>

                <hr style={{ margin: '1rem 0', borderTop: '1px solid #ddd' }} />

                <div>
                    <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Question Text</label>
                    <textarea className="input-field" value={text} onChange={e => setText(e.target.value)} required placeholder="What is the time complexity of QuickSort?" style={{ minHeight: '80px', fontFamily: 'inherit' }} />
                </div>

                <div>
                    <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Difficulty Level</label>
                    <select className="input-field" value={difficulty} onChange={e => setDifficulty(e.target.value)} required>
                        <option value="basic">Basic</option>
                        <option value="intermediate">Intermediate</option>
                        <option value="advanced">Advanced</option>
                    </select>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                    <div><label style={{ fontWeight: 'bold' }}>Option A</label><input required className="input-field" value={optA} onChange={e => setOptA(e.target.value)} /></div>
                    <div><label style={{ fontWeight: 'bold' }}>Option B</label><input required className="input-field" value={optB} onChange={e => setOptB(e.target.value)} /></div>
                    <div><label style={{ fontWeight: 'bold' }}>Option C</label><input required className="input-field" value={optC} onChange={e => setOptC(e.target.value)} /></div>
                    <div><label style={{ fontWeight: 'bold' }}>Option D</label><input required className="input-field" value={optD} onChange={e => setOptD(e.target.value)} /></div>
                </div>

                <div>
                    <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Correct Option</label>
                    <select className="input-field" value={correct} onChange={e => setCorrect(e.target.value)} required style={{ width: '200px' }}>
                        <option value="A">A</option>
                        <option value="B">B</option>
                        <option value="C">C</option>
                        <option value="D">D</option>
                    </select>
                </div>

                <button type="submit" className="btn" style={{ alignSelf: 'flex-start', marginTop: '1rem' }}>Save Question to Database</button>
            </form>
        </div>
    );
}

export function InputNotes() {
    const [subjects, setSubjects] = useState([]);
    const [modules, setModules] = useState([]);
    const [selectedSubject, setSelectedSubject] = useState('');
    const [selectedModule, setSelectedModule] = useState('');
    const [level, setLevel] = useState('basic');
    const [ytLink, setYtLink] = useState('');
    const [pdfFile, setPdfFile] = useState(null);
    const [uploading, setUploading] = useState(false);

    useEffect(() => {
        axios.get(`${API}/api/admin/subjects`).then(res => {
            setSubjects(res.data);
            if (res.data.length > 0) {
                setSelectedSubject(res.data[0].id);
                fetchModules(res.data[0].id);
            }
        });
    }, []);

    const fetchModules = (subjId) => {
        axios.get(`${API}/api/student/subjects/${subjId}/modules`).then(res => {
            setModules(res.data);
            if (res.data.length > 0) setSelectedModule(res.data[0].id);
            else setSelectedModule('');
        });
    };

    const handleSubjectChange = (e) => {
        const val = e.target.value;
        setSelectedSubject(val);
        fetchModules(val);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!selectedModule) return alert('Please select a module first');

        setUploading(true);
        const formData = new FormData();
        formData.append('module_id', selectedModule);
        formData.append('level', level);
        formData.append('yt_link', ytLink);
        if (pdfFile) {
            formData.append('pdf_file', pdfFile);
        }

        try {
            await axios.post(`${API}/api/admin/notes`, formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            setYtLink('');
            setPdfFile(null);
            alert(`${level.charAt(0).toUpperCase() + level.slice(1)} Notes updated successfully!`);
        } catch (err) {
            console.error(err);
            alert('Failed to upload notes');
        }
        setUploading(false);
    };

    return (
        <div>
            <h3 style={{ marginBottom: '1.5rem' }}>Upload Reference Notes &amp; Media</h3>
            <form onSubmit={handleSubmit} style={{ maxWidth: '600px', display: 'flex', flexDirection: 'column', gap: '1rem', padding: '1.5rem', backgroundColor: '#fdfdfd', borderRadius: '12px', border: '1px solid #eaeaea' }}>
                <div style={{ display: 'flex', gap: '1rem' }}>
                    <div style={{ flex: 1 }}>
                        <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Subject</label>
                        <select className="input-field" value={selectedSubject} onChange={handleSubjectChange} required>
                            {subjects.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
                        </select>
                    </div>
                    <div style={{ flex: 1 }}>
                        <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Module</label>
                        <select className="input-field" value={selectedModule} onChange={e => setSelectedModule(e.target.value)} required>
                            {modules.map(m => <option key={m.id} value={m.id}>{m.name}</option>)}
                            {modules.length === 0 && <option value="">No modules found</option>}
                        </select>
                    </div>
                </div>

                <hr style={{ margin: '1rem 0', borderTop: '1px solid #ddd' }} />

                <div>
                    <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Target Level</label>
                    <select className="input-field" value={level} onChange={e => setLevel(e.target.value)} required>
                        <option value="basic">Basic Level Students</option>
                        <option value="intermediate">Intermediate Level Students</option>
                        <option value="advanced">Advanced Level Students</option>
                    </select>
                </div>

                <div>
                    <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>PDF Notes Upload (Optional)</label>
                    <input type="file" className="input-field" accept=".pdf" onChange={e => setPdfFile(e.target.files[0])} style={{ padding: '0.5rem' }} />
                </div>

                <div>
                    <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>YouTube Video Link (Optional)</label>
                    <input className="input-field" value={ytLink} onChange={e => setYtLink(e.target.value)} placeholder="https://youtube.com/watch?v=..." />
                </div>

                <button type="submit" className="btn" style={{ alignSelf: 'flex-start', marginTop: '1rem' }} disabled={uploading}>
                    {uploading ? 'Uploading...' : 'Save Notes Content'}
                </button>
            </form>
        </div>
    );
}

export function PerformanceView() {
    return (
        <div style={{ padding: '2rem', textAlign: 'center', backgroundColor: '#f9f9f9', borderRadius: '12px', border: '1px dashed #ccc' }}>
            <h3 style={{ marginBottom: '1rem', color: 'var(--text-dark)' }}>Student Performance Tracker</h3>
            <p style={{ color: 'var(--text-light)', fontSize: '1.1rem' }}>Reporting Interface Available in Next Version.</p>
            <p style={{ marginTop: '0.5rem', color: '#888' }}>Currently all scores are handled dynamically on the Student portal to generate Timetables.</p>
        </div>
    );
}
