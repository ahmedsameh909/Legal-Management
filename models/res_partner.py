# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_legal_client = fields.Boolean(string='Is Legal Client', default=False)
    is_opponent = fields.Boolean(string='Is Opponent', default=False)
    national_id = fields.Char(string='National ID / Commercial Reg', tracking=True)

    case_ids = fields.One2many('legal.case', 'client_id', string='Legal Cases')
    case_count = fields.Integer(string='Case Count', compute='_compute_legal_counts')

    contract_ids = fields.One2many('legal.contract', 'partner_id', string='Contracts')
    contract_count = fields.Integer(string='Contract Count', compute='_compute_legal_counts')

    @api.depends('case_ids', 'contract_ids')
    def _compute_legal_counts(self):
        for partner in self:
            partner.case_count = len(partner.case_ids)
            partner.contract_count = len(partner.contract_ids)

    def action_view_partner_cases(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Cases'),
            'res_model': 'legal.case',
            'view_mode': 'list,form',
            'domain': [('client_id', '=', self.id)],
            'context': {'default_client_id': self.id},
        }

    def action_view_partner_contracts(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Contracts'),
            'res_model': 'legal.contract',
            'view_mode': 'list,form',
            'domain': [('partner_id', '=', self.id)],
            'context': {'default_partner_id': self.id},
        }