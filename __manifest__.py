{'name': 'Travels Management',
 'version': '16.0.1.0.0',
 'sequence': -1,
 'summary': 'Happy journy',
 'website': 'https://www.odoo.com/page/travel_management',
 'category': 'Sales/travel_management',
 'installable': True,
 'application': True,
 'auto_install': False,
 'depends': ['base', 'sale', 'account','website',],
 'data': [
     'security/user_group.xml',
     'security/ir.model.access.csv',
     'data/sheduled_action.xml',
     'data/tour_packages.xml',
     'data/facilities_service.xml',
     'data/website_travels.xml',
     'wizard/report_travels.xml',
     'report/report_travels.xml',
     'views/success_website.xml',
     'views/travels_web_portal.xml',
     'views/facilities_travels.xml',
     'views/website_travels.xml',
     'views/package_estimation.xml',
     'views/package_travels.xml',
     'views/location_travels_view.xml',
     'views/vehicle_travels_view.xml',
     'views/travels_management_views.xml',
     'views/travels_management_menu.xml'
 ],
 'assets':{
     'web.assets_backend':[
         'travels_management/static/src/js/action_manager.js'
     ],
     'web.assets_frontend': [
         'travels_management/static/src/js/location_filter.js'
     ]
     }
 }
