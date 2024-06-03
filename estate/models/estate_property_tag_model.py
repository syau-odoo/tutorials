from odoo import models,fields

class TagModel(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Tags"
    _order="name"
    _sql_constraints = [('property_tag_unique', 'unique(name)', "Property tag must be unique! Please choose another one.")]
    name =fields.Char("Name", required=True)
    color = fields.Integer()