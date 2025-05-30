import firebase_admin
from odoo import http
from odoo.http import request
from firebase_admin import credentials, auth
import json
import logging

SECRET_TOKEN = "?"
firebase_app = None
_logger = logging.getLogger(__name__)

class WebhookCreateContact(http.Controller):

    @http.route('/webhook/create_contact', type='http', auth='public', methods=['POST'], csrf=False)
    def create_contact(self, **kwargs):
        auth_header = request.httprequest.headers.get('Authorization')
        if auth_header != f"Bearer {SECRET_TOKEN}":
            return request.make_response(
                json.dumps({"error": "Unauthorized"}),
                headers=[('Content-Type', 'application/json')],
                status=401
            )
        #else:
            #procesar token

        data = request.jsonrequest
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')

        if not all([first_name, last_name, email]):
            return request.make_response(
                json.dumps({"error": "Missing parameters"}),
                headers=[('Content-Type', 'application/json')],
                status=400
            )

        full_name = f"{first_name} {last_name}"
        request.env['res.partner'].sudo().create({
            'name': full_name,
            'email': email,
        })
    def validar_token_jwt(token_string):
        global firebase_app

        if not firebase_app:
            try:
                cred = credentials.Certificate('/ruta/completa/a/credenciales-firebase.json')
                firebase_app = firebase_admin.initialize_app(cred)
            except Exception as e:
                _logger.error(f"Error al inicializar Firebase Admin: {e}")
                return False

        try:
            # Remover el prefijo 'Bearer ' si existe
            if token_string.startswith('Bearer '):
                token_string = token_string[7:]

            decoded_token = auth.verify_id_token(token_string)
            _logger.info(f"Token verificado: {decoded_token}")
            return True
        except Exception as e:
            _logger.warning(f"Error al verificar el token JWT: {e}")
            return False