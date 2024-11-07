from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime
from functools import wraps
from ratelimit import limits, sleep_and_retry
import threading
from typing import Dict, List, Any, Tuple, Optional

from config import Config
from validators import validate_student_data
from models import Student
from cache import cache_summary
from utils import call_ollama_api, generate_student_prompt, OllamaError

import requests


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Global variables
students: Dict[int, Student] = {}
id_counter = 1
lock = threading.Lock()

# Rate limiting decorator
@sleep_and_retry
@limits(calls=Config.RATE_LIMIT_CALLS, period=Config.RATE_LIMIT_PERIOD)
def rate_limited_api():
    pass

def rate_limit(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        rate_limited_api()
        return f(*args, **kwargs)
    return decorated_function

@app.route('/health', methods=['GET'])
def health_check() -> Tuple[Dict[str, str], int]:
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }, 200

@app.route('/ollama/status', methods=['GET'])
def check_ollama_status() -> Tuple[Dict[str, Any], int]:
    try:
        response = requests.get(
            "http://localhost:11434/api/tags",
            timeout=5
        )
        if response.status_code == 200:
            return {
                "status": "available",
                "models": response.json(),
                "api_url": Config.OLLAMA_API_URL
            }, 200
    except Exception as e:
        return {
            "status": "unavailable",
            "error": str(e),
            "help": "Make sure Ollama is running and the model is installed"
        }, 503

@app.route('/students', methods=['POST'])
@rate_limit
def add_student() -> Tuple[Dict[str, Any], int]:
    data = request.get_json()
    logger.info(f"Received request to create student: {data}")

    validation_errors = validate_student_data(data)
    if validation_errors:
        return {"errors": validation_errors}, 400

    with lock:
        global id_counter
        student = Student(id_counter, data["name"], data["age"], data["email"])
        students[id_counter] = student
        id_counter += 1

    logger.info(f"Created student with ID: {student.id}")
    return student.to_dict(), 201

@app.route('/students', methods=['GET'])
@rate_limit
def get_all_students() -> Tuple[Dict[str, Any], int]:
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    student_list = [s.to_dict() for s in students.values()]
    start = (page - 1) * per_page
    end = start + per_page
    
    return {
        "students": student_list[start:end],
        "total": len(student_list),
        "page": page,
        "per_page": per_page,
        "total_pages": (len(student_list) + per_page - 1) // per_page
    }, 200

@app.route('/students/<int:id>', methods=['GET'])
@rate_limit
def get_student(id: int) -> Tuple[Dict[str, Any], int]:
    student = students.get(id)
    if not student:
        return {"error": "Student not found"}, 404
    return student.to_dict(), 200

@app.route('/students/<int:id>', methods=['PUT'])
@rate_limit
def update_student(id: int) -> Tuple[Dict[str, Any], int]:
    data = request.get_json()
    student = students.get(id)
    
    if not student:
        return {"error": "Student not found"}, 404

    validation_errors = validate_student_data(data)
    if validation_errors:
        return {"errors": validation_errors}, 400

    with lock:
        student.update(data)

    logger.info(f"Updated student with ID: {id}")
    return student.to_dict(), 200

@app.route('/students/<int:id>', methods=['DELETE'])
@rate_limit
def delete_student(id: int) -> Tuple[Dict[str, Any], int]:
    student = students.get(id)
    if not student:
        return {"error": "Student not found"}, 404

    with lock:
        del students[id]
    
    logger.info(f"Deleted student with ID: {id}")
    return {
        "message": "Student deleted successfully",
        "deleted_at": datetime.now().isoformat()
    }, 200

@app.route('/students/<int:id>/summary', methods=['GET'])
@rate_limit
def get_student_summary(id: int) -> Tuple[Dict[str, Any], int]:
    student = students.get(id)
    if not student:
        return {"error": "Student not found"}, 404

    try:
        # Check cache first
        prompt = generate_student_prompt(student.to_dict())
        cached_summary = cache_summary(student.id, prompt)
        
        if cached_summary:
            return {
                "student_id": id,
                "summary": cached_summary,
                "source": "cache",
                "generated_at": datetime.now().isoformat()
            }, 200

        # Generate new summary
        summary = call_ollama_api(prompt)
        cache_summary(student.id, prompt, summary)

        return {
            "student_id": id,
            "summary": summary,
            "source": "ollama",
            "model": Config.OLLAMA_MODEL,
            "generated_at": datetime.now().isoformat()
        }, 200

    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        return {
            "error": "Failed to generate summary",
            "details": str(e),
            "suggestions": [
                "Check if Ollama is running: 'ps aux | grep ollama'",
                f"Verify model '{Config.OLLAMA_MODEL}' is installed: 'ollama list'",
                "Try pulling the model: 'ollama pull llama2'",
                "Check Ollama logs for errors"
            ]
        }, 500

if __name__ == "__main__":
    logger.info(f"Starting Student API server on port {Config.PORT}...")
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=Config.PORT)