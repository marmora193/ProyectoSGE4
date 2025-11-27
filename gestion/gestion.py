import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from db.config import session
from db.models.models import Venta, Usuario, Tasacion, Estado



class Gestion:
    @staticmethod
    def ventas_por_mes():
        mes = input("Introduce mes (MM/YYYY): ")

        try:
            fecha = datetime.strptime(mes, "%m/%Y")
        except:
            print("Formato de fecha incorrecto.")
            return

        inicio = fecha.replace(day=1)
        if fecha.month == 12:
            fin = fecha.replace(year=fecha.year + 1, month=1, day=1)
        else:
            fin = fecha.replace(month=fecha.month + 1, day=1)

        ventas = (session.query(Venta).join(Tasacion, Venta.id_tasacion == Tasacion.id).filter(Tasacion.fecha >= inicio)
                  .filter(Tasacion.fecha < fin).all())

        if ventas:
            print(f"\nVentas del mes {mes}:")
            for v in ventas:
                print(f"- Venta {v.id}: {v.precio}€  (Tasación {v.id_tasacion})")
        else:
            print(f"No hay ventas en {mes}.")


    @staticmethod
    def ventas_por_cliente():
        dni = input("Introduce el DNI del cliente: ")

        usuario = session.query(Usuario).filter_by(dni=dni).first()
        if not usuario:
            print("No existe un usuario con ese DNI.")
            return

        ventas = session.query(Venta).filter_by(usuario_id=usuario.id).all()

        print(f"\nVentas realizadas por {usuario.nombre} {usuario.apellidos}:")

        if ventas:
            for v in ventas:
                print(f"- Venta {v.id} | Precio: {v.precio}€ | Tasación {v.id_tasacion}")
        else:
            print("Este cliente no tiene ventas registradas.")


    @staticmethod
    def tasaciones_no_aceptadas():
        ids_resueltas = [v.id_tasacion for v in session.query(Venta).all()]

        tasaciones = session.query(Tasacion).filter(~Tasacion.id.in_(ids_resueltas)).all()

        print("\nTasaciones pendientes:\n")

        if tasaciones:
            for t in tasaciones:
                print(f"- Tasación {t.id}: {t.peso_gramos} g | Usuario ID {t.usuario_id}")
        else:
            print("No hay tasaciones pendientes.")

        print("\nTasaciones no aceptadas:\n")


    @staticmethod
    def cliente_con_mas_ventas():
        ventas = session.query(Venta).all()

        if not ventas:
            print("No hay ventas registradas.")
            return

        conteo = {}

        for v in ventas:
            if v.usuario_id not in conteo:
                conteo[v.usuario_id] = 0
            conteo[v.usuario_id] += 1

        usuario_id = max(conteo, key=conteo.get)
        usuario = session.query(Usuario).get(usuario_id)

        print("\nCliente con más ventas:\n")
        print(f"{usuario.nombre} {usuario.apellidos} (DNI: {usuario.dni})")
        print(f"Total de ventas: {conteo[usuario_id]}")


    @staticmethod
    def clientes_inactivos_3_meses():
        @staticmethod
        def clientes_inactivos_3_meses():
            hoy = datetime.now()
            limite = hoy - timedelta(days=90)

            usuarios = session.query(Usuario).all()
            inactivos = []

            for u in usuarios:
                ventas_usuario = session.query(Venta).filter_by(usuario_id=u.id).all()

                if not ventas_usuario:
                    inactivos.append(u)
                    continue

                fechas = []
                for v in ventas_usuario:
                    tasacion = session.query(Tasacion).filter_by(id=v.id_tasacion).first()
                    if tasacion:
                        fechas.append(tasacion.fecha)

                if not fechas or max(fechas) < limite:
                    inactivos.append(u)

            print("\nClientes inactivos (últimos 3 meses):\n")

            if inactivos:
                for u in inactivos:
                    print(f"- {u.nombre} {u.apellidos} | DNI: {u.dni}")
            else:
                print("Todos los clientes han realizado ventas recientes.")

