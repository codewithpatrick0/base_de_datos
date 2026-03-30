import sqlite3

#with cierra la conexion automaticamente
with sqlite3.connect("negocio.db") as conn :
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vendedores")
    resultados = cursor.fetchall()
    print(resultados)
    
#MAS LIMPIO Y EFICIENTE