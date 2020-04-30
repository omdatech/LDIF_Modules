# -*- coding: utf-8 -*-
#########################################################################
#
#   Author: Rupam1089 (https://www.freelancer.com/u/Rupamodoo.html)
#
#########################################################################
{
    'name': 'Payroll Localization',
    'summary': 'Customisation in Payroll, Localization for Libya',
    'sequence': 1,
    'category': 'Backend',
    'author': "rupamodoo",
    'website': 'https://www.freelancer.com/u/Rupamodoo.html',
    'depends': ["hr_payroll", "hr_payroll_expense", "hr_holidays_attendance", "account_accountant", "hr_skills", "hr_loan", "hr_holidays"],
    'data': [
        'security/payroll_security.xml',
        'security/ir.model.access.csv',
        'views/models_views.xml',
        'views/hr_employee_views.xml',
        'views/hr_payroll_structure_views.xml',
        'views/res_company_views.xml',
        "data/banks_data.xml",
        "data/payroll_data.xml",
        "data/full_time_employee_data.xml",
        "data/limited_full_time_employee_data.xml",
        "data/unlimited_full_time_employee_data.xml",
        "data/contract_employee_data.xml",
        "data/base_data.xml"
    ],
    'installable': True,
    'application': True
}
