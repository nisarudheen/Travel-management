from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PackageTravels(models.Model):
    _name = "package.travels"
    _description = "packages of  travel management"
    _rec_name = "customer_id"

    customer_id = fields.Many2one('res.partner', string="Customer")
    quotation_Date = fields.Date(string='Quotation Date',
                                 default=fields.Date.today())
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    source_location_id = fields.Many2one('location.travels',
                                         string='Source Location')
    destination_location_id = fields.Many2one('location.travels',
                                              string='Destination Location')
    number_of_travellers = fields.Integer(string='Number Of Travellers')
    facilities_id = fields.Many2one("facilities.travels", string='Facilities')
    vehicle_id = fields.Many2one("vehicle.travels", string='Vehicle')
    estimated_km = fields.Float()
    vehicle_type = fields.Selection(string='Vehicle Type',
                                    selection=[('bus', 'Bus'),
                                               ('traveller', 'Traveller'),
                                               ('van', 'Van'),
                                               ('other', 'Other')])
    estimation_vehicle_id = fields.One2many('estimation.vehicle',
                                            'estimation_id')
    start_date = fields.Date(default=fields.Date.today())
    state = fields.Selection(string='State',
                             selection=[('draft', 'Draft'),
                                        ('confirmed', 'Confirmed')],
                             default='draft')
    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.company,
                                 string="Company")
    currency_id = fields.Many2one('res.currency',
                                  default=lambda self: self.env.company.
                                  currency_id)
    total_amount = fields.Monetary(string='Total :',
                                   compute='_compute_total_amount')
    vehicle_selection_ids = fields.One2many('vehicle.travels', 'facilities_id')

    def button_in_confirmed(self):
        value = self.env["booking.management"].create({
            'customer_id': self.customer_id.id,
            'no_of_passengers': self.number_of_travellers,
            'booking_date': self.quotation_Date,
            'source_location_id': self.source_location_id.id,
            'destination_location_id': self.destination_location_id.id,
            'travel_Date': self.start_date,
            'expiration_date': self.end_date
             })
        self.write({
            'state': 'confirmed'
             })

    #                    '''filtration of vehicle type three'''

    @api.onchange('vehicle_type', 'number_of_travellers', 'facilities_id')
    def onchange_vehicle_id(self):
        domain = []
        if self.facilities_id:
            domain.append(('facilities_id', '=', self.facilities_id.ids))
        if self.vehicle_type:
            domain.append(('vehicle_type', '=', self.vehicle_type))
        if self.number_of_travellers:
            domain.append(('number_of_seats', '=', self.number_of_travellers))
        return {
            'domain': {'vehicle_id': domain}
        }

    @api.constrains('start_date',
                    'end_date')
    def _vehicle_availability(self):
        val = self.env['package.travels'].search([('id', '!=', self.id)])
        if not self.end_date:
            raise ValidationError('Please provide end date')
        for rec in val:
            if self.vehicle_id == rec.vehicle_id and self.start_date <= rec.\
                    end_date and self.end_date >= rec.start_date:
                raise ValidationError('This vehicle is already booked')

    @api.onchange('source_location_id')
    def onchange_source_location_field(self):
        return {'domain': {'destination_location_id': [('id',
                                                        '!=', self.
                                                        source_location_id.id)
                                                       ]}}

    @api.onchange('vehicle_id')
    def onchange_vehicle_id_field(self):
        self.write({'estimation_vehicle_id': [(5, 0)]})
        for rec in self.vehicle_id.order_line_travel_ids:
            vals = {
                'service': rec.service,
                'quantity': rec.quantity,

                'amount': rec.amount,
                'estimation_id': self.id
            }
            self.write({'estimation_vehicle_id': [(0, 0, vals)]})

    @api.depends('estimation_vehicle_id')
    def _compute_total_amount(self):
        for i in self:
            i.total_amount = sum(i.estimation_vehicle_id.mapped('sub_total'))


class EstimationVehicle(models.Model):
    _name = "estimation.vehicle"
    _description = "Estimations of travels management"

    service = fields.Char(string='Service')
    quantity = fields.Integer(string='Quantity')
    amount = fields.Float(string='Amount')
    sub_total = fields.Float(string='Sub Total', compute='_compute_sub_total')
    estimation_id = fields.Many2one('package.travels')

    @api.depends('amount', 'quantity')
    def _compute_sub_total(self):
        for record in self:
            record.sub_total = record.amount * record.quantity
