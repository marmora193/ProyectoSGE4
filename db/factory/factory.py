import configparser
import os

from faker import Faker
from db.config import session
from db.models.models import Usuario, Tasacion, Venta, Estado
from datetime import datetime, timedelta
import random

def bd_vacia():
    #Devolvemos True si no existe ningún usuario en la BD.
    return session.query(Usuario).count() == 0

fake = Faker("es_ES")

#Creamos 20 usuarios
def crear_usuarios(n=20):
    usuarios = []

    for _ in range(n):
        u = Usuario(
            nombre=fake.first_name(),
            apellidos=fake.last_name(),
            fecha_nac=fake.date_of_birth(minimum_age=18, maximum_age=90),
            dni=fake.unique.random_number(digits=8).__str__() + fake.random_letter().upper(),
            email=fake.email(),
            nacionalidad=fake.country(),
            telefono=fake.phone_number(),
            direccion=fake.address(),
            activo=True
        )
        usuarios.append(u)
        session.add(u)

    session.commit()
    return usuarios

#Creamos:
    #- 400 tasaciones aceptadas → generan venta
    #- 30 tasaciones rechazadas → generan venta con estado RECHAZADA
    #- 20 tasaciones pendientes → no generan venta
def crear_tasaciones_y_ventas(usuarios):

    estado_aceptada = session.query(Estado).filter_by(descripcion="ACEPTADA").first()
    estado_rechazada = session.query(Estado).filter_by(descripcion="RECHAZADA").first()
    estado_tasacion = session.query(Estado).filter_by(descripcion="TASACION").first()

    hoy = datetime.now()
    inicio=datetime(2025, 1, 1)
    dias_totales = (hoy - inicio).days

    #Creamos tasaciones aceptadas
    for _ in range(400):
        usuario = random.choice(usuarios)

        fecha = inicio + timedelta(days=random.randint(0, dias_totales))
        valor = 113000 * (1 + random.uniform(-0.03, 0.03))
        peso = random.uniform(1, 50)
        importe = valor * (peso / 1000)

        t = Tasacion(
            usuario_id=usuario.id,
            fecha=fecha,
            peso_gramos=peso,
            valor=valor,
            importe=importe
        )
        session.add(t)
        session.commit()

        v = Venta(
            usuario_id=usuario.id,
            estado_id=estado_aceptada.id,
            precio=importe,
            id_tasacion=t.id,
            gramos=peso
        )
        session.add(v)
        session.commit()

    #2. Creamos tasaciones rechazadas
    for _ in range(30):
        usuario = random.choice(usuarios)

        fecha = inicio + timedelta(days=random.randint(0, dias_totales))
        valor = 113000 * (1 + random.uniform(-0.03, 0.03))
        peso = random.uniform(1, 40)
        importe = valor * (peso / 1000)

        t = Tasacion(
            usuario_id=usuario.id,
            fecha=fecha,
            peso_gramos=peso,
            valor=valor,
            importe=importe
        )
        session.add(t)
        session.commit()

        v = Venta(
            usuario_id=usuario.id,
            estado_id=estado_rechazada.id,
            precio=importe,
            id_tasacion=t.id,
            gramos=peso
        )
        session.add(v)
        session.commit()

    #3. Creamos tasaciones pendientes (sin venta)
    for _ in range(20):
        usuario = random.choice(usuarios)

        fecha = inicio + timedelta(days=random.randint(0, dias_totales))
        valor = 113000 * (1 + random.uniform(-0.03, 0.03))
        peso = random.uniform(1, 60)
        importe = valor * (peso / 1000)

        t = Tasacion(
            usuario_id=usuario.id,
            fecha=fecha,
            peso_gramos=peso,
            valor=valor,
            importe=importe
        )
        session.add(t)
        session.commit()

        # Venta pendiente (estado TASACIÓN)
        v = Venta(
            usuario_id=usuario.id,
            estado_id=estado_tasacion.id,
            precio=importe,
            id_tasacion=t.id,
            gramos=peso
        )
        session.add(v)
        session.commit()


def cargar_datos_iniciales():
    #Cargamos la factoría completa si la BD está vacía.
    if not bd_vacia():
        print("BD con datos: Factoría no ejecutada.")
        return

    print("BD vacía: Generando datos iniciales...")

    usuarios = crear_usuarios()
    crear_tasaciones_y_ventas(usuarios)

    print("Factoría completada.")
