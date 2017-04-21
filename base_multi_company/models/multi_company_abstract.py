# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import logging

from odoo import api, fields, models
from odoo.tools import ormcache


_logger = logging.getLogger(__name__)


class MultiCompanyAbstract(models.AbstractModel):

    _name = 'multi.company.abstract'
    _description = 'Multi-Company Abstract'

    active = fields.Boolean(
        related='company_active_id.is_active',
    )
    company_active_id = fields.Many2one(
        string='Company Activation',
        comodel_name='company.activate',
        compute='_compute_company_active_id',
        search='_search_company_active_id',
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
    @api.depends('company_ids')
    def _compute_company_id(self):
        for record in self:
            record.company_id = record.company_ids[:1].id

    @api.multi
    @api.depends('company_active_ids')
    @ormcache('self.env.user.company_id.id', 'id')
    def _compute_company_active_id(self):
        for record in self:
            active = record.company_active_ids.filtered(
                lambda r: r.company_id == self.env.user.company_id
            )
            record.company_active_id = active and active.id or False

    @api.model
    def _search_company_active_id(self, operator, value):
        return [
            ('company_active_ids.company_id', operator, value),
        ]
