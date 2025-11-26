from db.config import session
from db.models.models import Usuario, Venta, Tasacion
from sqlalchemy import func
from datetime import date, timedelta
import random


class UsuarioService:
    @staticmethod
    def crear_usuario(nombre, apellidos, fecha_nac, dni, email, nacionalidad, telefono, direccion):

        #Validamos para que el dni no esté duplicado
        if UsuarioService.buscar_por_dni(dni):
            return None


        usuario = Usuario(
            nombre = nombre,
            apellidos = apellidos,
            fecha_nac = fecha_nac,
            dni = dni,
            email = email,
            nacionalidad = nacionalidad,
            telefono = telefono,
            direccion = direccion
        )

        session.add(usuario)
        session.commit()
        return usuario

    @staticmethod
    def listar_usuarios():
        return session.query(Usuario).filter_by(activo=True).all()

    @staticmethod
    def buscar_por_dni(dni):
        return session.query(Usuario).filter_by(dni = dni).first()

    @staticmethod
    def mayor_edad(usuario):
        #Evitamos que devuelva None para que no crashee la app
        if usuario.fecha_nac is None:
            return False

        hoy = date.today()
        edad = hoy.year - usuario.fecha_nac.year - ((hoy.month, hoy.day) < (usuario.fecha_nac.month, usuario.fecha_nac.day))
        return edad >= 18

    @staticmethod
    def dar_baja(dni):
        usuario = UsuarioService.buscar_por_dni(dni)
        if usuario:
            usuario.activo = False
            session.commit()
        return usuario

class VentaService:

    @staticmethod
    def get_precio_fecha(fecha:date):
        "Devuelve el precio del oro para una fecha concreta. Si no existe devuelve NONE."
        return session.query(Venta).filter_by(fecha=fecha).first()

    @staticmethod
    def generar_precio(fecha:date):
        "Genera un precio aleatorio entre -3% y +3% a partir del precio del día anterior."

        #Buscar el día anterior
