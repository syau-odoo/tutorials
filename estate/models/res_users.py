from odoo import fields, models

class UserInheritedModel(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "salesperson")