# -*- coding: utf-8 -*-
# Copyright 2015-2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# Copyright 2017 LasLabs Inc.
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import api, SUPERUSER_ID


def post_init_hook(cr, rule, model):
    """ Set the `domain_force` and default `company_ids` to `company_id`.
    
    Args:
        cr (Cursor): Database cursor to act upon.
        rule (IRRule): Security rule to write the `domain_force` to.
        model (Model): Odoo model object to search for existing records.
    """
    """Put domain in product access rule and copy company_id as the default
    value in new field company_ids."""
    # Change access rule
    rule.write({
        'active': True,
        'domain_force': (
            "['|', ('company_ids', 'in', user.company_id.ids),"
            " ('company_id', '=', False)]"
        ),
    })
    # Copy company values
    groups = model.read_group([], ['company_id'], ['company_id'])
    for group in groups:
        if not group['company_id']:
            continue
        records = model.search(group['__domain'])
        records.write({
            'company_ids': [(6, 0, [group['company_id'][0]])],
        })


def uninstall_hook(cr, rule):
    """ Restore product rule to base value.  
    
    Args:
        rule (IRRule): Security rule to remove the `domain_force` from.
    """
    rule.write({
        'active': False,
        'domain_force': (
            " ['|',('company_id','=',user.company_id.id),"
            "('company_id','=',False)]"
        ),
    })
