# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Rupam1089 (https://www.freelancer.com/u/Rupamodoo.html)
#
##############################################################################

from odoo import api, fields, models, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError


class resCompany(models.Model):
    _inherit = "res.company"


    def write(self, vals):
        employee = self.env['hr.employee'].sudo().search([])
        if "position_allowance" in vals and not vals.get("position_allowance"):
            employee.write({"chk_position_allowance": vals.get("position_allowance")})

        if "transport_allowance" in vals and not vals.get("transport_allowance"):
            employee.write({"chk_transport_allowance": vals.get("transport_allowance")})

        if "fuel_allowance" in vals and not vals.get("fuel_allowance"):
            employee.write({"chk_fuel_allowance": vals.get("fuel_allowance")})

        if "calling_allowance" in vals and not vals.get("calling_allowance"):
            employee.write({"chk_calling_allowance": vals.get("calling_allowance")})

        if "res_allowance" in vals and not vals.get("res_allowance"):
            employee.write({"chk_res_allowance": vals.get("res_allowance")})

        if "clothes_allowance" in vals and not vals.get("clothes_allowance"):
            employee.write({"chk_clothes_allowance": vals.get("clothes_allowance")})
        
        return super(resCompany, self).write(vals)
       

    @api.onchange('pf_discount_applicable')
    def _onchange_pf_discount_applicable(self):
        self.employee_pf_cont = 3.75
        self.employer_pf_cont = 10.5


    def get_tadamon_tax(self):
        if self.tadamon_tax_applicabe:
            return self.tadamon_tax
        return 0.00

    def get_jhad_tax(self):
        if self.jhad_tax_applicabe:
            return self.jhad_tax
        return 0.00



    position_allowance = fields.Boolean("Job Position Allowance", default=True)
    transport_allowance = fields.Boolean("Conveyance Allowance", default=True)
    fuel_allowance = fields.Boolean("Fuel Allowance", default=True)
    calling_allowance = fields.Boolean("Calling Allowance", default=True)
    res_allowance = fields.Boolean("House Rent Allowance", default=True)
    clothes_allowance = fields.Boolean("Clothes Allowance", default=True)


    inc_position_allowance = fields.Boolean("Include in SSF Calculation", default=True)
    inc_transport_allowance = fields.Boolean("Include in SSF Calculation", default=True)
    inc_calling_allowance = fields.Boolean("Include in SSF Calculation", default=True)
    inc_clothes_allowance = fields.Boolean("Include in SSF Calculation", default=True)
    inc_res_allowance = fields.Boolean("Include in SSF Calculation", default=True)
    inc_fuel_allowance = fields.Boolean("Include in SSF Calculation", default=True)



    pf_discount_applicable = fields.Boolean("PF Contribution Discount System Applicable", default=True)
    employer_career_age_threshold = fields.Integer("Employer's Career Age (in years) Threshold for discount eligibility", default=35)
    employee_pf_cont = fields.Float("Employee SSFC %", digits=(16, 3), default=3.750)
    employer_pf_cont = fields.Float("Employer SSFC %", digits=(16, 3), default=10.500)
    employee_pf_cont_disc = fields.Float("Employee SSFC Discount %", digits=(16, 3), default=1.25)
    employer_pf_cont_disc = fields.Float("Employer SSFC DIscount %", digits=(16, 3), default=8.0)


    income_deduction = fields.Boolean("Income Deduction Applicable", default=True)
    upto_1000_deduction = fields.Float("Deduction % Upto 1000", digits=(16, 3), default=5.0)
    above_1000_deduction = fields.Float("Deduction % Above 1000", digits=(16, 3), default=10.0)

    jhad_tax_applicabe = fields.Boolean("Jhad Tax Applicable", default=True)
    jhad_tax = fields.Float("Jhad Tax %", default=3.0, digits=(16, 3))

    tadamon_tax_applicabe = fields.Boolean("Tadamon Tax Applicable", default=True)
    tadamon_tax = fields.Float("Tadamon Tax %", default=1.0, digits=(16, 3))

    sal_allowance_ids = fields.One2many("sk.sal.allowance", "company_id", "Salary Allowance")
    sk_salary_table = fields.One2many("sk.sal.table", "company_id", "Salary Table")
    performace_ids = fields.One2many("sk.performance.eval", "company_id", "Performance")

    performance_applicable = fields.Boolean("Last Performance Evalutation Applicable on Annual Allowance", default=True)
    performance_emp_degree_ids = fields.Many2many("hr.degree",  'rel1', 'rel2', 'rel3', string="Applicable on Degrees")

    health_insurance_applicabe = fields.Boolean("Health Insurance Applicable", default=True)
    health_insurance_rate = fields.Float("Health Insurance Rate/Person", default=8.0, digits=(16, 3))


    @api.onchange('income_deduction')
    def _onchange_income_deduction(self):
        self.upto_1000_deduction = 0
        self.above_1000_deduction = 0
        if self.income_deduction:
            self.upto_1000_deduction = 5.0
            self.above_1000_deduction = 10.0



