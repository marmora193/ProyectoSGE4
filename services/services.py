from db.config import session
from db.models.models import Cliente, VentaOro, Tasacion
from sqlalchemy import func
from datetime import date, timedelta
import random


class ClienteService:
    @staticmethod
    def crear_cliente(nombre, apellidos, fecha_nac, dni, email, nacionalidad, telefono, direccion):
        cliente = Cliente(
            nombre = nombre,
            apellidos = apellidos,
            fecha_nac = fecha_nac,
            dni = dni,
            email = email,
            nacionalidad = nacionalidad,
            telefono = telefono,
            direccion = direccion
        )

        session.add(cliente)
        session.commit()
        return cliente

    @staticmethod
    def listar_clientes():
        return session.query(Cliente).filter_by(activo=True).all()

    @staticmethod
    def buscar_por_dni(dni):
        return session.query(Cliente).filter_by(dni = dni).first()

    @staticmethod
    def mayor_edad(cliente):
        hoy = date.today()
        edad = hoy.year - cliente.fecha_nac.year - ((hoy.month, hoy.day) < (cliente.fecha_nac.month, cliente.fecha_nac.day))
        return edad >= 18

    @staticmethod
    def dar_baja(dni):
        cliente = ClienteService.buscar_por_dni(dni)
        if cliente:
            cliente.activo = False
            session.commit()
        return cliente

