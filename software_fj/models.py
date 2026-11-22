"""Entidades y servicios del sistema Software FJ."""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
import re
from .exceptions import ValidationError, ServiceUnavailableError, InvalidReservationStateError

MONEY = Decimal("0.01")

def money(value: Decimal | int | float | str) -> Decimal:
    return Decimal(str(value)).quantize(MONEY, rounding=ROUND_HALF_UP)

class Entidad(ABC):
    """Clase abstracta para entidades identificables."""
    def __init__(self, identificador: str) -> None:
        if not isinstance(identificador, str) or not identificador.strip():
            raise ValidationError("El identificador es obligatorio.")
        self._identificador = identificador.strip()

    @property
    def identificador(self) -> str:
        return self._identificador

    @abstractmethod
    def describir(self) -> str:
        raise NotImplementedError

class Cliente(Entidad):
    EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
    def __init__(self, identificador: str, nombre: str, email: str, telefono: str) -> None:
        super().__init__(identificador)
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

    @property
    def nombre(self) -> str: return self._nombre
    @nombre.setter
    def nombre(self, value: str) -> None:
        if not isinstance(value, str) or len(value.strip()) < 3:
            raise ValidationError("El nombre debe tener al menos 3 caracteres.")
        self._nombre = value.strip()

    @property
    def email(self) -> str: return self._email
    @email.setter
    def email(self, value: str) -> None:
        if not isinstance(value, str) or not self.EMAIL_RE.fullmatch(value.strip()):
            raise ValidationError("El correo electrónico no es válido.")
        self._email = value.strip().lower()

    @property
    def telefono(self) -> str: return self._telefono
    @telefono.setter
    def telefono(self, value: str) -> None:
        cleaned = re.sub(r"[\s+-]", "", str(value))
        if not cleaned.isdigit() or not 7 <= len(cleaned) <= 15:
            raise ValidationError("El teléfono debe contener entre 7 y 15 dígitos.")
        self._telefono = cleaned

    def describir(self) -> str:
        return f"Cliente {self.nombre} ({self.identificador}) - {self.email}"

class Servicio(Entidad, ABC):
    """Servicio abstracto con cálculo polimórfico de costo."""
    def __init__(self, identificador: str, nombre: str, tarifa_base: Decimal | int | float, disponible: bool = True) -> None:
        super().__init__(identificador)
        if not nombre or len(nombre.strip()) < 3:
            raise ValidationError("El nombre del servicio es inválido.")
        if money(tarifa_base) <= 0:
            raise ValidationError("La tarifa base debe ser mayor que cero.")
        self.nombre = nombre.strip()
        self.tarifa_base = money(tarifa_base)
        self.disponible = bool(disponible)

    def validar_disponibilidad(self) -> None:
        if not self.disponible:
            raise ServiceUnavailableError(f"El servicio {self.nombre} no está disponible.")

    @abstractmethod
    def calcular_costo(self, duracion: float, descuento: float = 0, impuesto: float = 0.19, **kwargs) -> Decimal:
        raise NotImplementedError

    def _ajustar(self, subtotal: Decimal, descuento: float, impuesto: float) -> Decimal:
        if not 0 <= descuento <= 1:
            raise ValidationError("El descuento debe estar entre 0 y 1.")
        if not 0 <= impuesto <= 1:
            raise ValidationError("El impuesto debe estar entre 0 y 1.")
        return money(subtotal * (Decimal("1") - Decimal(str(descuento))) * (Decimal("1") + Decimal(str(impuesto))))

class ReservaSala(Servicio):
    def __init__(self, identificador: str, nombre: str, tarifa_hora: Decimal | int | float, capacidad: int, disponible: bool = True) -> None:
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if capacidad <= 0: raise ValidationError("La capacidad debe ser positiva.")
        self.capacidad = capacidad

    def calcular_costo(self, duracion: float, descuento: float = 0, impuesto: float = 0.19, **kwargs) -> Decimal:
        self.validar_disponibilidad()
        if duracion <= 0: raise ValidationError("La duración debe ser mayor que cero.")
        asistentes = int(kwargs.get("asistentes", 1))
        if asistentes <= 0 or asistentes > self.capacidad:
            raise ValidationError(f"Asistentes fuera del rango 1-{self.capacidad}.")
        return self._ajustar(self.tarifa_base * Decimal(str(duracion)), descuento, impuesto)

    def describir(self) -> str:
        return f"Sala {self.nombre}, capacidad {self.capacidad}, tarifa/hora ${self.tarifa_base}"

