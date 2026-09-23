{
    'name': 'Conference Sessions',
    'version': '19.0.1.0.0',
    'summary': 'Track sessions for conferences and training events',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_config_parameter.xml',
        'views/conference_session_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}
