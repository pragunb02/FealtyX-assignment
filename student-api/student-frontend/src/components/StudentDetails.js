import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import './StudentDetails.css';

const StudentDetails = () => {
  const { id } = useParams();
  const [student, setStudent] = useState(null);

  useEffect(() => {
    const fetchStudentDetails = async () => {
      try {
        const response = await axios.get(`/students/${id}`);
        setStudent(response.data);
      } catch (error) {
        console.error('Error fetching student details:', error);
      }
    };
    fetchStudentDetails();
  }, [id]);

  if (!student) {
    return <div>Loading...</div>;
  }

  return (
    <div className="student-details-container">
      <h1>{student.name}</h1>
      <p>Age: {student.age}</p>
      <p>Email: {student.email}</p>
      <p>Created: <span className="label">{student.created_at}</span></p>
      <p>Updated: <span className="label">{student.updated_at}</span></p>
    </div>
  );
};

export default StudentDetails;