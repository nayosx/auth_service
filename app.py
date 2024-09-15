import logging
from flask import Flask, request, jsonify
from auth import authenticate_user
from jwt_util import generate_jwt, verify_jwt
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde .env
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,  # Puedes cambiar el nivel según necesites
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),  # Guardar los logs en un archivo
        logging.StreamHandler()          # Imprimir los logs en la consola
    ]
)

app = Flask(__name__)

# Ruta de autenticación
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Logear intentos de autenticación
    logging.info(f"Intento de autenticación de usuario: {username}")
    
    # Autenticar el usuario contra Odoo
    user_id = authenticate_user(username, password)
    
    if user_id:
        logging.info(f"Autenticación exitosa para el usuario {username} (ID: {user_id})")
        # Generar un token JWT si la autenticación es exitosa
        token = generate_jwt(user_id, username)
        return jsonify({"token": token}), 200
    else:
        logging.warning(f"Autenticación fallida para el usuario {username}")
        return jsonify({"error": "Autenticación fallida"}), 401

# Ruta protegida de ejemplo
@app.route('/api/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization').split(" ")[1]
    user = verify_jwt(token)

    if user:
        logging.info(f"Acceso autorizado para el usuario: {user['username']}")
        return jsonify({"message": "Acceso autorizado", "user": user}), 200
    else:
        logging.error("Token inválido o expirado")
        return jsonify({"error": "Token inválido o expirado"}), 401

if __name__ == "__main__":
    app.run(debug=True)
