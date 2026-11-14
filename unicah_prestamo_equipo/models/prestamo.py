

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PrestamoEquipo(models.Model):
    _name = "unicah.prestamo.equipo"
    _description = "Préstamo de equipos universitarios"

    name = fields.Char(
        string="Código del préstamo",
        required=True,
        default="Nuevo",
    )

    solicitante_id = fields.Many2one(
        "res.partner",
        string="Solicitante",
        required=True,
    )

    equipo = fields.Char(
        string="Equipo",
        required=True,
    )

    fecha_prestamo = fields.Date(
        string="Fecha del préstamo",
        required=True,
        default=fields.Date.context_today,
    )

    fecha_devolucion = fields.Date(
        string="Fecha de devolución",
        required=True,
    )

    dias_prestamo = fields.Integer(
        string="Días de préstamo",
        compute="_compute_dias_prestamo",
        store=True,
    )

    estado = fields.Selection(
        [
            ("pendiente", "Pendiente"),
            ("prestado", "Prestado"),
            ("devuelto", "Devuelto"),
        ],
        string="Estado",
        default="pendiente",
        required=True,
    )

    @api.depends("fecha_prestamo", "fecha_devolucion")
    def _compute_dias_prestamo(self):
        for prestamo in self:
            if prestamo.fecha_prestamo and prestamo.fecha_devolucion:
                dias = (
                    prestamo.fecha_devolucion - prestamo.fecha_prestamo
                ).days
                prestamo.dias_prestamo = dias
            else:
                prestamo.dias_prestamo = 0

    @api.constrains("fecha_prestamo", "fecha_devolucion")
    def _check_fechas(self):
        for prestamo in self:
            if (
                prestamo.fecha_prestamo
                and prestamo.fecha_devolucion
                and prestamo.fecha_devolucion < prestamo.fecha_prestamo
            ):
                raise ValidationError(
                    "La fecha de devolución no puede ser anterior "
                    "a la fecha del préstamo."
                )


class ResPartner(models.Model):
    _inherit = "res.partner"

    es_responsable_equipo = fields.Boolean(
        string="Responsable de equipos"
    )
