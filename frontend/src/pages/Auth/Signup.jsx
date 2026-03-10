import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';

export default function Signup() {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [role, setRole] = useState('student');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await axios.post('http://localhost:5000/api/auth/register', { name, email, password, role });
            navigate('/login');
        } catch (err) {
            setError(err.response?.data?.error || 'Registration failed');
        }
    };

    return (
        <div style={{ width: '100%', minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: '#f4f5f7', padding: '2rem 0' }}>
            <div className="form-container" style={{ maxWidth: '450px', width: '90%', padding: '2.5rem', background: 'white', borderTop: '5px solid var(--primary)', borderRadius: '12px', boxShadow: 'var(--shadow)' }}>
                <h2 style={{ color: 'var(--text-dark)', textAlign: 'center', marginBottom: '1.5rem', fontSize: '1.8rem' }}>Join EduPath</h2>
                {error && <p style={{ color: 'red', textAlign: 'center', marginBottom: '1rem', backgroundColor: '#ffcccc', padding: '0.5rem', borderRadius: '4px' }}>{error}</p>}
                <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
                    <div>
                        <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>Full Name</label>
                        <input type="text" className="input-field" value={name} onChange={(e) => setName(e.target.value)} required placeholder="John Doe" />
                    </div>
                    <div>
                        <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>Email Address</label>
                        <input type="email" className="input-field" value={email} onChange={(e) => setEmail(e.target.value)} required placeholder="student@example.com" />
                    </div>
                    <div>
                        <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>Password</label>
                        <input type="password" className="input-field" value={password} onChange={(e) => setPassword(e.target.value)} required placeholder="••••••••" />
                    </div>
                    <div>
                        <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>Account Type</label>
                        <select className="input-field" value={role} onChange={(e) => setRole(e.target.value)} style={{ cursor: 'pointer' }}>
                            <option value="student">Student</option>
                            <option value="admin">Administrator</option>
                        </select>
                    </div>
                    <button type="submit" className="btn" style={{ marginTop: '0.5rem' }}>Register Account</button>
                </form>
                <p style={{ textAlign: 'center', marginTop: '1.5rem', fontSize: '0.95rem' }}>
                    Already have an account? <Link to="/login" style={{ color: 'var(--primary)', textDecoration: 'none', fontWeight: '600' }}>Sign in</Link>
                </p>
            </div>
        </div>
    );
}
