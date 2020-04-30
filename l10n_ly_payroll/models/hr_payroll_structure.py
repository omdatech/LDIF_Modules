# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Rupam1089 (https://www.freelancer.com/u/Rupamodoo.html)
#
##############################################################################

from odoo import api, fields, models, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError


class HrWorkEntryType(models.Model):
    _inherit = 'hr.work.entry.type'
    _description = "Update work entry type"

    is_overtime = fields.Boolean("Overtime")

class HrPayrollStructureType(models.Model):
    _inherit = 'hr.payroll.structure.type'
    _description = "Update salary structre model"

    show_wage = fields.Boolean("Show Wage Field in Employee Contract")

