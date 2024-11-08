# regular expression module
import re
from typing import List, Dict, Union

def validate_email(email: str) -> bool:
    # regular expression pattern
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def validate_age(age: int) -> bool:
    # age is of type int
    return isinstance(age, int) and 5 <= age <= 120

def validate_name(name: str) -> bool:
    return isinstance(name, str) and 2 <= len(name.strip()) <= 100

def validate_student_data(data: Dict) -> List[str]:
    errors = []
    # name is missing or name is invalid
    if not data.get('name') or not validate_name(data.get('name', '')):
        errors.append("Name must be between 2 and 100 characters")
    
    if not data.get('age') or not validate_age(data.get('age', 0)):
        errors.append("Age must be between 5 and 120")
    
    if not data.get('email') or not validate_email(data.get('email', '')):
        errors.append("Invalid email format")
    
    return errors