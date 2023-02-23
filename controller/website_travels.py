from odoo import http
from odoo.http import request
from datetime import datetime


class WebsiteForm(http.Controller):
    @http.route(['/booking'], type='http', auth="user",
                website=True, csrf=False)
    def booking(self):
        value = {}
        location = request.env['location.travels'].sudo().search([])
        service = request.env['service.travels'].sudo().search([])
        value.update({
            'location': location,
            'services': service
        })
        return request.render("travels_management.website_travels_booking",
                              value)

    @http.route(['/booking/submit/'], type='http', auth="user", website=True,
                csrf=False)
    def submit(self, **post):
        customer_id = request.env['res.partner'].sudo().create({
            'name': post.get('name')
        })
        date = post.get('travel_date')
        date_travels = datetime.strptime(date, '%Y-%m-%d').date()
        print(post.get('destination_location'))
        dest_id = request.env['location.travels'].sudo().search(
            [('location', '=', post.get('destination_location'))])
        booking = request.env['booking.travels'].sudo().create({
            'customer_id': customer_id.id,
            'no_of_passengers': post.get('no_of_passengers'),
            'travel_Date': date_travels,
            'source_location_id': post.get('source_location'),
            'destination_location_id': dest_id.id,
            'service_id': post.get('service')
        })
        vals = {
            'booking': booking
        }
        return request.render("travels_management.website_form_success",
                              vals)

    @http.route(['/booking/location'], type='json', auth="user",
                methods=['POST'],
                csrf=False)
    def web_location(self, location):
        list = []
        locations = request.env['location.travels'] \
            .sudo().search([('id', '!=', location)])
        for i in locations:
            list.append(i.location)
        return list
