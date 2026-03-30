import sqlite3

with sqlite3.connect("negocio.db") as conn:
    cursor = conn.cursor()
    
    # Ejecutar consulta:
    cursor.execute("SELECT * FROM vendedores")
    
    # Obtener resultados:
    todos = cursor.fetchall()      # lista de tuplas con todos
    uno = cursor.fetchone()        # solo el primero
    algunos = cursor.fetchmany(3)  # los primeros 3
    
    # Recorrer:
    for fila in todos:
        print(fila)
        # (1, 'Patrick', 'Lima', 12000.0, 1)
    
    # Con parámetros:
    cursor.execute("SELECT * FROM vendedores WHERE region = ?", ("Lima",))
    limeños = cursor.fetchall()