# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Rupam1089 (https://www.freelancer.com/u/Rupamodoo.html)
#
##############################################################################

from odoo import api, fields, models, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta



class Employee(models.Model):
    _inherit = "hr.employee"
    _description = "Update Employee model"


    def _compute_loan_count(self):
        for employee in self:
            employee.loan_count = self.env['employee.loan'].search_count([("employee_id","=",employee.id)])


    def get_installment(self, firstDate, lastDate):
        for employee in self:
            emi = 0.00
            # current_date = datetime.now().date()
            # firstDate = current_date.replace(day=1)
            # lastDate = current_date + relativedelta(months=1)
            # lastDate = lastDate.replace(day=1)+ timedelta(days=-1)
            if employee.loan_lines:
                for line in employee.loan_lines:
                    if line.start_date >= firstDate and line.start_date <= lastDate:
                        emi += line.amount
            return emi


    loan_count = fields.Integer(compute='_compute_loan_count', string='Loan Count')
    loan_lines = fields.One2many("loan.installement", "employee_id", string="Loan")


    def return_action_to_open_loan(self):
        self.ensure_one()
        xml_id = "action_hr_loan_settings"
        if xml_id:
            rec = self.env['employee.loan'].search([("employee_id","=",self.id)])
            res = self.env['ir.actions.act_window'].for_xml_id('hr_loan', xml_id)
            res.update(
                domain=[('id', 'in', rec.ids)]
            )
            return res
        return False


class employeeLoan(models.Model):
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _name = "employee.loan"
    _description = "Update Empoly Loan model"


    def action_confirm_loan(self):
        for line in self.installment_lines:
            line.write({"employee_id": self.employee_id.id})
        return self.write({"state": "confirm"})


    def action_reject_loan(self):
        for line in self.installment_lines:
            line.write({"employee_id": False})
        return self.write({"state": "cancel"})


    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('employee.loan') or _('New')
        return super(employeeLoan, self).create(vals)


    @api.onchange('start_date', "tennure", "loan_amt")
    def _compute_installments(self):
        for record in self:
            if record.start_date and record.tennure:
                result = []
                tennure = float(max(record.tennure, 1))
                emi = record.loan_amt / tennure
                for x in range(max(record.tennure, 1)):
                    if x == 0:
                        dt = record.start_date
                    else:
                        dt = record.start_date + relativedelta(months=x)
                    result.append((0, 0, {'amount':emi, "start_date": dt}))
                record.installment_lines=False
                record.installment_lines=result



    name = fields.Char("Name", default="/")
    employee_id = fields.Many2one("hr.employee", string="Employee", tracking=1, readonly=True, states={'draft': [('readonly', False)]})
    tennure = fields.Integer("Tennure in Months", readonly=True, states={'draft': [('readonly', False)]})
    loan_amt = fields.Float("Loan Amount", readonly=True, states={'draft': [('readonly', False)]})
    request_date = fields.Date("Request Date", tracking=1, readonly=True, states={'draft': [('readonly', False)]})
    start_date = fields.Date("Repayment Start Date", tracking=1, readonly=True, states={'draft': [('readonly', False)]})
    company_id = fields.Many2one('res.company', string='Company', required=True, index=True, default=lambda self: self.env.company, readonly=True, states={'draft': [('readonly', False)]})

    installment_lines = fields.One2many("loan.installement", "loan_id", string='Lines',  states={'cancel': [('readonly', True)], 'confirm': [('readonly', True)]}, copy=True, auto_join=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, default='draft')



class loanInstallement(models.Model):
    _name = "loan.installement"
    _description = "Update Loan Installment model"

    employee_id = fields.Many2one("hr.employee", string="Employee")
    loan_id = fields.Many2one("employee.loan", string="Loan")
    start_date = fields.Date("Repayment Date")
    amount = fields.Float("Monthly Installment")
