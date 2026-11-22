import logging
import unittest
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory

from software_fj import (
    Cliente,
    ReservaSala,
    GestorSoftwareFJ,
    configure_logger,
)
from software_fj.exceptions import (
    ValidationError,
    InvalidReservationStateError,
)


class TestSoftwareFJ(unittest.TestCase):

    def setUp(self):
        self.tmp = TemporaryDirectory()
        logger = configure_logger(Path(self.tmp.name) / "test.log")

        self.g = GestorSoftwareFJ(logger)
        self.c = Cliente(
            "C1",
            "Cliente Prueba",
            "prueba@correo.com",
            "3001234567",
        )
        self.s = ReservaSala(
            "S1",
            "Sala Prueba",
            100,
            10,
        )

        self.g.registrar_cliente(self.c)
        self.g.registrar_servicio(self.s)

    def tearDown(self):
        # Cierra los manejadores antes de eliminar test.log en Windows.
        logger = logging.getLogger("software_fj")

        for handler in logger.handlers[:]:
            handler.flush()
            handler.close()
            logger.removeHandler(handler)

        self.tmp.cleanup()

    def test_email_invalido(self):
        with self.assertRaises(ValidationError):
            Cliente(
                "C2",
                "Nombre Prueba",
                "mal",
                "1234567",
            )

    def test_costo_sala(self):
        resultado = self.s.calcular_costo(
            2,
            descuento=0,
            impuesto=0,
        )
        self.assertEqual(resultado, Decimal("200.00"))

    def test_flujo_reserva(self):
        reserva = self.g.crear_reserva(
            "R1",
            "C1",
            "S1",
            2,
        )

        reserva.procesar(
            impuesto=0,
            asistentes=5,
        )
        reserva.confirmar()
        reserva.cancelar()

        self.assertEqual(reserva.estado, "CANCELADA")

        with self.assertRaises(InvalidReservationStateError):
            reserva.cancelar()


if __name__ == "__main__":
    unittest.main()