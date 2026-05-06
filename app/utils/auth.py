import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from flask import request

SECRET = "this_is_a_super_long_secret_key_for_jwt_12345"

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

# token generate
def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(days=1)
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")

def get_user_id_from_token(request):
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return None
    try:
        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return payload["user_id"]
    except:
        return None

def get_user_id_from_request():
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return None

    try:
        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return payload["user_id"]
    except:
        return None
    

    
    