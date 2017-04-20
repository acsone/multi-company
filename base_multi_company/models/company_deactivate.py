# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class CompanyDeactivate(models.Model):

    _name = 'company.deactivate'
    _description = 'Company Deactivations'

    active = fields.Boolean(
        default=True,
    )
    resource_ref = fields.Reference(
        string='Resource',
        selection='_get_resource_types',
        required=True,
    )
    resource_int = fields.Integer(
        compute='_compute_resource_int',
        required=True,
        store=True,
    )
    model_name = fields.Char(
        compute='_compute_model_name',
        required=True,
        store=True,
    )
    company_id = fields.Many2one(
        string='Company',
        comodel_name='res.company',
        required=True,
    )

    @api.model
    def _get_resource_types(self):
        """ Return the models implementing the mixin. """
        fields = self.env['ir.model.fields'].search([
            ('name', '=', 'company_inactive_ids'),
        ])
        models = self.env['ir.model'].search([
            ('field_id', 'in', fields.ids),
        ])
        return [(m.model, m.name) for m in models]

    @api.multi
    @api.depends('resource_ref')
    def _compute_model_name(self):
        """ Determine the model name when the resource changes. """
        for record in self:
            record.model_name = record.resource_ref._name

    @api.multi
    @api.depends('resource_ref')
    def _compute_resource_int(self):
        """ Determine the resource ID when the resource changes. """
        for record in self:
            record.resource_int = record.resource_ref.id

    @api.multi
    def _check_resource_company(self):
        """ Do not allow two active for the same resource and company. """
        for record in self:
            matches = self.get_by_resource(
                record.resource_ref, record.company_id,
            )
            if len(matches) > 1:
                raise ValidationError(_(
                    'Cannot have two deactivation records for the same '
                    'resource on the same company.',
                ))

    @api.multi
    def deactivate(self):
        """ Deactivate the records. """
        return self.write({'active': False})

    @api.model
    def create_by_resource(self, record, company=None):
        """ Create a new CompanyDeactivate for the record and company. """
        return self.create({
            'resource_ref': record,
            'company_id': company.id,
        })

    @api.model
    def get_by_resource(self, record, company=None):
        """ Return the CompanyDeactivate for the resource and company. """
        if company is None:
            company = self.env.user.company_id
        return self.search([
            ('model_name', '=', record._name),
            ('resource_int', '=', record.id),
            ('company_id', '=', company.id),
        ])
