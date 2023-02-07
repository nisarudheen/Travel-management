from odoo import models, fields


class LocationTravels(models.Model):

    _name = "location.travels"
    _description = "Locations of travel management"
    _rec_name = 'location'

    location = fields.Char(string='Location')