import React, { useState } from 'react';
import axios from 'axios';

const StudentForm = () => {
  const [formData, setFormData] = useState({
    name: '',
    age: '',
    email: '',
  });

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setFormData((prevFormData) => ({
      ...prevFormData,
      [name]: value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    // Validate form data
    if (!formData.name || !formData.age || !formData.email) {
      console.error('Please fill in all fields');
      return;
    }

    // Convert age to a number (if it's a valid number string)
    const age = Number(formData.age);
    if (isNaN(age)) {
      console.error('Age must be a valid number');
      return;
    }

    const validatedFormData = { ...formData, age };

    try {
      // Send POST request with validated data
      await axios.post('/students', validatedFormData);
      // Reset the form after successful submission
      setFormData({ name: '', age: '', email: '' });
    } catch (error) {
      console.error('Error creating student:', error);
      if (error.response) {
        console.error('Response error:', error.response.data); // Log detailed error response
      }
    }
  };

  return (
    <div>
      <h1>Create Student</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="name">Name:</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleInputChange}
          />
        </div>
        <div>
          <label htmlFor="age">Age:</label>
          <input
            type="number"
            id="age"
            name="age"
            value={formData.age}
            onChange={handleInputChange}
          />
        </div>
        <div>
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleInputChange}
          />
        </div>
        <button type="submit">Create</button>
      </form>
    </div>
  );
};

export default StudentForm;
