import logging
# A library to send HTTP requests (like sending data to a web server).
import requests
from typing import Dict, Any
# import backoff: This is used to automatically retry a function if it fails (with exponential backoff), meaning it will retry after increasing delays.
# 1 sec -> 2 sec -> 4 sec -> ...
import backoff
from config import Config

logger = logging.getLogger(__name__)

# This decorator automatically retries the function if it fails for 3 times
@backoff.on_exception(
    backoff.expo,
    (requests.exceptions.RequestException),
    max_tries=Config.MAX_RETRIES
)
def call_ollama_api(prompt: str) -> str:
    # dict payload send to api
    payload = {
        "model": Config.OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "num_predict": 500,
        }
    }

    response = requests.post(
        Config.OLLAMA_API_URL,
        json=payload,
        timeout=Config.REQUEST_TIMEOUT
    )
    # sends an HTTP POST request to the Ollama API, with the payload as the body of the request. The URL of the API and the timeout are taken from the Config.
    if response.status_code != 200:
        logger.error(f"Error: Ollama API returned status code {response.status_code}")
        return "Error: Unable to get response from Ollama API"

    result = response.json()

    if "response" not in result:
        logger.error("Error: Empty response from Ollama")
        return "Error: Empty response from Ollama"

    return result["response"]

def generate_student_prompt(student: Dict[str, Any]) -> str:
    return f"""
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
    
    Format the response with only 4 distinct points, each concise and structured and and no special chacaters and directly give 4 points.
    """
