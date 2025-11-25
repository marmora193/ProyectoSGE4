#Mapeo de la BBDD con python
from sqlalchemy import (Column, Integer, String, Numeric, Date, ForeignKey, Boolean)
from sqlalchemy.orm import (declarative_base, relationship)


Base = declarative_base()

class Cliente(Base):
    __tablename__="CLIENTE"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    NOMBRE = Column(String(50), nullable = False)
    APELLIDOS = Column(String(50), nullable=False)
    FECHA_NAC = Column(Date, nullable=False)
    DNI = Column(String(9), unique=True, nullable=False)
    EMAIL = Column(String(100), nullable=False)
    NACIONALIDAD = Column(String(50), nullable=False)
    TELEFONO = Column(String(20), nullable=False)
    DIRECCION = Column(String(100), nullable=False)
    ACTIVO = Column(Boolean, default=True)

    #Relación
    tasaciones = relationship("Tasacion", back_populates="cliente")

class VentaOro(Base):
    __tablename__ = "VENTA_ORO"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    FECHA = Column(Date, unique=True, nullable=False)
    PRECIO_KG = Column(Numeric(12, 2), nullable=False)

class Tasacion(Base):
    __tablename__ = "TASACION"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    CLIENTE_ID = Column(Integer, ForeignKey("CLIENTE.ID"), nullable=False)
    FECHA_TASACION = Column(Date, nullable=False)
    PESO_GRAMOS = Column(Numeric(10, 2), nullable=False)
    PRECIO_ORO_KG_EN_FECHA = Column(Numeric(12, 2), nullable=False)
    IMPORTE = Column(Numeric(12, 2), default=0)
    ESTADO = Column(String(10), nullable=False)

    #Relación
    cliente = relationship("Cliente", back_populates="tasaciones")
