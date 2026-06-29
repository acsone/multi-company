# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

_WEBSITE_SALE_DOMAIN = (
    "['|', ('company_id', 'in', [False, website.company_id.id]),"
    " ('company_id', 'in', company_ids)]"
)


def uninstall_hook(env):
    for xmlid in (
        "website_sale.product_pricelist_comp_rule",
        "website_sale.product_pricelist_item_comp_rule",
    ):
        env.ref(xmlid).domain_force = _WEBSITE_SALE_DOMAIN
