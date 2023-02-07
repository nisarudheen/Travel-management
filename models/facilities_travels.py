from odoo import models, fields


class FacilitiesTravels(models.Model):

    _name = "facilities.travels"
    _description = "Facilities of travel management"

    name = fields.Char(string='Name')
