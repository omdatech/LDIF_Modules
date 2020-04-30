# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Rupam1089 (https://www.freelancer.com/u/Rupamodoo.html)
#
##############################################################################

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class HrContract(models.Model):
    _inherit = "hr.contract"
    _description = "modify employee contract"


    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            dd = datetime.now().strftime("%m-%Y")
            structure_type_id = False
            ir_model_data = self.env['ir.model.data']
            if self.employee_id.employment_type and self.employee_id.employment_type == 'full-time':
                try:
                    structure_type_id = ir_model_data.get_object_reference('l10n_ly_payroll', 'full_time_employee_type')[1]
                except ValueError:
                    structure_type_id = False
            elif self.employee_id.employment_type and self.employee_id.employment_type == 'limited':
                try:
                    structure_type_id = ir_model_data.get_object_reference('l10n_ly_payroll', 'limited_full_time_employee_type')[1]
                except ValueError:
                    structure_type_id = False

            elif self.employee_id.employment_type and self.employee_id.employment_type == 'unlimited':
                try:
                    structure_type_id = ir_model_data.get_object_reference('l10n_ly_payroll', 'unlimited_full_time_employee_type')[1]
                except ValueError:
                    structure_type_id = False
            elif self.employee_id.employment_type and self.employee_id.employment_type == 'contract':
                try:
                    structure_type_id = ir_model_data.get_object_reference('l10n_ly_payroll', 'contract_employee_type')[1]
                except ValueError:
                    structure_type_id = False
            else:
                try:
                    structure_type_id = ir_model_data.get_object_reference('l10n_ly_payroll', 'other_employee_type')[1]
                except ValueError:
                    structure_type_id = False
            
            self.job_id = self.employee_id.job_id
            self.department_id = self.employee_id.department_id
            self.resource_calendar_id = self.employee_id.resource_calendar_id
            self.company_id = self.employee_id.company_id
            self.structure_type_id = structure_type_id
            self.name = "Contract:%s-%s"%(self.employee_id.name, dd)



    @api.onchange('degree.id')
    def _onchange_degree_id(self):
        basic = 0.00
        annual_allowance = 0.00
        degree = self.employee_id and self.employee_id.emp_degree or False
        performance = self.employee_id and self.employee_id.performance_last or False
        if self.company_id.sk_salary_table and degree:
            for line in self.company_id.sk_salary_table:
                if line.emp_degree.id == degree.id:
                    basic = line.basic
                    annual_allowance = line.annual_allowance
                    break
            if performance:
                for degree in self.company_id.performance_emp_degree_ids:
                    if degree.id == degree.id:
                        annual_allowance = annual_allowance*self.employee_id.performance_last.perf_percent*0.01
                        break
            self.wage = basic + annual_allowance


    show_wage = fields.Boolean(related='structure_type_id.show_wage', string="Show Wage", readonly=True)
    wage = fields.Float('Wage', required=True, digits=(16, 3),precision_digits=3, tracking=True, help="Employee's monthly gross wage.")
    hourly_wage = fields.Float('Hourly Wage', digits=(16, 3),precision_digits=3, default=0, required=True, tracking=True, help="Employee's hourly gross wage.")
