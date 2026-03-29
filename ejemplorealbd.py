import sqlite3

class GestorVendedores :
    def __init__ (self, db="negocio.db") :
        self.db = db
        self._crear_tabla()
        
    def crear_tabla(self) :
        with sqlite3.connect(self.db) as conn :
            conn.execute("""
                         CREATE TABLE IF NOT EXISTS vendedores (
                             id INTEGER PRIMARY KEY
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
    
    def
            