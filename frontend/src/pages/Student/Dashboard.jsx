import React from 'react';
import { Routes, Route, useNavigate, useLocation } from 'react-router-dom';
import { AuthContext } from '../../context/AuthContext';
import SubjectsView from './SubjectsView';
import TimetableView from './TimetableView';
import AssessmentView from './AssessmentView';
import LiveChat from './LiveChat';

export default function StudentDashboard() {
    const { user, logout } = React.useContext(AuthContext);
    const navigate = useNavigate();
    const location = useLocation();

    const getNavClass = (path) => {
        // Exact or starts with helps keep it active during assessment
        if (path === '/student' && location.pathname === '/student') return "nav-item active";
        if (path !== '/student' && location.pathname.startsWith(path)) return "nav-item active";
        return "nav-item";
    };

    return (
        <div className="app-container">
            {/* Sidebar matching the gorgeous Red UI given by user */}
            <div className="sidebar">
                <h2>Student Portal</h2>
                <nav className="nav-links">
                    <div className={getNavClass('/student')} onClick={() => navigate('/student')}>
                        👤 Profile & Dashboard
                    </div>
                    <div className={getNavClass('/student/timetable')} onClick={() => navigate('/student/timetable')}>
                        📅 Time Table
                    </div>
                    <div className={getNavClass('/student/assessment')} onClick={() => navigate('/student/assessment')}>
                        🧠 Knowledge Assessment
                    </div>
                    <div className={getNavClass('/student/chat')} onClick={() => navigate('/student/chat')}>
                        💬 Live Chat Box
                    </div>
                    <div className="nav-item" onClick={() => { logout(); navigate('/login'); }} style={{ marginTop: 'auto', backgroundColor: 'rgba(0,0,0,0.2)' }}>
                        🚪 Log Out
                    </div>
                </nav>
            </div>

            {/* Main Content Area */}
            <div className="main-content">
                <Routes>
                    <Route path="/" element={
                        <div style={{ animation: 'fadeIn 0.3s' }}>
                            <div className="profile-header">
                                <div className="avatar">
                                    {user?.name?.charAt(0).toUpperCase() || 'S'}
                                </div>
                                <div className="profile-details">
                                    <p><strong>Name:</strong> {user?.name}</p>
                                    <p><strong>Email:</strong> {user?.email}</p>
                                    <p><strong>College:</strong> College Of Engineering Chengannur</p>
                                    <p><strong>Role:</strong> Student Status</p>
                                </div>
                            </div>
                            <SubjectsView />
                        </div>
                    } />
                    <Route path="/timetable" element={<TimetableView />} />
                    <Route path="/assessment" element={<SubjectsView />} />
                    <Route path="/assessment/take/:subjectId" element={<AssessmentView />} />
                    <Route path="/assessment/take/:subjectId/:moduleId" element={<AssessmentView />} />
                    <Route path="/chat" element={<LiveChat />} />
                </Routes>
            </div>
        </div>
    );
}
