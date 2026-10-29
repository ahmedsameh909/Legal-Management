# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class LegalHearing(models.Model):
    _name = 'legal.hearing'
    _description = 'Court Hearing'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Hearing Ref', required=True, readonly=True, copy=False, default=lambda self: _('New'))
    case_id = fields.Many2one('legal.case', string='Case', required=True, ondelete='cascade', tracking=True)
    client_id = fields.Many2one('res.partner', related='case_id.client_id', string='Client', readonly=True)
    lawyer_id = fields.Many2one('res.users', string='Attending Lawyer', tracking=True)
    
    date = fields.Datetime(string='Hearing Date', required=True, tracking=True)
    court_name = fields.Selection(related='case_id.court_name', string='Court', readonly=True)
    court_room = fields.Char(string='Court Room / Hall')
    judge_name = fields.Char(string='Judge Name')

    summary = fields.Text(string='Hearing Summary / Requirements')
    decision = fields.Text(string='Court Decision', tracking=True)
    next_hearing_date = fields.Datetime(string='Next Hearing Date')
    postponed_reason = fields.Text(string='Postponement Reason')

    state = fields.Selection([
        ('scheduled', 'Scheduled'),
        ('attended', 'Attended'),
        ('postponed', 'Postponed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='scheduled', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('legal.hearing') or _('New')
        return super(LegalHearing, self).create(vals_list)

    def action_mark_attended(self):
        self.write({'state': 'attended'})

    def action_postpone(self):
        self.write({'state': 'postponed'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_reset_to_scheduled(self):
        self.write({'state': 'scheduled'})