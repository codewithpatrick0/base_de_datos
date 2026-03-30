import sqlite3

with sqlite3.connect("negocio.db") as conn :
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS vendedores(
                       id INTEGER PRIMARY KEY 
                       nombre TEXT NOT NULL
                       region TEXT
                       ventas_totales REAL DEFAULT 0
                       activo INTEGER DEFAULT 1
                       )
                """)
    conn.commit()
    print("Tabla creada correctamente")
    
    cursor.execute("""
                   INSERT INTO vendedores (nombre, region, ventas_totales)
                   VALUES(?, ?, ?) 
                   """, ("Patrick", "Lima", 2099.99)) #(?) Placeholders que luego se llenan con los datos de fuera
    vendedores = [
        ("Luis", "Cusco", 8000),
        ("Ana", "Lima", 15000),
        ("María", "Arequipa", 7000),
    ]
    
    cursor.executemany("""
                   INSERT INTO vendedores (nombre, region, ventas_totales)
                   VALUES (?, ?, ?)
                   """, vendedores)
    conn.commit()
    
