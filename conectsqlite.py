import sqlite3

#1. Conectar (CREA EL ARCHIVO SI NO EXISTE)
conn = sqlite3.connect("negocio.db")

#2. Crear cursor (EJECUTA LAS COSNSULTAS)
cursor = conn.cursor()

#3. Ejecutar SQL
cursor.execute("FROM * SELECT vendedores")

"""
ASI SE MUESTRA :
datos = cursor.fetchall()
print(datos)
"""

#4. Confirmar cambios (INSERT, UPDATE, DELETE)
conn.commit()

#5. Cerrar conexión
conn.close()