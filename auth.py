import requests
import os

def authenticate_user(username, password):
    # URL de la API JSON-RPC de Odoo
    odoo_url = os.getenv("ODOO_URL") + "/jsonrpc"
    
    # Parámetros de la solicitud
    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "service": "common",          # Especificar el servicio 'common'
            "method": "login",            # Método para autenticar
            "args": [
                os.getenv("ODOO_DB"),     # Nombre de la base de datos de Odoo
                username,                 # Usuario de Odoo (correo electrónico)
                password                  # Contraseña del usuario
            ]
        },
        "id": 1
    }

    headers = {
        "Content-Type": "application/json"
    }

    print(f"datos de url: {odoo_url}")

    try:
        response = requests.post(odoo_url, json=payload, headers=headers)
        response_json = response.json()

        # Verificar si hay un resultado (UID del usuario)
        result = response_json.get("result")
        if isinstance(result, int):
            # Retornar el UID del usuario
            return result
        else:
            return None
    except Exception as e:
        print(f"Error al autenticar con Odoo: {e}")
        return None
