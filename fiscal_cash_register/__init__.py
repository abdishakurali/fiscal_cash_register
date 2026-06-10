# -*- coding: utf-8 -*-

from . import models
from . import controllers
from . import report
from . import wizard


def post_init_hook(env):
    """Initialize fiscal settings for existing POS configurations and fix SGR products"""
    import logging
    _logger = logging.getLogger(__name__)

    try:
        # Clear registry cache to ensure field overrides are applied
        _logger.info("Clearing registry cache to apply field overrides...")
        env.registry.clear_cache()
        _logger.info("Cache cleared successfully")

        # Get company fiscal settings
        company = env.company
        fiscal_integration_method = getattr(company, 'fiscal_integration_method', 'local_file') or 'local_file'
        fiscal_os_type = getattr(company, 'fiscal_os_type', 'android') or 'android'
        fiscal_api_endpoint = getattr(company, 'fiscal_api_endpoint', 'http://localhost:65400/api/Receipt') or 'http://localhost:65400/api/Receipt'

        # Update all existing POS configurations
        pos_configs = env['pos.config'].search([])
        for pos_config in pos_configs:
            if not getattr(pos_config, 'fiscal_integration_method', None):
                pos_config.fiscal_integration_method = fiscal_integration_method
            if not getattr(pos_config, 'fiscal_os_type', None):
                pos_config.fiscal_os_type = fiscal_os_type
            if not getattr(pos_config, 'fiscal_api_endpoint', None):
                pos_config.fiscal_api_endpoint = fiscal_api_endpoint

        # CRITICAL: Remove categories from ALL existing SGR products
        _logger.info("Fixing all existing SGR products...")
        sgr_products = env['product.product'].sudo().search([('name', '=', 'SGR')])
        sgr_templates = env['product.template'].sudo().search([
            '|', ('name', '=', 'SGR'), ('is_sgr', '=', True)
        ])

        if sgr_products or sgr_templates:
            _logger.info(f"Found {len(sgr_products)} SGR products and {len(sgr_templates)} SGR templates")

            # Use SQL to set category to NULL - most reliable method
            try:
                env.cr.execute("""
                    UPDATE product_template
                    SET categ_id = NULL, active = true
                    WHERE id IN (
                        SELECT product_tmpl_id
                        FROM product_product
                        WHERE name = 'SGR'
                    ) OR name = 'SGR' OR is_sgr = true
                """)
                env.cr.commit()
                _logger.info("✓ Successfully set category to NULL for all SGR products using SQL")
            except Exception as e:
                _logger.warning(f"SQL update failed, falling back to ORM: {e}")
                # Fallback to ORM
                all_sgr = sgr_products | sgr_templates
                all_sgr.write({'categ_id': False, 'active': True})
                _logger.info("✓ Successfully set category to empty for all SGR products using ORM")

        # Ensure all products available in POS are active
        pos_products = env['product.template'].search([
            ('available_in_pos', '=', True),
            ('active', '=', False)
        ])
        if pos_products:
            _logger.info(f"Found {len(pos_products)} inactive products available in POS, activating them")
            pos_products.write({'active': True})
            _logger.info("Successfully activated all products available in POS")

        # Clear cache again after all changes
        env.registry.clear_cache()

        _logger.info("✓ Post-init hook completed successfully - all fixes applied")

    except Exception as e:
        # Log error but don't fail the module installation
        _logger.error(f"Error in fiscal_cash_register post_init_hook: {e}")
        import traceback
        _logger.error(traceback.format_exc())

