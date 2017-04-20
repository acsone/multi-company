# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class CompanyActiveMixin(models.AbstractModel):

    _name = 'company.active.mixin'
    _description = 'Company Active Mixin'

    active = fields.Boolean(
        compute='_compute_company_active_status',
        inverse='_inverse_company_active_status',
    )
    company_inactive_ids = fields.Many2many(
        string='Company Deactivations',
        comodel_name='company.deactivate',
    )

    @api.multi
    def _compute_company_active_status(self):
        for record in self:
            record.active = self.env['company.deactivate'].get_by_resource(
                record,
            )

    @api.multi
    def _inverse_company_active_status(self):
        CompanyDeactivate = self.env['company.deactivate']
        for record in self:
            if record.active:
                CompanyDeactivate.get_by_resource(record).deactivate()
            else:
                deactivate = CompanyDeactivate.create_by_resource(record)
                record.company_inactive_ids = [(4, deactivate.id)]
