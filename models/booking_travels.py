from odoo import models, fields, api, _
import datetime


class BookingTravels(models.Model):
    _name = "booking.travels"
    _description = "Booking Travels"
    _rec_name = "booking_reference"

    booking_reference = fields.Char(string='Reference', readonly=True,
                                    default=_('New'))
    customer_id = fields.Many2one('res.partner',
                                  string='Customer')
    no_of_passengers = fields.Integer(default=1,
                                      string='No Of Passengers')
    booking_date = fields.Date(default=fields.Date.today(),
                               string='Booking Date')
    source_location_id = fields.Many2one('location.travels',
                                         string='Source Location')
    destination_location_id = fields.Many2one('location.travels',
                                              string='Destination Location')
    travel_Date = fields.Date()
    service_id = fields.Many2one("service.travels", string='Service')
    package_re = fields.Boolean(related='service_id.package')
    state = fields.Selection(string='State',
                             selection=[('draft', 'Draft'),
                                        ('confirmed', 'Confirmed'),
                                        ('done', 'Done'),
                                        ('expired', 'Expired')],
                             default='draft')
    expiration_date = fields.Date(compute="_compute_total")
    booking_line_ids = fields.One2many("package.estimation", 'booking_id')
    package_id = fields.Many2one("package.travels", string='Package')
    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.company,
                                 string='Company')
    currency_id = fields.Many2one('res.currency',
                                  default=lambda self: self.env.
                                  company.currency_id,
                                  string='Currency')
    total_amount = fields.Monetary(compute="_compute_total_amount",
                                   string='Total')
    charges = fields.Monetary(string='Charges')

    @api.onchange('package_id')
    def onchange_vehicle_id_field(self):
        self.write({'booking_line_ids': [(5, 0)]})
        self.write({'booking_line_ids': [(0, 0, {
                'service': rec.service,
                'quantity': rec.quantity,

                'amount': rec.amount,
                'booking_id': self.id
            }) for rec in self.package_id.estimation_vehicle_id]})

    @api.depends('booking_line_ids')
    def _compute_total_amount(self):
        for i in self:
            i.total_amount = sum(i.booking_line_ids.mapped('sub_total'))

    def button_in_confirmed(self):
        self.write({
            'state': 'confirmed'
        })

    def button_in_done(self):
        self.write({
            'state': 'done'
        })

    def button_in_invoice(self):
        if self.package_re:
            vals = []
            for rec in self.booking_line_ids:
                value = {
                    'name': rec.service,
                    'quantity': rec.quantity,
                    'price_unit': rec.amount,
                }
                vals.append((0, 0, value))
            invoice = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': self.customer_id.id,
                'invoice_line_ids': vals
            })
        else:
            vals = []
            values = {
                'name': f"{self.booking_reference} ({self.service_id.name})",
                'price_unit': self.charges,
            }
            vals.append((0, 0, values))
            invoice = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': self.customer_id.id,
                'invoice_line_ids': vals
            })

        return {
            'name': 'invoice',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.move',
            'view_id': self.env.ref('account.view_move_form').id,
            'type': 'ir.actions.act_window',
            'res_id': invoice.id,
            'target': 'current'
        }

    @api.model
    def create(self, vals):
        vals['booking_reference'] = self.env['ir.sequence'].next_by_code(
            'booking.travels.sequence') or _('New')
        return super(BookingTravels, self).create(vals)

    @api.onchange('source_location_id')
    def onchange_source_location(self):
        return {'domain': {'destination_location_id': [
            ('id', '!=', self.source_location_id.id)]}}

    @api.depends("expiration_date")
    def _compute_total(self):
        for record in self:
            record.expiration_date = record.booking_date + datetime.timedelta(
                days=record.service_id.expiration_period)

    def process_scheduler_queue(self):
        for rec in self.search([('state', '=', 'draft')]):
            if rec.expiration_date == fields.Date.today():
                rec.write({'state': 'expired'})
