from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import DeclarativeBase, Session

# 1. Motor — conecta con la BD:
engine = create_engine("sqlite:///negocio.db")

# 2. Base — clase padre de todos tus modelos:
class Base(DeclarativeBase):
    pass

# 3. Modelo — cada clase = una tabla:
class Cliente(Base):
    __tablename__ = "clientes" #DEFINE NOMBRE DE LA TABLA
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    ciudad = Column(String, default='No conocido')
    saldo = Column(Float, default=0)
    activo = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"Cliente({self.nombre} | {self.ciudad} | S/{self.saldo:,.2f})"

Base.metadata.create_all(engine)

#SESSION (EQUIVALENTE A CURSOR)
with Session(engine) as session :
    todos = session.query(Cliente).all()
    
    #FILTRAR
    limeños = session.query(Cliente).filter(Cliente.ciudad == "Lima").all()
    
    #UNO SOLO
    uno = session.query(Cliente).filter(Cliente.nombre == "Patrick").first()
    
    #ORDENADO
    por_saldo = session.query(Cliente).order_by(Cliente.saldo.desc()).all()
    
with Session(engine) as session :
    cliente = session.query(Cliente).filter(Cliente.nombre == "Mari").first()
    
    if cliente :
        cliente += 500.2
        session.commit()
        
with Session(engine) as session:
    cliente = session.query(Cliente).filter(Cliente.nombre == "Patrick").first()
    if cliente:
        session.delete(cliente)
        session.commit()
    