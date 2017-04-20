# -*- coding: utf-8 -*-
# Copyright 2015-2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# Copyright 2017 LasLabs Inc.
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import api, SUPERUSER_ID


def post_init_hook(cr, rule_ref, model_name):
    """ Set the `domain_force` and default `company_ids` to `company_id`.

    Args:
        cr (Cursor): Database cursor to use for operation.
        rule_ref (string): XML ID of security rule to write the
            `domain_force` from.
        model_name (string): Name of Odoo model object to search for
            existing records.
    """
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        # Change access rule
        rule = env.ref(rule_ref)
        rule.write({
            'active': True,
            'domain_force': (
                "['|', ('company_ids', 'in', user.company_id.ids),"
                " ('company_id', '=', False)]"
            ),
        })
        # Copy company values
        model = env[model_name]
        groups = model.read_group([], ['company_id'], ['company_id'])
        for group in groups:
            if not group['company_id']:
                continue
            records = model.search(group['__domain'])
            records.write({
                'company_ids': [(6, 0, [group['company_id'][0]])],
            })


def uninstall_hook(cr, rule_ref):
    """ Restore product rule to base value.

    Args:
        cr (Cursor): Database cursor to use for operation.
        rule_ref (string): XML ID of security rule to remove the
            `domain_force` from.
    """
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        # Change access rule
        rule = env.ref(rule_ref)
        rule.write({
            'active': False,
            'domain_force': (
                " ['|', ('company_id', '=', user.company_id.id),"
                " ('company_id', '=', False)]"
            ),
        })


__all__ = [
    'post_init_hook',
    'uninstall_hook',
]
