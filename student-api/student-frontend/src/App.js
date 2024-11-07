import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import StudentList from './components/StudentList';
import StudentForm from './components/StudentForm';
import StudentDetails from './components/StudentDetails';
// import StudentForm from './components/StudentForm';
// import './styless.css'; // Ensure your global styles are imported

function App() {
  return (
    <Router> {/* Wrap your app in BrowserRouter */}
      <div className="App">
        <h1>Welcome to the Student Dashboard</h1>

        {/* Navigation Links */}
        <nav>
          <ul>
            <li>
              <Link to="/">Student List</Link>
            </li>
            <li>
              <Link to="/students/">Create Student</Link>
            </li>
          </ul>
        </nav>

        {/* Define Routes */}
        <Routes>
          {/* Add your route components here */}
          <Route path="/students" element={<StudentForm />} />
          <Route path="/students/:id" element={<StudentDetails />} />
          <Route path="/" element={<StudentList />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
