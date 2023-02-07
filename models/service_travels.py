from odoo import models, fields, api


class ServiceTravels(models.Model):
    _name = "service.travels"
    _description = "services of travels management"

    name = fields.Char(string="Name")
    expiration_period = fields.Integer(string="Days")
    package = fields.Boolean(string='Package')


class VehicleTravels(models.Model):
    _name = "vehicle.travels"
    _description = "vehicles of travel management"

    registration_no = fields.Char(string='Registration No')
    vehicle_type = fields.Selection(string='Vehicle Type',
                                    selection=[('bus', 'Bus'),
                                               ('traveller', 'Traveller'),
                                               ('van', 'Van'),
                                               ('other', 'Other')])
    name = fields.Char(string='Name', store=True)
    number_of_seats = fields.Integer(default=1, string='Number Of Seat')
    service = fields.Char(string='Service')
    quantity = fields.Integer(default=1, string='Quantity')
    unit = fields.Integer(string='Unit')
    amount = fields.Float(string='Amount')
    facilities_id = fields.Many2many("facilities.travels",
                                     string="Facilities")
    order_line_travel_ids = fields.One2many('vehicle.charges',
                                            'travel_id',
                                            string="Travel Lines",)
    date = fields.Date(default=fields.Date.today())

    _sql_constraints = [('name_unique', 'unique(registration_no)',
                         'This registration number already take.')]

    @api.onchange('vehicle_type')
    def _onchange_vehicle_type(self):
        if self.registration_no:
            result_name = f"{self.registration_no} ({self.vehicle_type})"
            self.name = result_name


class VehicleCharges(models.Model):
    _name = "vehicle.charges"
    _description = "Charges of vehicles"

    service = fields.Char(string="Service")
    travel_id = fields.Many2one('vehicle.travels')
    quantity = fields.Integer(default=1, string='Quantity')
    unit = fields.Integer(string='Unit')
    amount = fields.Float(string='Amount')


