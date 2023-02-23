from odoo import models, fields


class LocationTravels(models.Model):

    _name = "location.travels"
    _description = "Locations Travels"
    _rec_name = 'location'

    location = fields.Char(string='Location')
