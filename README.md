# Software FJ - Fase 4

Sistema orientado a objetos para gestionar clientes, servicios y reservas sin base de datos.

## Requisitos
- Python 3.12 o superior.
- No requiere paquetes externos.

## Ejecución
```bash
python main.py
```

## Pruebas
```bash
python -m unittest discover -s tests -v
```

## Funcionalidades
- Abstracción mediante `Entidad` y `Servicio`.
- Encapsulación y validaciones en `Cliente`.
- Herencia y polimorfismo con `ReservaSala`, `AlquilerEquipo` y `AsesoriaEspecializada`.
- Parámetros opcionales para impuestos, descuentos, depósitos y urgencia.
- Excepciones personalizadas, encadenamiento y bloques `try/except/else/finally`.
- Registro en `logs/sistema.log`.
- Quince operaciones válidas e inválidas sin interrumpir la aplicación.

## Integrantes
- Yulian Sayid Mendoza Figueroa
