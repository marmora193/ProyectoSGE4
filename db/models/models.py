#Mapeo de la BBDD con python
from sqlalchemy import (Column, Integer, String, Numeric, Date, ForeignKey, Boolean)
from sqlalchemy.orm import (declarative_base, relationship)


Base = declarative_base()

class Cliente(Base):
    __tablename__="cliente"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable = False)
    apellidos = Column(String(50), nullable=False)
    fecha_nac = Column(Date, nullable=False)
    dni = Column(String(9), unique=True, nullable=False)
    email = Column(String(100), nullable=False)
    nacionalidad = Column(String(50), nullable=False)
    telefono = Column(String(20), nullable=False)
    direccion = Column(String(100), nullable=False)
    activo = Column(Boolean, default=True)

    #Relación
    tasaciones = relationship("Tasacion", back_populates="cliente")

class VentaOro(Base):
    __tablename__ = "venta_oro"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(Date, unique=True, nullable=False)
    precio_kg = Column(Numeric(12, 2), nullable=False)

class Tasacion(Base):
    __tablename__ = "tasacion"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    fecha_tasacion = Column(Date, nullable=False)
    peso_gramos = Column(Numeric(10, 2), nullable=False)
    precio_oro_kg_en_fecha = Column(Numeric(12, 2), nullable=False)
    importe = Column(Numeric(12, 2), default=0)
    estado = Column(String(10), nullable=False)

    #Relación
    cliente = relationship("Cliente", back_populates="tasaciones")
