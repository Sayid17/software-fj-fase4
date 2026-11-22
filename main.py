"""Demostración con más de diez operaciones válidas e inválidas."""
from pathlib import Path
from software_fj import (
    Cliente, ReservaSala, AlquilerEquipo, AsesoriaEspecializada,
    GestorSoftwareFJ, configure_logger
)

def main() -> None:
    logger = configure_logger(Path(__file__).parent / "logs" / "sistema.log")
    gestor = GestorSoftwareFJ(logger)
    print("\n=== SOFTWARE FJ | DEMOSTRACIÓN DE OPERACIONES ===\n")

    # 1. Cliente válido
    ana = gestor.ejecutar_seguro("1. Registrar cliente válido", Cliente, "C001", "Ana Torres", "ana@correo.com", "3001234567")
    if ana: gestor.ejecutar_seguro("1B. Guardar cliente válido", gestor.registrar_cliente, ana)

    # 2. Cliente con correo inválido
    gestor.ejecutar_seguro("2. Rechazar correo inválido", Cliente, "C002", "Luis Pérez", "correo-invalido", "3001112233")

    # 3. Cliente duplicado
    if ana: gestor.ejecutar_seguro("3. Rechazar cliente duplicado", gestor.registrar_cliente, ana)

    # 4. Servicio sala válido
    sala = gestor.ejecutar_seguro("4. Crear sala válida", ReservaSala, "S001", "Sala Innovación", 80000, 20)
    if sala: gestor.ejecutar_seguro("4B. Registrar sala", gestor.registrar_servicio, sala)

    # 5. Servicio equipo válido
    equipo = gestor.ejecutar_seguro("5. Crear alquiler de equipo", AlquilerEquipo, "S002", "Portátil de alto rendimiento", 120000, 250000)
    if equipo: gestor.ejecutar_seguro("5B. Registrar equipo", gestor.registrar_servicio, equipo)

    # 6. Asesoría válida
    asesoria = gestor.ejecutar_seguro("6. Crear asesoría", AsesoriaEspecializada, "S003", "Asesoría de arquitectura", 150000, "Arquitectura de software")
    if asesoria: gestor.ejecutar_seguro("6B. Registrar asesoría", gestor.registrar_servicio, asesoria)

    # 7. Servicio inválido
    gestor.ejecutar_seguro("7. Rechazar tarifa negativa", ReservaSala, "S004", "Sala defectuosa", -10, 5)

    # 8. Reserva válida
    reserva = gestor.ejecutar_seguro("8. Crear reserva válida", gestor.crear_reserva, "R001", "C001", "S001", 3)

    # 9. Procesar con descuento e impuesto (método con parámetros opcionales)
    if reserva:
        costo = gestor.ejecutar_seguro("9. Calcular costo con descuento", reserva.procesar, descuento=0.10, impuesto=0.19, asistentes=12)
        if costo is not None: print(f"    Costo calculado: ${costo}")

    # 10. Confirmar reserva
    if reserva: gestor.ejecutar_seguro("10. Confirmar reserva", reserva.confirmar)

    # 11. Cancelar reserva
    if reserva: gestor.ejecutar_seguro("11. Cancelar reserva", reserva.cancelar)

    # 12. Cancelación repetida
    if reserva: gestor.ejecutar_seguro("12. Rechazar segunda cancelación", reserva.cancelar)

    # 13. Cliente inexistente: demuestra encadenamiento de excepción
    gestor.ejecutar_seguro("13. Rechazar cliente inexistente", gestor.crear_reserva, "R002", "NO-EXISTE", "S001", 1)

    # 14. Duración negativa
    gestor.ejecutar_seguro("14. Rechazar duración negativa", gestor.crear_reserva, "R003", "C001", "S001", -2)

    # 15. Servicio no disponible
    if equipo:
        equipo.disponible = False
        gestor.ejecutar_seguro("15. Rechazar servicio no disponible", gestor.crear_reserva, "R004", "C001", "S002", 2)

    print("\nLa aplicación finalizó sin interrupciones.")
    print(f"Consulte el log en: {Path(__file__).parent / 'logs' / 'sistema.log'}")

if __name__ == "__main__":
    main()
