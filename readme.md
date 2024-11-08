# Student Management API

## Overview

This API is designed to manage student data, including creating, reading, updating, and deleting student records. Additionally, the API integrates with the Ollama service to generate summaries of student details.

## Features
* **Create a new student** (POST /students)
* **Retrieve student details** (GET /students/{id})
* **Update student information** (PUT /students/{id})
* **Delete a student** (DELETE /students/{id})
* **List all students with pagination** (GET /students)
* **Generate AI summaries** using Ollama (GET /students/{id}/summary)
* **Health check** for server status (GET /health)
* **Ollama status check** (GET /ollama/status)
* **Cache system** for AI summaries
* **Thread-safe** operations
* **Input validation** with error handling
* **CORS** enabled
* **Comprehensive logging**

## Setup Instructions

### Requirements

Before starting the application, make sure you have the following installed:

- Python 3.x
- Flask
- Ollama API (for student summaries)

### Installation
```bash
# Clone repository
git clone https://github.com/pragunb02/FealtyX-assignment
cd student-api

# Install dependencies
pip install -r requirements.txt

# Setup Ollama
ps aux | grep ollama  # Check if running
ollama list          # Check models
ollama pull llama3   # Install model
ollama serve         #run model

# Run application
3 app.py
```

The app runs at http://localhost:5001

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

## Data Validation

The API validates student data using the `validate_student_data()` function, which checks:
- Required fields presence (name, age, email)
- Data type correctness
- Field value validity

### Ollama Integration Details

The API integrates with Ollama for generating student summaries using the following approach:

1. **Prompt Engineering**
   The API uses a carefully crafted prompt template for generating summaries:
   ```python
   prompt = f"""

    Create a detailed student profile analysis and mentorship summary:
    
    Student Details:
    - Name: {student['name']}
    - Age: {student['age']}
    - Email: {student['email']}
    
   Please provide the following:
    1. A brief, impactful assessment of their academic potential (1 sentence)
    2. The key area(s) for improvement or growth based on their age group and academic progress (1 sentence)
    3. Specific and actionable recommendations for their educational journey (1 sentence)
    4. A motivational statement or words of encouragement for the student (1 sentence)
    
    Format the response with only 4 distinct points, each concise and structured and no special chacaters and directly give 4 points
    """
   ```

2. **Summary Generation**
   ```python
   response = ollama.generate(
       model="llama3",
       prompt=prompt,
   )
   ```

3. **Caching**
   - Summaries are cached to improve performance
   - Cache invalidates after student data updates

Example Summary Response:
```json
{
    "id": 1,
    "summary": "John Doe is a 20-year-old student with strong academic potential...",
    "generated_at": "2024-03-08T12:00:00Z"
}
```

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


## HTTP Status Codes

The API uses standard HTTP status codes to indicate the success or failure of requests:

- `200`: Successful request
- `201`: Resource successfully created
- `400`: Bad Request (client error)
- `404`: Not Found
- `503`: Service Unavailable (for Ollama service)

## Error Scenarios and Responses

### 1. Student Not Found (404)
Occurs when attempting to access, update, or delete a non-existent student.

```json
{
    "error": "Student not found"
}
```

**Affected Endpoints:**
- `GET /students/<id>`
- `PUT /students/<id>`
- `DELETE /students/<id>`
- `GET /students/<id>/summary`

### 2. Invalid Student Data (400)
Occurs when the provided student data fails validation.

```json
{
    "errors": {
        "name": "Name is required",
        "age": "Age must be provided",
        "email": "Invalid email format"
    }
}
```

**Affected Endpoints:**
- `POST /students`
- `PUT /students/<id>`

### 3. Ollama Service Status (503)
Occurs when the Ollama service is unavailable.

```json
{
    "status": "unavailable",
    "help": "Make sure Ollama is running and the model is installed"
}
```

**Affected Endpoints:**
- `GET /ollama/status`

### 4. Student Summary Generation
The summary endpoint includes source information in successful responses:

**Cache Hit Response:**
```json
{
    "student_id": 1,
    "summary": "...",
    "source": "cache",
    "generated_at": "2024-11-08T12:00:00Z"
}
```

**New Generation Response:**
```json
{
    "student_id": 1,
    "summary": "...",
    "source": "ollama",
    "model": "llama2",
    "generated_at": "2024-11-08T12:00:00Z"
}
```

## Concurrency

- Thread-safe operations using a mutex lock (`lock`) to ensure safe concurrent access to shared resources.
- Atomic ID generation using a global counter (`id_counter`) with a mutex to prevent race conditions.
- Protected shared resources using locks during data manipulation.

## Data Storage

The application uses in-memory storage with thread-safe operations:
- Primary data structure: Dictionary (`students`) with student ID as the key.
- Mutex (`lock`) implementation for concurrent access to the shared `students` dictionary.
- Atomic operations for ID generation using a global counter (`id_counter`), ensuring safe increment within the locked section.


## Key test areas:
1. CRUD operations
2. Input validation
3. Concurrent access
4. Ollama integration
5. Error handling

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

4. **Data Export/Import**
   - Add bulk import functionality
   - Enable data export in various formats
   - Implement backup solutions