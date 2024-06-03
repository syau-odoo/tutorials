from odoo import models,fields,api,_
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero

class EstateModel(models.Model):
    _name = "estate.property"
    _description ="Real Estate Apps"
    _order = "id desc"
    _sql_constraints = [
        (
            'check_expexted_price','CHECK(expected_price > 0)', 'The Expected Price must be positive'
        ),
        (
            'check_selling_price','CHECK(selling_price >= 0)', 'Selling Price should be positive number'
        ),
    ]
    name = fields.Char("Name",required=True)
    description=fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availibility = fields.Date("Availibilty Date",default=fields.Datetime.today()+relativedelta(months=+3))
    expected_price = fields.Float("Expected Price",required=True)
    selling_price = fields.Float("Selling Price",readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms",default=2)
    living_area = fields.Integer("Living Area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area")
    garden_orientation=fields.Selection(
        string='Garden Orientation',
        selection=[('north','North'),('south','South'),('east','East'),('west','West')],
        help="this will decide which direction for your garden"
    )
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        string='State',
        selection=[('new','New'),('offer received','Offer Received'),('offer accepted','Offer Accepted'),('sold','Sold'),("canceled","Canceled")],
        help="this will decide which direction for your garden",
        default="new",
        copy=False
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer = fields.Many2one("res.partner",string="Buyer",copy=False)
    salesperson = fields.Many2one("res.users",string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag",string="Tags")
    offer_ids = fields.One2many("estate.property.offer","property_id")
    total_area = fields.Integer(compute="_compute_total")
    best_price = fields.Float(compute="max_price", string="Best Offer")

   

    @api.depends("living_area","garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids')
    def max_price(self):
        for record in self:
            if len(record.offer_ids) == 0:
                record.best_price = 0
            else:
                record.best_price = max(record.offer_ids.mapped('price'))
    
    @api.onchange("garden")
    def onchange_garden_area(self):
        self.garden_area = 10
        self.garden_orientation = "north"

    def sold_button(self):
        if self.state == 'canceled':
            raise UserError("Cancelled properties cannot be sold")
        else:
            self.state = 'sold'
    
    def cancel_button(self):
        if self.state == 'sold':
            raise UserError("Sold properties cannot be cancelled")
        else:
            self.state = 'canceled'
    
    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price,precision_digits=2) != True:
                if float_compare(0.9*record.expected_price,record.selling_price,precision_digits=2) >=0:
                    raise ValidationError("Offer accepted must greater than 90%")
    
    @api.ondelete(at_uninstall=False)
    def delete_new_cancel(self):
        for record in self:
            if record.state not in ['new','canceled']:
                raise UserError("You cannot delete if the state if not new or cancelled")
            


        

