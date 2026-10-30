# -*- coding: utf-8 -*-
{
    'name': 'Legal Management',
    'version': '18.0.1.0.0',
    'summary': 'Legal Cases, Hearings, and Contracts Management System for Odoo 18',
    'description': """
        System to manage legal department and law firms:
        - Cases tracking & Court degrees
        - Hearings scheduling & Calendar
        - Contracts management & Automated expirations
        - Portal access for clients
    """,
    'category': 'Legal',
    'author': 'Ahmed Sameh',
    'depends': [
        'base',
        'mail',
        'portal',
    ],
    'data': [
        # 1. Sequences & Cron Jobs
        'data/ir_sequence_data.xml',
        'data/cron_jobs.xml',

        # 2. Security (Groups, ACLs, Record Rules)
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'security/record_rules.xml',

        # 3. Views & Menus
        'views/legal_case_view.xml',
        'views/legal_hearing_views.xml',
        'views/legal_contract_views.xml',
        'views/res_partner_view.xml',
        'views/ui_customization.xml',
        'demo/legal_management_demo.xml',
        'views/menu.xml',

        # 4. Reports PDF
        'report/case_summary_report.xml',
        'report/contract_template.xml',
    ],
    'demo': [
        'demo/legal_management_demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'legal_managment/static/src/scss/custom_styles.scss',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
