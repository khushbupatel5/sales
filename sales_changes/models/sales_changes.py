from odoo import fields, models, api


class SaleChanges(models.TransientModel):
    _inherit = 'res.config.settings'

    merge_sale_order_lines = fields.Boolean(string='Merge Order Lines',
                                            help="If enabled, merge all sale order lines containing the same product.")


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    def create(self, vals):
        if self.env['ir.config_parameter'].sudo().get_param('sales_changes.merge_sale_order_lines'):
            existing_line = self.search(
                [('order_id', '=', vals.get('order_id')), ('product_id', '=', vals.get('product_id'))])
            if existing_line:
                existing_line.write(
                    {'product_uom_qty': existing_line.product_uom_qty + vals.get('product_uom_qty')})
                return existing_line
        return super(SaleOrderLine, self).create(vals)




    # def set_values(self):
    #     super(SaleChanges, self).set_values()
    #     config_parameter = self.env['ir.config_parameter'].sudo()
    #     config_parameter.set_param('sales_changes.merge_sale_order_lines', self.merge_sale_order_lines)
    #
    # @api.model
    # def get_values(self):
    #     res = super(SaleChanges, self).get_values()
    #     merge_sale_order_lines = self.env['ir.config_parameter'].sudo().get_param('sales_changes.merge_sale_order_lines')
    #     res.update(
    #         merge_sale_order_lines=merge_sale_order_lines,
    #     )
    #     return res


