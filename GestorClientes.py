import sqlite3

class GestorClientes :
    def __init__ (self, db = "clientes.db") :
        self.db = db
        self._crear_tabla()
        
    def _crear_tabla(self) :
        with sqlite3.connect(self.db) as conn :
            conn.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    ciudad TEXT DEFAULT 'NO CONOCIDO',
                    saldo REAL DEFAULT 0,
                    activo INTEGER DEFAULT 1
                )
                    """)
    
    def agregar(self, nombre, ciudad, saldo=0, activo=1) :
        with sqlite3.connect(self.db) as conn :
            conn.execute("""
                INSERT INTO clientes(nombre, ciudad, saldo, activo)
                VALUES (?, ?, ?, ?)
                         """, (nombre, ciudad, saldo, activo))
        print(f"CLIENTE {nombre} AÑADIDO CORRECTAMENTE")
        
    def obtener_todos(self) :
        with sqlite3.connect(self.db) as conn :
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM clientes")
            return cursor.fetchall()
        
    def buscar(self, nombre) :
        with sqlite3.connect(self.db) as conn :
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(" SELECT * FROM clientes WHERE nombre = ?", (nombre,))
            resultados = cursor.fetchone()
            if resultados :
                print(f"Cliente {nombre} :")
                print(f"Ciudad : {resultados['ciudad']}")
                print(f"Saldo : {resultados['saldo']}")
                return resultados
            else :
                print(f"No hay registros con el nombre {nombre}")
                return []
    
    def depositar(self, nombre, saldo) :
        if saldo <= 0 :
            print("Saldo de depósito inválido")
            return
            
        with sqlite3.connect(self.db) as conn :
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT saldo FROM clientes WHERE nombre = ?", (nombre,))
            fila = cursor.fetchone()
            
            if fila is None :
                print(f"Error: El cliente {nombre} no existe.")
                return
            
            conn.execute("UPDATE clientes SET saldo = saldo + ? WHERE nombre = ?", (saldo, nombre))
                
            nuevo_saldo = fila['saldo'] + saldo
            print(f"Saldo de {nombre} actualizado correctamente")
            print(f"Nuevo saldo : {nuevo_saldo:,.2f}")
            
    def retirar(self, nombre, monto) :
        if monto <= 0:
            print("Monto de retiro inválido")
            return
        
        with sqlite3.connect(self.db) as conn :
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT saldo FROM clientes WHERE nombre = ?", (nombre,))
            #.fetchone() retorna un solo resultado, en este caso estoy consultando saldo por un nombre en especifico
            fila = cursor.fetchone()
            
            if fila is None :
                print(f"Error: El cliente {nombre} no existe.")
                return
            
            saldo_actual = fila['saldo']
            
            if monto > saldo_actual :
                print(f"{nombre}, no tienes suficiente saldo. Saldo actual: S/ {saldo_actual}")
                return
            
            conn.execute("UPDATE clientes SET saldo = saldo - ? WHERE nombre = ?", (monto, nombre))
        
            nuevo_saldo = saldo_actual - monto
            print(f"Retiro exitoso de {nombre} de S/ {monto}. Nuevo saldo: S/ {nuevo_saldo:.2f}")
            
    def desactivar(self, nombre) :
        with sqlite3.connect(self.db) as conn :
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT activo FROM clientes WHERE nombre = ?", (nombre,))
            fila = cursor.fetchone()
            
            if fila is None:
                print(f"El cliente {nombre} no existe")
                return
            
            if fila['activo'] == 0 :
                print(f"El cliente {nombre} ya se encuentra inactivo")
                return
                
            conn.execute("UPDATE clientes SET activo = 0 WHERE nombre = ?", (nombre,))
            print(f"Cliente {nombre} desactivado correctamente")
    
    def reporte(self) :
        with sqlite3.connect(self.db) as conn :
            conn.row_factory = sqlite3.Row  
            cursor = conn.execute("""SELECT 
                                  COUNT(*) AS total_clientes,
                                  SUM(saldo) AS saldo_total,
                                  AVG(saldo) AS saldo_promedio
                                  FROM clientes
                                  """)
            resumen = cursor.fetchone()
            
            if resumen['total_clientes'] == 0:
                print("No hay clientes registrados para generar el reporte.")
                return
            
            print("--- REPORTE GENERAL ---")
            print(f"Total de clientes : {resumen['total_clientes']}")
            print(f"Saldo acumulado   : S/ {resumen['saldo_total']:,.2f}")
            print(f"Promedio de saldo : S/ {resumen['saldo_promedio']:,.2f}")
            print("-----------------------") 
            
gestor = GestorClientes()
gestor.agregar("Marianella", "Lima", 2099.89)
gestor.agregar("Patrick", "Arequipa", 4999.65, 0)
gestor.agregar("Fabian", "Callao", 615.5, 0)   
gestor.agregar("Alison", "Tarapoto", 599.89)

for c in gestor.obtener_todos() :
    print(f"{c['nombre']} | {c['ciudad']} | {c['saldo']}")
    
gestor.buscar("Patrick")
gestor.depositar("Marianella", 200.5)
gestor.retirar("Alison", 200.8)
gestor.desactivar("Alison")

gestor.reporte()