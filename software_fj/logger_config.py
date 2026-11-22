"""Configuración central de registros del sistema."""
from __future__ import annotations
import logging
from pathlib import Path
from .exceptions import LogWriteError

LOGGER_NAME = "software_fj"

def configure_logger(log_file: str | Path = "logs/sistema.log") -> logging.Logger:
    """Crea un logger de archivo y consola sin duplicar manejadores."""
    try:
        path = Path(log_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        logger = logging.getLogger(LOGGER_NAME)
        logger.setLevel(logging.INFO)
        logger.propagate = False
        if not logger.handlers:
            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            file_handler = logging.FileHandler(path, encoding="utf-8")
            file_handler.setFormatter(formatter)
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
        return logger
    except OSError as exc:
        raise LogWriteError(f"No fue posible crear el log en {log_file}") from exc
