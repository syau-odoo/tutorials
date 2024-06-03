from odoo import fields,models,api

class PropertyModel(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "name"
    _sql_constraints = [('property_type_unique', 'unique(name)', "Property type must be unique! Please choose another one.")]
    name = fields.Char("Name",required=True)
    property_ids = fields.One2many("estate.property","property_type_id")
    sequence = fields.Integer('Sequence', default =1)
    offer_ids = fields.One2many('estate.property.offer',"property_type_id")
    offer_count=fields.Integer("Count", compute="_compute_count")

    @api.depends('offer_ids')
    def _compute_count(self):
        for record in self:
            record.offer_count = len(self)