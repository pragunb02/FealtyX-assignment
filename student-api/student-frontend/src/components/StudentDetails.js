import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

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
    <div>
      <h1>{student.name}</h1>
      <p>Age: {student.age}</p>
      <p>Email: {student.email}</p>
      <p>Created: {student.created_at}</p>
      <p>Updated: {student.updated_at}</p>
    </div>
  );
};

export default StudentDetails;