from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, func
from sqlalchemy.orm import DeclarativeBase, sessionmaker

class Base(DeclarativeBase) :
    pass

engine = create_engine("sqlite:///clientes2.db")

Session = sessionmaker(bind=engine)

class Cliente(Base) :
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    ciudad = Column(String, default="Sin ciudad")
    saldo = Column(Float, default=0)
    activo = Column(Boolean, default=True)
    
#CREAR LAS TABLAS EN LA DB
Base.metadata.create_all(engine)


class GestorClientes :
    def __init__(self) :
        self.session = Session()
        
    def agregar(self, nombre, ciudad='No conocido', saldo=0, activo=True) :
        nuevo_cliente = Cliente(nombre=nombre, ciudad=ciudad, saldo=saldo, activo=activo)
        self.session.add(nuevo_cliente)
        self.session.commit()
        print(f"CLIENTE {nombre} AÑADIDO CORRECTAMENTE")
        
    def obtener_todos(self) :
        return self.session.query(Cliente).all()
    
    def buscar(self, nombre) :
        cliente = self.session.query(Cliente).filter_by(nombre=nombre).first()
        if cliente :
            print(f"Cliente: {cliente.nombre} | Ciudad: {cliente.ciudad} | Saldo: {cliente.saldo:,.2f}")
            return cliente
        print("No hay registros con ese nombre aún")
        return None
    
    def depositar(self, nombre, monto) :
        cliente = self.session.query(Cliente).filter_by(nombre = nombre).first()
        if cliente and monto > 0 :
            cliente.saldo += monto
            self.session.commit()
            print(f"Nuevo saldo de {nombre}: S/{cliente.saldo:,.2f}")
        else :
            print("Error en el depósito o ese cliente inexistente")
            
    def retirar(self, nombre, monto) :
        cliente = self.session.query(Cliente).filter_by(nombre = nombre).first()
        if cliente and monto <= cliente.saldo :
            cliente.saldo -=monto
            self.session.commit()
            print(f"Retiro exitoso. Nuevo saldo: {cliente.saldo}")
        else:
            print("Saldo insuficiente o monto inválido")
            
    def desactivar(self, nombre) :
        cliente = self.session.query(Cliente).filter_by(nombre = nombre).first()
        if cliente and cliente.activo :
            cliente.activo = False
            self.session.commit()
            print(f"Cliente {nombre} desactivado")
            
        else :
            print("El cliente no existe o ya está inactivo")
            
    def reporte(self) :
        total = self.session.query(func.count(Cliente.id)).scalar()
        if total == 0 :
            print("No hay datos a mostrar")
            return
        
        suma = self.session.query(func.sum(Cliente.saldo)).scalar()
        promedio = self.session.query(func.avg(Cliente.saldo)).scalar()
        
        print("--- REPORTE GENERAL ---")
        print(f"Total clientes: {total}")
        print(f"Saldo total: S/ {suma:,.2f}")
        print(f"Promedio: S/ {promedio:,.2f}")

# --- PRUEBAS ---
gestor = GestorClientes()
gestor.agregar("Marianella", "Lima", 2099.89)
gestor.agregar("Patrick", "Arequipa", 4999.65, False)

for c in gestor.obtener_todos():
    status = "Activo" if c.activo else "Inactivo"
    print(f"{c.nombre} | {c.ciudad} | S/ {c.saldo} | {status}")

gestor.reporte()