class Graficos:

    #Creamos una carpeta gráficos para guardarlos
    ruta_graficos = "graficos"
    if not os.path.exists(ruta_graficos):
        os.makedirs(ruta_graficos)

    @staticmethod
    def oro_por_cliente():
        ventas = session.query(Venta).all()

        if not ventas:
            print("No hay ventas registradas.")
            return

        acumulado = {}

        for v in ventas:
            usuario = session.query(Usuario).get(v.usuario_id)
            if usuario:
                nombre = f"{usuario.nombre} {usuario.apellidos}"
                if nombre not in acumulado:
                    acumulado[nombre] = 0
                acumulado[nombre] += float(v.gramos)

        nombres = list(acumulado.keys())
        gramos = list(acumulado.values())

        plt.figure(figsize=(10, 6))
        plt.barh(nombres, gramos, color="gold")
        plt.title("Cantidad de oro vendido por cliente (gramos)")
        plt.xlabel("Gramos vendidos")
        plt.ylabel("Clientes")

        ruta = os.path.join(Graficos.ruta_graficos, "oro_por_cliente.png")
        plt.savefig(ruta)
        print(f"Gráfico guardado en: {ruta}")

        plt.show()
        plt.close()

    @staticmethod
    def importe_por_cliente():
        ventas = session.query(Venta).all()

        if not ventas:
            print("No hay ventas registradas.")
            return

        acumulado = {}

        for v in ventas:
            usuario = session.query(Usuario).get(v.usuario_id)
            if usuario:
                nombre = f"{usuario.nombre} {usuario.apellidos}"
                if nombre not in acumulado:
                    acumulado[nombre] = 0
                acumulado[nombre] += float(v.precio)

        nombres = list(acumulado.keys())
        importes = list(acumulado.values())

        plt.figure(figsize=(10, 6))
        plt.bar(nombres, importes, color="green")
        plt.title("Importe total vendido por cliente (€)")
        plt.xlabel("Clientes")
        plt.ylabel("Importe (€)")
        plt.xticks(rotation=45)

        ruta = os.path.join(Graficos.ruta_graficos, "importe_por_cliente.png")
        plt.savefig(ruta)
        print(f"Gráfico guardado en: {ruta}")

        plt.show()
        plt.close()

    @staticmethod
    def tasaciones_por_estado():
        # Tasaciones pendientes: las que NO están en venta
        tasaciones_ids = [t.id for t in session.query(Tasacion).all()]
        ventas_ids = [v.id_tasacion for v in session.query(Venta).all()]

        #Contamos las tasaciones que no tienen una venta asociada
        pendientes = len([t_id for t_id in tasaciones_ids if t_id not in ventas_ids])

        aceptadas = session.query(Venta).filter_by(estado_id=2).count()
        rechazadas = session.query(Venta).filter_by(estado_id=3).count()

        labels = ["Pendientes", "Aceptadas", "Rechazadas"]
        valores = [pendientes, aceptadas, rechazadas]
        colores = ["orange", "green", "red"]

        plt.figure(figsize=(8, 8))
        plt.pie(valores, labels=labels, autopct="%1.1f%%", colors=colores)
        plt.title("Distribución de tasaciones por estado")

        ruta = os.path.join(Graficos.ruta_graficos, "tasaciones_por_estado.png")
        plt.savefig(ruta)
        print(f"Gráfico guardado en: {ruta}")

        plt.show()
        plt.close()

    @staticmethod
    def ventas_por_mes():
        ventas = (session.query(Venta).join(Tasacion, Venta.id_tasacion == Tasacion.id).all())

        if not ventas:
            print("No hay ventas registradas.")
            return

        conteo_mensual = {}

        for v in ventas:
            tas = session.query(Tasacion).filter_by(id=v.id_tasacion).first()
            mes = tas.fecha.strftime("%m/%Y")  # formato MM/YYYY

            if mes not in conteo_mensual:
                conteo_mensual[mes] = 0
            conteo_mensual[mes] += 1

        meses = sorted(list(conteo_mensual.keys()))
        cantidades = list(conteo_mensual.values())

        plt.figure(figsize=(10, 6))
        plt.plot(meses, cantidades, marker="o", color="blue")
        plt.title("Ventas por mes")
        plt.xlabel("Mes")
        plt.ylabel("Cantidad de ventas")
        plt.xticks(rotation=45)

        ruta = os.path.join(Graficos.ruta_graficos, "ventas_por_mes.png")
        plt.savefig(ruta)
        print(f"Gráfico guardado en: {ruta}")

        plt.show()
        plt.close()