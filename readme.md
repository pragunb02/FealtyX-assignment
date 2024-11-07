# Student Management API

## Overview

This API is designed to manage student data, including creating, reading, updating, and deleting student records. Additionally, the API integrates with the Ollama service to generate summaries of student details.

## Features

- **Create a new student**
- **Retrieve student details**
- **Update student information**
- **Delete a student**
- **Generate a student summary** using the Ollama API
- **Health check to ensure the server is running**
- **List all students with pagination**

## Setup Instructions

### Requirements

Before starting the application, make sure you have the following installed:

- Python 3.x
- Flask
- Ollama API (for student summaries)

### Installation

1. Clone this repository:
```bash
git clone https://github.com/pragunb02/FealtyX-assignment
cd student-api
```

2. Install the required Python dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure the Ollama API is set up and running:
```bash
ps aux | grep ollama # Check if Ollama is running
ollama list # Verify if the llama3 model is installed
ollama pull llama3 # Pull the llama3 model if not already installed
ollama serve
```

4. Run the Flask application:
```bash
python3 app.py
```

The app will start at http://localhost:5001.

## API Documentation

### Available Endpoints

#### 1) Health Check
**Endpoint:** `GET /health`

Description: Check if the API is up and running.

Example Request:
```bash
curl http://localhost:5001/health
```

[Insert screenshot of health check endpoint response]

#### 2) Create a Student
**Endpoint:** `POST /students`

Description: Add a new student.

Request Body (JSON):
```json
{
    "name": "John Doe",
    "age": 20,
    "email": "johndoe@example.com"
}
```

Example Request:
```bash
curl -X POST http://localhost:5001/students \
-H "Content-Type: application/json" \
-d '{"name": "John Doe", "age": 20, "email": "johndoe@example.com"}'
```

[Insert screenshot of create student endpoint response]

#### 3) Get All Students
**Endpoint:** `GET /students`

Description: Retrieve all students. Supports pagination with query parameters.

Example Request:
```bash
curl http://localhost:5001/students
```

With pagination:
```bash
curl 'http://localhost:5001/students?page=1&per_page=5'
```

[Insert screenshot of get all students endpoint response]

#### 4) Get a Single Student by ID
**Endpoint:** `GET /students/{id}`

Description: Retrieve the student details by ID.

Example Request:
```bash
curl http://localhost:5001/students/1
```

[Insert screenshot of get single student endpoint response]

#### 5) Update a Student
**Endpoint:** `PUT /students/{id}`

Description: Update an existing student by ID.

Request Body (JSON):
```json
{
    "name": "Jane Doe",
    "age": 21,
    "email": "janedoe@example.com"
}
```

Example Request:
```bash
curl -X PUT http://localhost:5001/students/1 \
-H "Content-Type: application/json" \
-d '{"name": "Jane Doe", "age": 21, "email": "janedoe@example.com"}'
```

[Insert screenshot of update student endpoint response]

#### 6) Delete a Student
**Endpoint:** `DELETE /students/{id}`

Description: Delete the student by ID.

Example Request:
```bash
curl -X DELETE http://localhost:5001/students/1
```

[Insert screenshot of delete student endpoint response]

#### 7) Generate a Student Summary
**Endpoint:** `GET /students/{id}/summary`

Description: Generate or retrieve a cached summary of the student's details.

Example Request:
```bash
curl http://localhost:5001/students/1/summary
```

[Insert screenshot of student summary endpoint response]

#### 8) Ollama API Status
**Endpoint:** `GET /ollama/status`

Description: Check the status of the Ollama API and list available models.

Example Request:
```bash
curl http://localhost:5001/ollama/status
```

[Insert screenshot of Ollama status endpoint response]

## API Response Examples

Here are some example responses from the API endpoints:

[Insert screenshots of example responses from various endpoints showing successful and error cases]

## Troubleshooting

### Ollama API Errors
If you encounter errors when trying to generate a student summary, ensure Ollama is running and the llama3 model is available. You can check this using the following commands:

```bash
ps aux | grep ollama
ollama list
ollama pull llama3
```

### Common Issues and Solutions

1. **Server Connection Issues**
   - Verify the server is running on the correct port
   - Check if there are any conflicting applications using port 5001

2. **Ollama Integration Issues**
   - Confirm Ollama service is running
   - Check if the required models are properly installed

## Future Enhancements

1. **PDF Generation for Student Summary**
   - Allow users to download a PDF containing the student summary
   - Include formatting options for the PDF output

2. **Search Functionality**
   - Add the ability to search students by:
     - Name
     - Email
     - Age range
     - Custom criteria

3. **Authentication**
   - Implement user authentication
   - Role-based access control
   - API key management

4. **Logging and Monitoring**
   - Integrate comprehensive logging
   - Add usage analytics
   - Implement performance monitoring
   - Set up alert systems

5. **Data Export/Import**
   - Add bulk import functionality
   - Enable data export in various formats
   - Implement backup solutions

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## Contact

Project Link: [https://github.com/pragunb02/FealtyX-assignment](https://github.com/pragunb02/FealtyX-assignment)

## Acknowledgments

* Thanks to the Flask community for the excellent web framework
* Ollama team for providing the AI capabilities