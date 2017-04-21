# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, models


class IrProperty(models.Model):

    _inherit = 'ir.property'

    @api.model
    def get(self, name, model, res_id=False):
        res = super(IrProperty, self).get(name, model, res_id)
        if res:
            return res
        field = self.env[model]._fields[name]
        # Must use original args because `field.default` is actually
        #   property.get()
        default = field._attrs.get('company_default')
        if default is None:
            return
        return default() if callable(default) else default
