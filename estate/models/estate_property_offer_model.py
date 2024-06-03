from odoo import models,fields,api
from dateutil.relativedelta import relativedelta
from datetime import date
from odoo.exceptions import ValidationError

class OfferModel(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Offering"
    _order = "price desc"

    price = fields.Float("Price")
    status = fields.Selection(
        string= 'Status',
        selection=[('accepted','Accepted'),('refused','Refused')],
        help = "this is the offer"
    )
    _sql_constraints = [
        (
            'check_price','CHECK(price > 0)', 'Price must be a positive number and more than 0'
        ),
    ]
    partner_id = fields.Many2one("res.partner",string="Partner",required=True)
    property_id = fields.Many2one("estate.property",string="Property",required=True)
    property_type_id = fields.Many2one("estate.property.type", stored=True, related="property_id.property_type_id")
    validity = fields.Integer(string="Validity",default=7)
    date_deadline = fields.Date(string="Deadline", compute="compute_deadline", inverse="inverse_deadline")

    @api.depends('validity')
    def compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Datetime.today() + relativedelta(days=record.validity)

    def inverse_deadline(self):
        for record in self:
            validity = (record.date_deadline - record.create_date.date()).days
            record.validity = validity
    
    def confirm(self):
        self.status = 'accepted'
        self.property_id.selling_price = self.price
        self.property_id.buyer = self.partner_id
        self.property_id.state = 'offer accepted'

    def cancel(self):
        self.status = 'refused'
        self.property_id.selling_price = 0
        self.property_id.buyer = {}
        self.property_id.state = 'canceled'

    @api.model
    def create(self, vals):
        property_id = self.env["estate.property"].browse(vals.get('property_id'))
        existing = self.env["estate.property.offer"].search([('property_id', '=', vals.get('property_id'))])
        for record in existing:
           if record.price > vals.get('price'):
               raise ValidationError("Offer price must higher")

        return super(OfferModel,self).create(vals)            