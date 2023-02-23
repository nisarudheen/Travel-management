from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import Request, Controller


class TravelsWebPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id
        count = request.env['booking.travels'].sudo().search_count([('customer_id', '=', partner.id)])
        if 'count_booking' in counters:
             values['count_booking'] = count
        return values


class PortalBooking(Controller):
    @http.route(['/my/bookings'], type='http', auth="user", website=True)
    def bookings_portal(self):
        partner_id = request.env.user.partner_id
        bookings = request.env['booking.travels']\
            .sudo().search([('customer_id', '=', partner_id.id)])
        values = {}
        values.update({
                'ref': bookings
        })
        return request.render("travels_management.portal_my_booking", values)


