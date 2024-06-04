{
    'name':'Real Estate',
    'author':'Syauqi',
    'website':'www.odoo.com',
    'summary':'Training for making estate module',
    'application': True,
    'license':'LGPL-3',
    'demo':[
        'demo/estate.property.xml'
    ],
    'data':[
        'security/ir.model.access.csv',
        'data/estate.property.type.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml',
        'report/estate_report_template.xml',
        'report/estate_report_view.xml'
    ],
}