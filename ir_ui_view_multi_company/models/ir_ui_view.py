# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.osv.expression import AND


class IrUiView(models.Model):
    _inherit = "ir.ui.view"
    _inheriting_views_domain_company_operator = (
        "="  # Override this if needed, e.g., use 'parent_of' or 'child_of'
    )

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
                    (
                        "company_id",
                        self._inheriting_views_domain_company_operator,
                        self.env.company.id,
                    ),
                ],
            ]
        )
