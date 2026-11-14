
monto_ahorro = fields.Monetary(
    string="Ahorro por convenio",
    compute="_compute_monto_ahorro",
    store=True,
    currency_field="currency_id",
)

# TODO 1: indicar los campos que usa el cálculo
@api.depends(
    "order_line.price_unit",
    "order_line.product_uom_qty",
    "order_line.discount",
)
def _compute_monto_ahorro(self):
    for order in self:
        # TODO 2: calcular el ahorro de las líneas de producto
        order.monto_ahorro = sum(
            line.price_unit
            * line.product_uom_qty
            * line.discount / 100
            for line in order.order_line
        )
