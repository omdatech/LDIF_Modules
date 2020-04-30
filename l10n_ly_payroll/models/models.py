# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Rupam1089 (https://www.freelancer.com/u/Rupamodoo.html)
#
##############################################################################

from odoo import api, fields, models, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError

GRADE = {
    "poor": "Poor",
    "avge": "Average",
    "good": "Good",
    "very": "Very Good",
    "excellent": "Excellent"
}

class SkSalAllowance(models.Model):
    _name = "sk.sal.allowance"
    _description = "Update Allowances Table model"

    name = fields.Char("Allowance Name", translate=True)
    position_allowance = fields.Float("Position Allowance")
    transport_allowance = fields.Float("Transport Allowance")
    fuel_allowance = fields.Float("Fuel Allowance")
    calling_allowance = fields.Float("Calling Allowance")
    clothes_allowance = fields.Float("Clothes Allowance")
    res_allowance = fields.Float("Residential Allowance")
    overtime_allowance = fields.Float("Hourly Rate for Overtime")
    job_id = fields.Many2one("hr.job", "Associated Job")
    company_id = fields.Many2one('res.company', 'Company')



class SkSalTable(models.Model):
    _name = "sk.sal.table"
    _rec_name = "emp_degree"
    _description = "Update Salary Table model"


    emp_degree = fields.Many2one("hr.degree", "Degree", required=True)
    basic = fields.Float("Basic", required=True)
    annual_allowance = fields.Float("Annual Allowance", required=True)
    min_years_appraisal = fields.Float("Appraisal Min Years in the degree")
    max_years_appraisal = fields.Float("Appraisal Max Years in the degree")
    company_id = fields.Many2one("res.company", "Company")


    @api.constrains('company_id', 'emp_degree')
    def _check_order_line_setting_id(self):
        for order in self:
            check = self.search([("company_id","=",order.company_id.id), ("emp_degree", "=", order.emp_degree.id), ("id","!=",order.id)])
            if check:
                raise ValidationError((_("You cannot create multiple salary rule for one degree: %s")%(order.emp_degree.name)))



class HrFamily(models.Model):
    _name = "hr.family"
    _description = "Update Family Table model"


    employee_id = fields.Many2one("hr.employee", "Employee")
    name = fields.Char("Name", required=True)
    dob = fields.Date("Date of Birth", required=True)
    national_id = fields.Char("National ID")
    contact_no = fields.Char("Contact No")
    relationship = fields.Selection([
        ("father", "Father"),
        ("mother", "Mother"),
        ("son", "Son"),
        ("daughter", "Daughter"),
        ("partner", "Partner/Spouse"),
        ], string="Relationship", required=True)
    insurance_eligible = fields.Boolean("Health Insurance Eligiblity")


    # @api.constrains('contact_no')
    # def _check_order_contact_no(self):
    #     for order in self:
    #         if len(order.contact_no) !=10:
    #             raise ValidationError((_("Contact Number must be of 10 character length: %s")%(order.contact_no)))


    # @api.constrains('national_id')
    # def _check_order_national_id(self):
    #     for order in self:
    #         if len(order.national_id) !=10:
    #             raise ValidationError((_("National ID must be of 12 character length: %s")%(order.national_id)))



class HrDegree(models.Model):
    _name = "hr.degree"
    _description = "Update Degree Table model"

    name = fields.Char("Name", required=True)

    @api.constrains('name')
    def _check_order_line_name_degree(self):
        for order in self:
            check = self.search([("id","!=",order.id)])
            if check:
                for rec in check:
                    if rec.name.lower() == order.name.lower() :
                        raise ValidationError((_("You cannot create degree with same name: %s")%(order.name)))



class SkPerformanceEval(models.Model):
    _name = "sk.performance.eval"
    _description = "Update Performance Table model"

    def name_get(self):
        return [(value.id, "%s : %s" % (GRADE.get(value.grade, ""), value.perf_percent)) for value in self]


    grade = fields.Selection([("poor", "Poor"), ("avge","Average"), ("good", "Good"), ("very", "Very Good"), ("excellent", "Excellent")], required=True)
    perf_percent = fields.Float("Reward %", required=True)
    company_id = fields.Many2one('res.company', 'Company')

    @api.constrains('company_id', 'grade')
    def _check_order_line_setting_id(self):
        for order in self:
            check = self.search([("company_id","=",order.company_id.id), ("grade", "=", order.grade), ("id","!=",order.id)])
            if check:
                raise ValidationError((_("You cannot create multiple entries for same grade: %s")%(GRADE.get(order.grade, ""))))


