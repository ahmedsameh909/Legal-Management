# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class LegalContract(models.Model):
    _name = 'legal.contract'
    _description = 'Legal Contract'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Contract Ref', required=True, readonly=True, copy=False, default=lambda self: _('New'))
    title = fields.Char(string='Contract Title', required=True, tracking=True)
    
    partner_id = fields.Many2one('res.partner', string='Partner / Client', required=True, tracking=True)
    case_id = fields.Many2one('legal.case', string='Related Case')
    responsible_user_id = fields.Many2one('res.users', string='Responsible Lawyer', default=lambda self: self.env.user)

    contract_type = fields.Selection([
        ('retainer', 'Legal Retainer'),
        ('consultation', 'Consultation Agreement'),
        ('settlement', 'Settlement Agreement'),
        ('nda', 'Non-Disclosure Agreement (NDA)'),
        ('other', 'Other')
    ], string='Contract Type', required=True, default='retainer')

    start_date = fields.Date(string='Start Date', required=True, default=fields.Date.context_today)
    end_date = fields.Date(string='End Date', required=True)
    auto_renew = fields.Boolean(string='Auto Renew', default=False)
    notice_period_days = fields.Integer(string='Notice Period (Days)', default=30)

    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)
    contract_amount = fields.Monetary(string='Contract Value', currency_field='currency_id')

    terms_and_conditions = fields.Html(string='Terms and Conditions')
    notes = fields.Text(string='Internal Notes')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_approval', 'Pending Approval'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('terminated', 'Terminated'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('legal.contract') or _('New')
        return super(LegalContract, self).create(vals_list)

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date and record.start_date > record.end_date:
                raise ValidationError(_("End Date cannot be earlier than Start Date."))

    def action_submit_for_approval(self):
        self.write({'state': 'in_approval'})

    def action_activate(self):
        self.write({'state': 'active'})

    def action_expire(self):
        self.write({'state': 'expired'})

    def action_terminate(self):
        self.write({'state': 'terminated'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_reset_to_draft(self):
        self.write({'state': 'draft'})