# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.osv.expression import AND


class IrUiView(models.Model):
    _inherit = "ir.ui.view"

    company_id = fields.Many2one("res.company", string="Company", index=True)

    @api.model
    def _get_inheriting_views_domain(self):
        domain = super()._get_inheriting_views_domain()
        domain = domain if domain else []
        return AND(
            [
                domain,
                [
                    "|",
                    ("company_id", "=", False),
                    ("company_id", "=", self.env.company.id),
                ],
            ]
        )


class Model(models.AbstractModel):
    _inherit = "base"

    @api.model
    def _get_view_cache_key(self, view_id=None, view_type="form", **options):
        """view cache dependent on the company"""
        key = super()._get_view_cache_key(view_id, view_type, **options)
        return key + (self.env.company,)
