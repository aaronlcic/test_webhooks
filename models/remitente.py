import string
from odoo import models, fields, api
import requests
import logging

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, vals):
        partner = super(ResPartner, self).create(vals)
        nombre = partner.name.split(' ')

        if len(nombre) < 2:
            payload = {
                'first_name': nombre[0],
                'last_name': '',
                'email': partner.email,
            }
        else:
            payload = {
                'first_name': nombre[0],
                'last_name': nombre[1],
                'email': partner.email,
            }

        webhook_url = "https://odoo-test-ws-444557042058.europe-west1.run.app"
        _logger.info("Datos a enviar en webhook: %s", payload)

        try:
            response = requests.post(webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            _logger.info("Webhook enviado con éxito: %s", response.text)
        except Exception as e:
            _logger.error("Error al enviar webhook: %s", str(e))

        return partner
