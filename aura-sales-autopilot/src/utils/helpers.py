import re
import os
from dotenv import load_dotenv
from typing import Dict, Any
import json

load_dotenv()

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    # Basic US/Intl phone validation
    pattern = r'^\+?1?[-\.\s]?\(?([0-9]{3})\)?[-\.\s]?([0-9]{3})[-\.\s]?([0-9]{4})$'
    return re.match(pattern, phone) is not None

def load_json(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as f:
        return json.load(f)

def get_env(var: str, default: str = "") -> str:
    return os.getenv(var, default)
