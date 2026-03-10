import React from 'react';
import { Routes, Route, useNavigate, useLocation } from 'react-router-dom';
import { AuthContext } from '../../context/AuthContext';
import { ManageSubjects, ManageModules, AddQuestions, InputNotes, PerformanceView } from './AdminViews';

export default function AdminDashboard() {
    const { user, logout } = React.useContext(AuthContext);
    const navigate = useNavigate();
    const location = useLocation();

    const getNavClass = (path) => {
        return location.pathname === path ? "nav-item active" : "nav-item";
    };

    return (
        <div className="app-container">
            <div className="sidebar" style={{ backgroundColor: '#1a1f36' }}>
                <h2 style={{ color: '#fff' }}>Admin Portal</h2>
                <nav className="nav-links">
                    <div className={getNavClass('/admin')} onClick={() => navigate('/admin')}>
                        📚 Manage Subjects
                    </div>
                    <div className={getNavClass('/admin/modules')} onClick={() => navigate('/admin/modules')}>
                        📑 Manage Modules
                    </div>
                    <div className={getNavClass('/admin/questions')} onClick={() => navigate('/admin/questions')}>
                        ✍️ Add Questions
                    </div>
                    <div className={getNavClass('/admin/notes')} onClick={() => navigate('/admin/notes')}>
                        📝 Input Notes (PDF/YT)
                    </div>
                    <div className={getNavClass('/admin/performance')} onClick={() => navigate('/admin/performance')}>
                        📈 Student Performance
                    </div>
                    <div className="nav-item" onClick={() => { logout(); navigate('/login'); }} style={{ marginTop: 'auto', backgroundColor: 'rgba(255,255,255,0.1)' }}>
                        🚪 Log Out
                    </div>
                </nav>
            </div>

            <div className="main-content">
                <div style={{ marginBottom: '2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', backgroundColor: '#f4f5f7', padding: '1rem 2rem', borderRadius: '12px' }}>
                    <div>
                        <h3 style={{ color: 'var(--text-dark)' }}>Administrator controls</h3>
                        <p style={{ fontSize: '0.85rem', color: 'var(--text-light)' }}>Logged in as {user?.email}</p>
                    </div>
                    <div className="avatar" style={{ width: '45px', height: '45px', fontSize: '1.2rem', backgroundColor: '#1a1f36' }}>
                        {user?.name?.charAt(0).toUpperCase() || 'A'}
                    </div>
                </div>

                <div style={{ animation: 'fadeIn 0.3s' }}>
                    <Routes>
                        <Route path="/" element={<ManageSubjects />} />
                        <Route path="/modules" element={<ManageModules />} />
                        <Route path="/questions" element={<AddQuestions />} />
                        <Route path="/notes" element={<InputNotes />} />
                        <Route path="/performance" element={<PerformanceView />} />
                    </Routes>
                </div>
            </div>
        </div>
    );
}
