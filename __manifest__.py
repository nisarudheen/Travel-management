{
    'name': 'Travels Management',
    'version': '16.0.1.00',
    'sequence': -1,
    'summary': 'Happy journy',
    'website': 'https://www.odoo.com/page/travel_management',
    'category': 'Sales/travel_management',
    'installable': True,
    'application': True,
    'auto_install': False,
    'depends': ['base', 'sale', 'account'],
    'data': [
        'security/user_group.xml',
        'security/ir.model.access.csv',
        'security/user_group.xml',
        'data/sheduled_action.xml',
        'data/tour_packages.xml',
        'data/facilities_service.xml',
        'views/facilities_travels.xml',
        'views/package_estimation.xml',
        'views/package_travels.xml',
        'views/location_travels_view.xml',
        'views/vehicle_travels_view.xml',
        'views/travels_management_table.xml',
        'views/travels_management_views.xml'
    ]
}
