from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    has_deposit = fields.Boolean(
        string='Support Guarantee (SGR)',
        help='Check this if the product requires a guarantee deposit',
        default=False,
    )
    deposit_product_id = fields.Many2one(
        'product.product',
        string='Deposit Product',
        help='Service product used for the guarantee deposit',
        domain=[('type', '=', 'service')],
    )

    def _get_fields_for_pos(self):
        fields = super()._get_fields_for_pos()
        fields += ['has_deposit', 'deposit_product_id']
        _logger.info('POS fields for product.template: %s', fields)
        return fields

    @api.onchange('type')
    def _onchange_type(self):
        """Clear deposit settings if product becomes a service"""
        res = super()._onchange_type()
        if self.type == 'service':
            self.has_deposit = False
            self.deposit_product_id = False
        return res

class ProductProduct(models.Model):
    _inherit = 'product.product'

    has_deposit = fields.Boolean(
        related='product_tmpl_id.has_deposit',
        readonly=False,
        store=True,
    )
    deposit_product_id = fields.Many2one(
        related='product_tmpl_id.deposit_product_id',
        readonly=False,
        store=True,
    )

    def _get_fields_for_pos(self):
        fields = super()._get_fields_for_pos()
        fields += ['has_deposit', 'deposit_product_id']
        _logger.info('Loading product %s (ID: %s) with has_deposit=%s, deposit_product_id=%s',
                    self.name, self.id, self.has_deposit, self.deposit_product_id.id if self.deposit_product_id else None)
        return fields

class PosSession(models.Model):
    _inherit = 'pos.session'

    def _pos_ui_models_to_load(self):
        result = super()._pos_ui_models_to_load()
        if 'product.product' not in result:
            result.append('product.product')
        return result

    def _loader_params_product_product(self):
        result = super()._loader_params_product_product()
        result['search_params']['fields'].extend(['has_deposit', 'deposit_product_id'])
        return result

    def _get_pos_ui_product_product(self, params):
        result = super()._get_pos_ui_product_product(params)
        products = self.env['product.product'].browse([p['id'] for p in result])
        
        for product_data, product in zip(result, products):
            if product.has_deposit and product.deposit_product_id:
                _logger.info(f"Product {product.name} has deposit: {product.has_deposit} and deposit product: {product.deposit_product_id.name}")
                product_data.update({
                    'has_deposit': True,
                    'deposit_product_id': product.deposit_product_id.id,
                })
        
        return result 