class AlquilerEquipo(Servicio):
    def __init__(self, identificador: str, nombre: str, tarifa_dia: Decimal | int | float, deposito: Decimal | int | float, disponible: bool = True) -> None:
        super().__init__(identificador, nombre, tarifa_dia, disponible)
        if money(deposito) < 0: raise ValidationError("El depósito no puede ser negativo.")
        self.deposito = money(deposito)

    def calcular_costo(self, duracion: float, descuento: float = 0, impuesto: float = 0.19, **kwargs) -> Decimal:
        self.validar_disponibilidad()
        if duracion <= 0 or int(duracion) != duracion:
            raise ValidationError("El alquiler debe expresarse en días enteros positivos.")
        incluir_deposito = bool(kwargs.get("incluir_deposito", True))
        subtotal = self.tarifa_base * Decimal(str(int(duracion)))
        total = self._ajustar(subtotal, descuento, impuesto)
        return money(total + (self.deposito if incluir_deposito else Decimal("0")))

    def describir(self) -> str:
        return f"Equipo {self.nombre}, tarifa/día ${self.tarifa_base}, depósito ${self.deposito}"

class AsesoriaEspecializada(Servicio):
    def __init__(self, identificador: str, nombre: str, tarifa_hora: Decimal | int | float, especialidad: str, disponible: bool = True) -> None:
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if not especialidad.strip(): raise ValidationError("La especialidad es obligatoria.")
        self.especialidad = especialidad.strip()

    def calcular_costo(self, duracion: float, descuento: float = 0, impuesto: float = 0.19, **kwargs) -> Decimal:
        self.validar_disponibilidad()
        if duracion <= 0: raise ValidationError("La duración debe ser mayor que cero.")
        urgencia = bool(kwargs.get("urgencia", False))
        factor = Decimal("1.25") if urgencia else Decimal("1")
        return self._ajustar(self.tarifa_base * Decimal(str(duracion)) * factor, descuento, impuesto)

    def describir(self) -> str:
        return f"Asesoría {self.especialidad}, tarifa/hora ${self.tarifa_base}"

@dataclass
class Reserva:
    identificador: str
    cliente: Cliente
    servicio: Servicio
    duracion: float
    estado: str = "PENDIENTE"
    costo: Decimal | None = None
    creada_en: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        if not self.identificador.strip(): raise ValidationError("El identificador de reserva es obligatorio.")
        if self.duracion <= 0: raise ValidationError("La duración debe ser mayor que cero.")
        self.servicio.validar_disponibilidad()

    def procesar(self, descuento: float = 0, impuesto: float = 0.19, **kwargs) -> Decimal:
        if self.estado == "CANCELADA":
            raise InvalidReservationStateError("No se puede procesar una reserva cancelada.")
        self.costo = self.servicio.calcular_costo(self.duracion, descuento, impuesto, **kwargs)
        return self.costo

    def confirmar(self) -> None:
        if self.estado != "PENDIENTE":
            raise InvalidReservationStateError(f"Solo se confirma una reserva PENDIENTE; estado actual: {self.estado}.")
        if self.costo is None:
            raise InvalidReservationStateError("La reserva debe procesarse antes de confirmarse.")
        self.estado = "CONFIRMADA"

    def cancelar(self) -> None:
        if self.estado == "CANCELADA":
            raise InvalidReservationStateError("La reserva ya fue cancelada.")
        self.estado = "CANCELADA"

    def describir(self) -> str:
        return f"Reserva {self.identificador}: {self.cliente.nombre} / {self.servicio.nombre} / {self.estado}"
