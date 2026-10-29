# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class LegalCase(models.Model):
    _name = "legal.case"
    _description = "Legal Case"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(
        string="Case Reference", 
        required=True, 
        readonly=True, 
        copy=False, 
        default=lambda self: _('New')
    )
    title = fields.Char(string="Case Title", required=True, tracking=True)

    client_id = fields.Many2one('res.partner', string="Client", required=True, tracking=True)
    opponent_id = fields.Many2one('res.partner', string="Opponent", tracking=True)
    lawyer_id = fields.Many2one('res.users', string="Lawyer", tracking=True, default=lambda self: self.env.user)

    court_name = fields.Selection([
        ('primary', 'الابتدائية'),
        ('appeal', 'الاستئناف'),
        ('cassation', 'النقض')
    ], string="Court Degree", tracking=True)

    case_number = fields.Char(string="Case Number", tracking=True)

    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)
    claim_amount = fields.Monetary(string="Claim Amount", currency_field='currency_id', tracking=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('pending', 'Pending Court'),
        ('won', 'Won'),
        ('lost', 'Lost'),
        ('settled', 'Settled'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', tracking=True)

    hearing_ids = fields.One2many('legal.hearing', 'case_id', string="Hearings")
    contract_ids = fields.One2many('legal.contract', 'case_id', string="Contracts")

    hearing_count = fields.Integer(string="Hearing Count", compute="_compute_hearing_count", store=True)

    @api.depends('hearing_ids')
    def _compute_hearing_count(self):
        for case in self:
            case.hearing_count = len(case.hearing_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('legal.case') or _('New')
        return super(LegalCase, self).create(vals_list)

    @api.constrains('claim_amount')
    def _check_claim_amount(self):
        for case in self:
            if case.claim_amount < 0:
                raise ValidationError(_("Claim Amount cannot be negative."))

    def action_start(self):
        self.write({'state': 'in_progress'})

    def action_pending(self):
        self.write({'state': 'pending'})

    def action_close(self):
        self.write({'state': 'closed'})

    def action_set_to_draft(self):
        self.write({'state': 'draft'})

    def action_view_hearings(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Hearings'),
            'res_model': 'legal.hearing',
            'view_mode': 'list,form',
            'domain': [('case_id', '=', self.id)],
            'context': {'default_case_id': self.id},
        }
        