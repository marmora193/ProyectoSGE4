from db.config import session
from db.models.models import Usuario, Venta, Tasacion, Estado
from datetime import date
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

class EstadoService:
    @staticmethod
    def buscar_por_id(id_estado):
        return session.query(Estado).filter_by(id=id_estado).first()

    @staticmethod
    def buscar_por_descripcion(descripcion):
        return session.query(Estado).filter_by(descripcion=descripcion.upper()).first()

class TasacionService:
    @staticmethod
    def obtener_precio_oro(fecha):
        precioBase = 113002
        random.seed(int(fecha.strftime("%Y%m%d")))
        # Usamos la fecha como semilla para que cada día tenga siempre
        # el mismo precio del oro, evitando valores distintos en cada ejecución.
        variacion = random.uniform(-0.03, 0.03)
        precio = precioBase * (1 + variacion)
        return round(precio, 2)

    @staticmethod
    def crear_tasacion(usuario_dni, peso_gramos):
        #Buscamos el usuario
        usuario = session.query(Usuario).filter_by(dni=usuario_dni).first()
        if not usuario:
            return None, "El usuario no existe"

        #Comprobamos que el usuario esté activo
        if not usuario.activo:
            return None, "El usuario está dado de baja."

        #Comprobamos que el usuario sea mayor de edad
        hoy = date.today()
        if usuario.fecha_nac is None:
            return None, "La fecha de nacimiento no está registrada"

        edad = hoy.year - usuario.fecha_nac.year - (
                (hoy.month, hoy.day) < (usuario.fecha_nac.month, usuario.fecha_nac.day)
        )
        if edad < 18:
            return None, "El usuario es menor de edad."

        #Obtenemos el precio del oro en el día
        precio_oro_dia = TasacionService.obtener_precio_oro(hoy)

        #Calculamos el importe
        importe = (peso_gramos / 1000) * precio_oro_dia

        #Creamos la tasación
        tasacion = Tasacion(
            usuario_id = usuario.id,
            fecha = hoy,
            peso_gramos = peso_gramos,
            valor = precio_oro_dia,
            importe = round(importe, 2)
        )

        session.add(tasacion)
        session.commit()

        return tasacion, "Tasación creada correctamente."

    @staticmethod
    def listar_tasaciones():
        tasaciones = session.query(Tasacion).all()
        resultado = []

        for t in tasaciones:
            resultado.append({
                "id": t.id,
                "dni": t.usuario.dni,
                "nombre": f"{t.usuario.nombre} {t.usuario.apellidos}",
                "peso": float(t.peso_gramos),
                "valor": float(t.valor),
                "importe": float(t.importe),
                "fecha": t.fecha
            })

        return resultado

    @staticmethod
    def obtener_tasacion_por_id(id_tasacion):
        tasacion = session.query(Tasacion).filter_by(id=id_tasacion).first()

        if tasacion is None:
            return None

        #Si existe una venta asociada, la tasación sigue en estado "TASACIÓN"
        if not tasacion.ventas:
            estado = "TASACION"
        else:
            estado = tasacion.ventas[0].estado.descripcion

        detalle = {
            "id": tasacion.id,
            "fecha": tasacion.fecha,
            "usuario": f"{tasacion.usuario.nombre} {tasacion.usuario.apellidos}",
            "dni": tasacion.usuario.dni,
            "peso": float(tasacion.peso_gramos),
            "valor": float(tasacion.valor),
            "importe": float(tasacion.importe),
            "estado": tasacion.ventas[0].estado.descripcion if tasacion.ventas else "PENDIENTE"
        }

        return detalle

    @staticmethod
    def obtener_resumen_tasaciones():
        tasaciones = session.query(Tasacion).all()
        resumen = []

        for t in tasaciones:
            resumen.append({
                "id": t.id,
                "dni": t.usuario.dni,
                "peso": float(t.peso_gramos),
                "valor": float(t.valor),
                "importe": float(t.importe)
            })
        return resumen

    @staticmethod
    def obtener_estadisticas_tasaciones():
        datos = TasacionService.listar_tasaciones()

        if not datos:
            print("No hay tasaciones registradas.")
            return None

        total = len(datos)
        peso_total = sum(t["peso"] for t in datos)
        importe_total = sum(t["importe"] for t in datos)
        precio_medio = round(importe_total / total, 2)

        mayor = max(datos, key=lambda x: x["importe"])
        menor = min(datos, key=lambda x: x["importe"])

        # Agrupar por usuario (usamos DNI)
        agrupado = {}
        for t in datos:
            dni = t["dni"]
            if dni not in agrupado:
                agrupado[dni] = 0
            agrupado[dni] += t["importe"]

        print("\n===== RESUMEN DE TASACIONES =====")
        print(f"Total de tasaciones: {total}")
        print(f"Peso total tasado: {peso_total} g")
        print(f"Importe total generado: {importe_total} €")
        print(f"Precio medio por tasación: {precio_medio} €")

        print(f"\nMayor tasación → {mayor['importe']} € (ID {mayor['id']}, DNI {mayor['dni']})")
        print(f"Menor tasación → {menor['importe']} € (ID {menor['id']}, DNI {menor['dni']})")

        print("\nImporte total por usuario:")
        for dni, valor in agrupado.items():
            print(f" - {dni}: {valor} €")

        print("=====================================\n")

        return {
            "total": total,
            "peso_total": peso_total,
            "importe_total": importe_total,
            "precio_medio": precio_medio,
            "mayor": mayor,
            "menor": menor,
            "agrupado": agrupado
        }


class VentaService:

    @staticmethod
    def aceptar_tasacion(id_tasacion):
        tasacion = session.query(Tasacion).filter_by(id=id_tasacion).first()

        if not tasacion:
            return None, "La tasación no existe."

        #Obtenemos el estado ACEPTADA
        estado_aceptada = session.query(Estado).filter_by(descripcion="ACEPTADA").first()


        #Si cambia de fecha recalculamos el precio y valor
        fecha_actual = date.today()

        if fecha_actual != tasacion.fecha:
            nuevo_precio = TasacionService.obtener_precio_oro(fecha_actual)
            tasacion.valor = nuevo_precio
            tasacion.fecha = fecha_actual    #fecha del día de la aceptación
            tasacion.importe = round((tasacion.peso_gramos / 1000) * nuevo_precio, 2)
            session.commit()

        #Creamos la venta
        venta = Venta(
            usuario_id = tasacion.usuario_id,
            estado_id = estado_aceptada.id,
            precio = tasacion.valor,
            id_tasacion = tasacion.id,
            gramos = tasacion.peso_gramos
        )

        session.add(venta)
        session.commit()

        return venta, "Tasación aceptada y venta creada correctamente."

    @staticmethod
    def rechazar_tasacion(id_tasacion):
        tasacion = session.query(Tasacion).filter_by(id=id_tasacion).first()

        if not tasacion:
            return None, "La tasación no existe"

        #Obtenemos el estado RECHAZADA

        estado_rechazada = EstadoService.buscar_por_descripcion("RECHAZADA")

        #Registramos la venta como rechazada
        venta = Venta(
            usuario_id=tasacion.usuario_id,
            estado_id=estado_rechazada.id,
            precio=0,                      #Al ser rechazada el precio es 0
            id_tasacion=tasacion.id,
            gramos=tasacion.peso_gramos
        )

        session.add(venta)
        session.commit()

        return venta, "Tasación rechazada correctamente."

    @staticmethod
    def listar_ventas():
        return session.query(Venta).all()