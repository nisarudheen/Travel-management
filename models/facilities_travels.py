from odoo import models, fields


class FacilitiesTravels(models.Model):

    _name = "facilities.travels"
    _description = "Facilities  Travel"

    name = fields.Char(string='Name')
