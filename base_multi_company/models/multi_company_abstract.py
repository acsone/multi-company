# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class MultiCompanyAbstract(models.AbstractModel):

    _name = 'multi.company.abstract'
    _description = 'Multi-Company Abstract'

    active = fields.Boolean(
        company_dependent=True,
        default=True,
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
    @api.depends('company_ids')
    def _compute_company_id(self):
        for record in self:
            record.company_id = record.company_ids[:1].id
