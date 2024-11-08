from datetime import datetime
from typing import Dict, Optional
# Optional allows you to specify if a value can be None
# this(self) pointer refers to the object of the class that called the method. 

class Student:
    #constructor
    def __init__(self, id: int, name: str, age: int, email: str):
        self.id = id
        self.name = name
        self.age = age
        self.email = email
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "email": self.email,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def update(self, data: Dict) -> None:
        if 'name' in data:
            self.name = data['name']
        if 'age' in data:
            self.age = data['age']
        if 'email' in data:
            self.email = data['email']
        self.updated_at = datetime.now().isoformat()