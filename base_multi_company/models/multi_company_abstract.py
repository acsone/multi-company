# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class MultiCompanyAbstract(models.AbstractModel):

    _name = 'multi.company.abstract'
    _description = 'Multi-Company Abstract'

    active = fields.Boolean(
        compute='_compute_company_active_status',
        inverse='_inverse_company_active_status',
        search='_search_company_active_status',
    )
    company_active_ids = fields.Many2many(
        string='Company Activations',
        comodel_name='company.activate',
    )
    company_id = fields.Many2one(
        string='Company',
        comodel_name='res.company',
        compute='_compute_company_id',
        store=True,
    )
    company_ids = fields.Many2many(
        string='Companies',
        comodel_name='res.company.assignment',
        default=lambda s: s._default_company_ids(),
        validate=False,
    )

    @api.model
    def _default_company_ids(self):
        Companies = self.env['res.company']
        return [
            (6, 0, Companies._company_default_get().ids),
        ]

    @api.multi
    def _compute_company_active_status(self):
        for record in self:
            record.active = self.env['company.activate'].get_by_resource(
                record,
            )

    @api.multi
    def _inverse_company_active_status(self):
        CompanyActivate = self.env['company.activate']
        for record in self:
            if not record.active:
                CompanyActivate.get_by_resource(record).deactivate()
            else:
                activate = CompanyActivate.upsert_by_resource(
                    record,
                    activate=True,
                )
                record.company_active_ids = [(4, activate.id)]

    @api.multi
    def _search_company_active_status(self, operator, value):
        company = self.env.user.company_id
        return [
            ('company_active_ids.company_id', '=', company.id),
            ('company_active_ids.active', operator, value),
        ]

    @api.multi
    @api.depends('company_ids')
    def _compute_company_id(self):
        for record in self:
            record.company_id = record.company_ids[:1].id
