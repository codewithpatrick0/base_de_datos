import sqlite3

with sqlite3.connect("negocio.db") as conn :
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor() 
# Por defecto los resultados son tuplas → fila[0], fila[1]
# Con row_factory son diccionarios → fila["nombre"]
    cursor.execute("SELECT * FROM vendedores")
    for fila in cursor.fetchall() :
        print(fila["nombre", fila["ventas_totales"]])
        
    # Actualizar:
    cursor.execute("""
        UPDATE vendedores 
        SET ventas_totales = ? 
        WHERE nombre = ?
    """, (15000, "Patrick"))
    
    # Eliminar:
    cursor.execute("DELETE FROM vendedores WHERE activo = ?", (0,))
    
    conn.commit()
    print(f"Filas afectadas: {cursor.rowcount}")
