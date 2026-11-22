"""Gestor de colecciones y operaciones del sistema."""
from __future__ import annotations
import logging
from .models import Cliente, Servicio, Reserva
from .exceptions import DuplicateEntityError, EntityNotFoundError, SoftwareFJError, ValidationError

class GestorSoftwareFJ:
    def __init__(self, logger: logging.Logger) -> None:
        self.clientes: dict[str, Cliente] = {}
        self.servicios: dict[str, Servicio] = {}
        self.reservas: dict[str, Reserva] = {}
        self.logger = logger

    def registrar_cliente(self, cliente: Cliente) -> None:
        if cliente.identificador in self.clientes:
            raise DuplicateEntityError(f"Cliente duplicado: {cliente.identificador}")
        self.clientes[cliente.identificador] = cliente
        self.logger.info("Cliente registrado: %s", cliente.describir())

    def registrar_servicio(self, servicio: Servicio) -> None:
        if servicio.identificador in self.servicios:
            raise DuplicateEntityError(f"Servicio duplicado: {servicio.identificador}")
        self.servicios[servicio.identificador] = servicio
        self.logger.info("Servicio registrado: %s", servicio.describir())

    def crear_reserva(self, reserva_id: str, cliente_id: str, servicio_id: str, duracion: float) -> Reserva:
        try:
            cliente = self.clientes[cliente_id]
            servicio = self.servicios[servicio_id]
        except KeyError as exc:
            raise EntityNotFoundError(f"No existe la entidad requerida: {exc.args[0]}") from exc
        if reserva_id in self.reservas:
            raise DuplicateEntityError(f"Reserva duplicada: {reserva_id}")
        reserva = Reserva(reserva_id, cliente, servicio, duracion)
        self.reservas[reserva_id] = reserva
        self.logger.info("Reserva creada: %s", reserva.describir())
        return reserva

    def obtener_reserva(self, reserva_id: str) -> Reserva:
        try:
            return self.reservas[reserva_id]
        except KeyError as exc:
            raise EntityNotFoundError(f"Reserva inexistente: {reserva_id}") from exc

    def ejecutar_seguro(self, etiqueta: str, funcion, *args, **kwargs):
        """Ejecuta una operación sin detener la aplicación."""
        self.logger.info("INICIO | %s", etiqueta)
        try:
            resultado = funcion(*args, **kwargs)
        except SoftwareFJError as exc:
            self.logger.error("ERROR CONTROLADO | %s | %s", etiqueta, exc)
            print(f"[ERROR CONTROLADO] {etiqueta}: {exc}")
            return None
        except Exception as exc:
            self.logger.exception("ERROR INESPERADO | %s", etiqueta)
            print(f"[ERROR INESPERADO] {etiqueta}: {exc}")
            return None
        else:
            self.logger.info("ÉXITO | %s", etiqueta)
            print(f"[OK] {etiqueta}")
            return resultado
        finally:
            self.logger.info("FIN | %s", etiqueta)
