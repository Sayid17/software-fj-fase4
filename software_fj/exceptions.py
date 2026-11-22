"""Excepciones de dominio para Software FJ."""

class SoftwareFJError(Exception):
    """Excepción base del sistema."""

class ValidationError(SoftwareFJError):
    """Datos o parámetros inválidos."""

class DuplicateEntityError(SoftwareFJError):
    """Entidad duplicada en el gestor."""

class EntityNotFoundError(SoftwareFJError):
    """Entidad no encontrada."""

class ServiceUnavailableError(SoftwareFJError):
    """Servicio no disponible."""

class InvalidReservationStateError(SoftwareFJError):
    """Cambio de estado no permitido."""

class LogWriteError(SoftwareFJError):
    """No fue posible escribir en el archivo de log."""
