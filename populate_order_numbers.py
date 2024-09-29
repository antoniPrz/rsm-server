from app import db, Repair, app  # Asegúrate de importar `app` desde tu aplicación principal
import datetime

# Ejecutar el código dentro del contexto de la aplicación
with app.app_context():
    # Obtener todos los registros de repairs que no tienen un `order_number`
    repairs_without_order_number = Repair.query.filter(Repair.order_number == None).all()

    # Actualizar cada registro con un número de orden generado
    for repair in repairs_without_order_number:
        # Generar un número de orden basado en la fecha y el id
        order_number = f"ORD-{datetime.datetime.now().strftime('%Y%m%d')}-{repair.id:03d}"
        
        repair.order_number = order_number
        db.session.add(repair)

    # Confirmar los cambios
    db.session.commit()

    print(f"Se actualizaron {len(repairs_without_order_number)} reparaciones con 'order_number'.")
