import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import StudentList from './components/StudentList';
import StudentForm from './components/StudentForm';
import StudentDetails from './components/StudentDetails';
import './app.css';

function App() {
  return (
    <Router>
      <div className="App">
        <h1>Welcome to the Student Dashboard</h1>

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

        <Routes>
          <Route path="/students" element={<StudentForm />} />
          <Route path="/students/:id" element={<StudentDetails />} />
          <Route path="/" element={<StudentList />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
