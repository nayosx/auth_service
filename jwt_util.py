import jwt
import os
from datetime import datetime, timedelta

# Generar un token JWT
def generate_jwt(user_id, username):
    secret = os.getenv("JWT_SECRET")
    payload = {
        "user_id": user_id,
        "username": username,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token

# Verificar un token JWT
def verify_jwt(token):
    secret = os.getenv("JWT_SECRET")
    try:
        decoded = jwt.decode(token, secret, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        print("El token ha expirado")
        return None
    except jwt.InvalidTokenError:
        print("Token inválido")
        return None
