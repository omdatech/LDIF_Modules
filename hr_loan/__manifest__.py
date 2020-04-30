# -*- coding: utf-8 -*-
#########################################################################
#
#   Author: Rupam1089 (https://www.freelancer.com/u/Rupamodoo.html)
#
#########################################################################
{
    'name': 'Employee Loan Management',
    'summary': 'Employee Loan Management',
    'sequence': 5,
    'category': 'hr',
    'author': "rupamodoo",
    'website': 'https://www.freelancer.com/u/Rupamodoo.html',
    'depends': ["hr", "hr_skills", "hr_payroll"],
    'data': [
        'data/ir_sequence_data.xml',
        'security/ir.model.access.csv',
        'views/models_views.xml',
        ],
    'installable': True,
    'application': False
}
