# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError


class ResCompanyAssignment(models.Model):

    _name = 'res.company.assignment'
    _auto = False

    @api.model_cr
    def __init__(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s
                AS SELECT *
                FROM res_company;
        """ % (self._table))
