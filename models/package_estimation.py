from odoo import models, fields, api


class PackageEstimation(models.Model):
    _name = "package.estimation"
    _description = "package estimation"

    service = fields.Char(string='Service')
    quantity = fields.Integer(string='Quantity')
    amount = fields.Float(string='Amount')
    sub_total = fields.Float(string='Sub Total', compute="_compute_sub_total")
    booking_id = fields.Many2one("booking.travels")

    @api.depends('amount', 'quantity')
    def _compute_sub_total(self):
        for record in self:
            record.sub_total = record.amount * record.quantity
