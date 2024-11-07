import logging
import requests
from typing import Dict, Any, Optional
import backoff
from config import Config

logger = logging.getLogger(__name__)


class OllamaError(Exception):
    """Custom exception for Ollama API errors"""
    pass

@backoff.on_exception(
    backoff.expo,
    (requests.exceptions.RequestException, OllamaError),
    max_tries=Config.MAX_RETRIES
)
def call_ollama_api(prompt: str) -> str:
    try:
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
        
        if response.status_code != 200:
            raise OllamaError(f"Ollama API error: {response.status_code}")

        result = response.json()
        if not result.get("response"):
            raise OllamaError("Empty response from Ollama")
            
        return result["response"]

    except Exception as e:
        logger.error(f"Ollama API error: {str(e)}")
        raise

def generate_student_prompt(student: Dict[str, Any]) -> str:
    return f"""

    Create a detailed student profile analysis and mentorship summary:
    
    Student Details:
    - Name: {student['name']}
    - Age: {student['age']}
    - Email: {student['email']}
    
   Please provide the following:
    1. A brief, impactful assessment of their academic potential (1-2 sentences)
    2. The key area(s) for improvement or growth based on their age group and academic progress (1-2 sentences)
    3. Specific and actionable recommendations for their educational journey (1-2 sentences)
    4. A motivational statement or words of encouragement for the student (1-2 sentences)
    
    Format the response with 4 distinct points, each concise and structured.
    """