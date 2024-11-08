from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime
import threading
from typing import Dict

from config import Config
from validators import validate_student_data
from models import Student
from cache import cache_summary
from utils import call_ollama_api, generate_student_prompt

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

@app.route('/health', methods=['GET'])
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }, 200

@app.route('/ollama/status', methods=['GET'])
def check_ollama_status():
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
    
    return {
        "status": "unavailable",
        "help": "Make sure Ollama is running and the model is installed"
    }, 503

@app.route('/students', methods=['POST'])
def add_student():
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
def get_all_students():
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
def get_student(id: int):
    student = students.get(id)
    if not student:
        return {"error": "Student not found"}, 404
    return student.to_dict(), 200

@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id: int):
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
def delete_student(id: int):
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
def get_student_summary(id: int):
    student = students.get(id)
    if not student:
        return {"error": "Student not found"}, 404

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

if __name__ == "__main__":
    logger.info(f"Starting Student API server on port {Config.PORT}...")
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=Config.PORT)