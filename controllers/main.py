from odoo import http
from odoo.http import request
import json

class WebhookCreateContact(http.Controller):

    @http.route('/webhook/create_contact', type='json', auth='public', methods=['POST'], csrf=False)
    def create_contact(self, **post):
        first_name = post.get('first_name')
        last_name = post.get('last_name')
        email = post.get('email')

        if not all([first_name, last_name, email]):
            return {"error": "Missing parameters"}

        # Combinar nombre y apellido
        full_name = f"{first_name} {last_name}"

        # Crear contacto
        request.env['res.partner'].sudo().create({
            'name': full_name,
            'email': email,
        })

        return {'status': 'success', 'message': f'Contact {full_name} created'}