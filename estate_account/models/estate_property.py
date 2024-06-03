from odoo import models,Command
from odoo.exceptions import AccessError,ValidationError

class InheritedEstateProperty(models.Model):
    _inherit = "estate.property"

    def sold_button(self):
        try:
            self.check_access_rights('write')
            self.check_access_rule('write')
        except AccessError:
            return ValidationError("You dont have the right access for this operation")
        partner_id = self.buyer.id
        move_type = 'out_invoice'

        journal_id = self.env['account.journal'].search([('type', '=', 'sale')], limit=1).id
        line = [
            Command.create({
                "name":"6% of Selling Price",
                "quantity":1,
                "price_unit":(self.selling_price)*0.06
            }),
            Command.create({
                "name":"Administration fee",
                "quantity":1,
                "price_unit":100.00
            })
        ]
        payload_move = {
            'partner_id':partner_id,
            'move_type':move_type,
            'journal_id':journal_id,
            'invoice_line_ids':line
        }
        self.env['account.move'].sudo().create(payload_move)

        
        
        res = super(InheritedEstateProperty,self).sold_button()
        return res
    