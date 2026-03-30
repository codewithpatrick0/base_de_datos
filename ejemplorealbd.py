import sqlite3

class GestorVendedores :
    def __init__ (self, db="negocio.db") :
        self.db = db
        self._crear_tabla()
        
    def _crear_tabla(self) :
        with sqlite3.connect(self.db) as conn :
            conn.execute("""
                         CREATE TABLE IF NOT EXISTS vendedores (
                             id INTEGER PRIMARY KEY,
                             nombre TEXT NOT NULL,
                            region TEXT,
                            ventas_totales REAL DEFAULT 0,
                            activo INTEGER DEFAULT 1
                             )
                        """)
    def agregar(self, nombre, region, ventas=0) :
        with sqlite3.connect(self.db) as conn :
            conn.execute("""
                         INSERT INTO vendedores (nombre, region, ventas_totales)
                         VALUES (?, ?, ?)
                         """, (nombre, region, ventas))
        print("AGREGADO CORRECTAMENTE")
        
    def obtener_todos(self) :
        with sqlite3.connect(self.db) as conn :
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM vendedores")
            return cursor.fetchall()
    
    def obtener_por_region(self, region) :
        with sqlite3.connect(self.db) as conn :
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM vendedores WHERE region = ?", (region,))
            return cursor.fetchall()    
    
    def actualizar_ventas(self, nombre, nuevas_ventas) :
        with sqlite3.connect(self.db) as conn :
            conn.execute("""
                UPDATE vendedores SET ventas_totales = ?
                WHERE nombre = ?
                         """, (nuevas_ventas,  nombre))
        print(f"Ventas de {nombre} actualizadas correctamente")
        
    def eliminar(self, nombre) :
        with sqlite3.connect(self.db) as conn :
            conn.execute("""
                DELETE FROM vendedores WHERE nombre = ?
                         """, (nombre))
        print(f"{nombre} eliminado.")

#USAR
gestor = GestorVendedores()
gestor.agregar("Patrick", "Lima", 12000)
gestor.agregar("Ana", "Lima", 15000)
gestor.agregar("Luis", "Cusco", 8000)

for v in gestor.obtener_todos():
    print(f"{v['nombre']} | {v['region']} | S/ {v['ventas_totales']:,.2f}")