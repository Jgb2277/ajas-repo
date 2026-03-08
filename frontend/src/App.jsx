import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, AuthContext } from './context/AuthContext';

// Import Pages
import Login from './pages/Auth/Login';
import Signup from './pages/Auth/Signup';
import StudentDashboard from './pages/Student/Dashboard';
import AdminDashboard from './pages/Admin/Dashboard';

const PrivateRoute = ({ children, role }) => {
  const { user, loading } = React.useContext(AuthContext);

  if (loading) return <div>Loading...</div>;
  if (!user) return <Navigate to="/login" />;
  if (role && user.role !== role) return <Navigate to="/" />;

  return children;
};

// Simple Fallback Component while we build Out the Pages
const LoadingPlaceholder = ({ name }) => (
  <div style={{ padding: '2rem', textAlign: 'center' }}>
    <h2>{name} Loading...</h2>
  </div>
);

function AppRoutes() {
  const { user } = React.useContext(AuthContext);

  return (
    <Routes>
      <Route path="/" element={user ? <Navigate to={`/${user.role}`} /> : <Navigate to="/login" />} />
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />

      {/* Student Routes */}
      <Route path="/student/*" element={
        <PrivateRoute role="student">
          <StudentDashboard />
        </PrivateRoute>
      } />

      {/* Admin Routes */}
      <Route path="/admin/*" element={
        <PrivateRoute role="admin">
          <AdminDashboard />
        </PrivateRoute>
      } />
    </Routes>
  );
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
