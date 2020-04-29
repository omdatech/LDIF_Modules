# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Rupam1089 (https://www.freelancer.com/u/Rupamodoo.html)
#
##############################################################################

from odoo import api, fields, models, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
import calendar
from dateutil.relativedelta import relativedelta


class HrEmployeePrivate(models.Model):
    _inherit = "hr.employee"


    def get_pf_employee_rate(self):
        rate = self.company_id.employee_pf_cont
        if self.company_id.pf_discount_applicable:
            if self.employee_age<=self.company_id.employer_career_age_threshold:
                rate = self.company_id.employee_pf_cont_disc
        return rate


    def get_pf_employer_rate(self):
        rate = self.company_id.employer_pf_cont
        if self.company_id.pf_discount_applicable:
            if self.employee_age<=self.company_id.employer_career_age_threshold:
                rate = self.company_id.employer_pf_cont_disc
        return rate


    # @api.depends('order_line.invoice_lines')
    def _get_setting_id(self):
        now = datetime.now()
        days = calendar.monthrange(now.year, now.month)[1]
        for employee in self:
            employee.salary_table_obj = False
            employee.last_performace_obj = False
            if employee.company_id and employee.emp_degree:

                if employee.company_id and employee.company_id.sk_salary_table:
                    for l in employee.company_id.sk_salary_table:
                        if l.emp_degree.id == employee.emp_degree.id:
                            employee.salary_table_obj = l.id
            
                if employee.company_id and employee.company_id.performance_applicable:
                    if employee.company_id.performance_emp_degree_ids and employee.performance_last:
                        for degree in employee.company_id.performance_emp_degree_ids:
                            if degree.id == employee.emp_degree.id:
                                employee.last_performace_obj = employee.performance_last and employee.performance_last.id or False
                                # employee.last_performace_obj = False
                                break
            # raise ValidationError((_("employee.salary_table_obj name: %s")%(employee.salary_table_obj)))


    @api.depends("family_ids.dob", "family_ids.name", "family_ids.relationship", "family_ids.insurance_eligible", "include_employee")
    def _compute_degree_date(self):
        for obj in self:
            no_family = 0
            total_family = 0
            if obj.include_employee:
                total_family+=1
            for line in obj.family_ids:
                if line.relationship in  ["partner", "daughter"]:
                    no_family += 1

                elif line.relationship == "son":
                    if line.dob:
                        birthDate = line.dob
                        today = datetime.now().date() 
                        age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
                        if age< 18:
                            no_family+=1

                if line.insurance_eligible:
                    total_family+=1

            obj.no_family = no_family
            obj.total_family = total_family


    def _compute_family_allowance(self):
        for obj in self:
            spouse = 0.00
            daughter = 0.00
            son = 0.00
            degree_basic = 0.00
            for line in obj.family_ids:
                if line.relationship == "partner":
                    spouse += 50
                elif line.relationship == "daughter":
                    daughter += 25
                elif line.relationship == "son":
                    if line.dob:
                        birthDate = line.dob
                        today = datetime.now().date() 
                        age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
                        if age< 18:
                            son+=25
            # if 
            obj.family_allowance = 150.0 + spouse + daughter + son
            if not obj.eligible_family_exempt:
                obj.family_allowance = 0.00
            # obj.degree_basic = degree_basic



    # @api.depends("birthday")
    def _compute_age_years(self):
        for obj in self:
            obj.employee_age = 0
            if obj.doj:
                birthDate = obj.doj
                today = datetime.now().date() 
                age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
                obj.employee_age = age


    def compute_overtime_attendance(self, firstDate, lastDate):
        hours_worked = 0.00
        overtime = 0.00
        firstDate = datetime(firstDate.year, firstDate.month, firstDate.day)
        lastDate = datetime(lastDate.year, lastDate.month, lastDate.day)
        total_attendance_required = self.env["hr.leave"]._get_number_of_days(firstDate, lastDate, self.id)['hours']

        # Attendance Calculation
        search_attedance = self.env['hr.attendance'].search([("check_in",">=",firstDate), ("check_out","<=",lastDate), ("employee_id","=",self.id)])
        if search_attedance:
            for att in search_attedance:
                hours_worked+=att.worked_hours
        if hours_worked>total_attendance_required:
            overtime = hours_worked - total_attendance_required
        return overtime


    def get_monthly_hours_required(self, firstDate, lastDate):
        firstDate = datetime(firstDate.year, firstDate.month, firstDate.day)
        lastDate = datetime(lastDate.year, lastDate.month, lastDate.day)
        return self.env["hr.leave"]._get_number_of_days(firstDate, lastDate, self.id)['hours']



    def compute_holiday_days(self, firstDate, lastDate):
        holiday_days = 0.00
        search = self.env['hr.leave'].search([("request_date_from",">=",firstDate), ("request_date_to","<=",lastDate), ("employee_id","=",self.id),("holiday_type",'=',"employee"),('state','=','validate')])
        if search:
            for att in search:
                holiday_days+=att.number_of_days
        return holiday_days


    def get_days_in_month(self, date):
        return float((date.replace(month = date.month % 12 +1, day = 1)-timedelta(days=1)).day)





    family_ids = fields.One2many("hr.family", "employee_id", "Family Members")
    family_allowance = fields.Float(compute="_compute_family_allowance", string="Family Allowance")
    emp_degree = fields.Many2one("hr.degree", "Managerial Degree", required=True)
    years_degree = fields.Integer("Years Since Last Degree")
    degree_note = fields.Char("Note")
    no_family = fields.Integer("No of Family Members Eligible for Tax Exempt", compute="_compute_degree_date")
    total_family = fields.Integer("No of Family Members included for Health Insurance Installment", compute="_compute_degree_date")
    
    chk_position_allowance = fields.Boolean("Job Position Allowance")
    chk_transport_allowance = fields.Boolean("Transport Allowance")
    chk_calling_allowance = fields.Boolean("Calling Allowance")
    chk_clothes_allowance = fields.Boolean("Clothes Allowance")
    chk_res_allowance = fields.Boolean("Residential Allowance")
    chk_fuel_allowance = fields.Boolean("Fuel Allowance")
    chk_fixed_allowance = fields.Boolean("Fixed Allowance")


    position_allowance = fields.Boolean("Job Position Allowance", related='company_id.position_allowance')
    transport_allowance = fields.Boolean("Conveyance Allowance", related='company_id.transport_allowance')
    fuel_allowance = fields.Boolean("Fuel Allowance", related='company_id.fuel_allowance')
    calling_allowance = fields.Boolean("Calling Allowance", related='company_id.calling_allowance')
    res_allowance = fields.Boolean("House Rent Allowance", related='company_id.res_allowance')
    clothes_allowance = fields.Boolean("Clothes Allowance", related='company_id.clothes_allowance')


    employee_age = fields.Integer("Employee Career Age", compute="_compute_age_years")
    include_employee = fields.Boolean(string="Include Employee in Health Insurance Premium")
    retired_employee = fields.Boolean(string="Retired")


    doj = fields.Date("Date of First Employment")
    actual_doj = fields.Date("Actual Starting Date")
    allowance_id = fields.Many2one("sk.sal.allowance", "Allowance")
    salary_table_obj = fields.Many2one("sk.sal.table", string='Salary Table', compute="_get_setting_id", readonly=True, copy=False)
    last_performace_obj = fields.Many2one("sk.performance.eval", string='Last Performance', compute="_get_setting_id", readonly=True, copy=False)


    performance_last = fields.Many2one("sk.performance.eval", "Last year performance evaluation")
    eligible_family_exempt = fields.Boolean("Eligible for Family Exemption", default=True)

    employment_type = fields.Selection([
        ("full-time", "Full Time Employee"),
        ("limited", "Limited Full Time Employee"),
        ("unlimited", "Unlimited Full Time Employee"),
        ("contract", "Consultant Contract"),
        ], string="Employment Type")

    monthly_overtime = fields.Float("Monthly Overtime")
    monthly_regular = fields.Float("Monthly Regular Allowance")

    current_month_unpaid_days = fields.Float(compute='_compute_current_month_attendance', string='Unpaid in Days')