#Mapeo de la BBDD con python
from sqlalchemy import (Column, Integer, String, Numeric, Date, ForeignKey, Boolean)
from sqlalchemy.orm import (declarative_base, relationship)


Base = declarative_base()

class Usuario(Base):
    __tablename__="usuario"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable = False)
    apellidos = Column(String(100))
    fecha_nac = Column(Date)
    dni = Column(String(9), unique=True)
    email = Column(String(100))
    nacionalidad = Column(String(50))
    telefono = Column(String(20))
    direccion = Column(String(100))
    activo = Column(Boolean, default=True)

    #Relación
    tasaciones = relationship("Tasacion", back_populates="usuario")
    ventas = relationship("Venta", back_populates="usuario")


class Estado(Base):
    __tablename__ = "estado"

    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String(20), nullable=False, unique=True)

    # Relación
    ventas = relationship("Venta", back_populates="estado")

class Tasacion(Base):
    __tablename__ = "tasacion"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    fecha = Column(Date, nullable=False)
    peso_gramos = Column(Numeric(10, 2), nullable=False)
    valor = Column(Numeric(12,2),nullable=False)
    importe = Column(Numeric(12, 2), default=0)

    #Relación
    usuario = relationship("Usuario", back_populates="tasaciones")
    ventas = relationship("Venta", back_populates="tasacion")

class Venta(Base):
    __tablename__ = "venta"


    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    estado_id = Column(Integer, ForeignKey("estado.id"), nullable=False)
    precio = Column(Numeric(12, 2), nullable=False)
    id_tasacion = Column(Integer, ForeignKey("tasacion.id"), nullable=False)
    gramos = Column(Numeric(10, 2), nullable=False)

    # Relación
    usuario = relationship("Usuario", back_populates="ventas")
    estado = relationship("Estado", back_populates="ventas")
    tasacion = relationship("Tasacion", back_populates="ventas")