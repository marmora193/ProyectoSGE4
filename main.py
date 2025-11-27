from datetime import date, datetime

from services.services import UsuarioService, TasacionService, VentaService
from gestion.gestion import Gestion


def menu():
    print("¡BIENVENIDO AL GESTOR DE ORO!\n" +
          "Selecciona una opción del menú para comenzar")
    while True:
        print("\n===== MENÚ PRINCIPAL =====")
        print("1. Gestión de Usuarios")
        print("2. Gestión de Tasaciones")
        print("3. Gestión de Ventas")
        print("4. Estadísticas")
        print("5. Gráficos")
        print("0. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            menu_usuarios()
        elif opcion == "2":
            menu_tasaciones()
        elif opcion == "3":
            menu_ventas()
        elif opcion == "4":
            menu_estadisticas()
        elif opcion == "5":
            print("Gráficos: ")
        elif opcion == "0":
            print("¡Hasta pronto!")
            break


def menu_usuarios ():

    while True:
        print("\n--Menú usuarios--")
        print("1. Crear un nuevo usuario")
        print("2. Listar todos los usuarios")
        print("3. Buscar usuario por DNI")
        print("4. Dar de baja usuario")
        print("0. Volver")

        opc = input("Dime qué quieres hacer: ")

        #1. Crear un nuevo usuario
        if opc == "1":
            try:
                nombre = input("Nombre: ")
                apellidos = input("Apellidos: ")
                fecha_nacStr = input("Fecha de nacimiento (DD/MM/YYYY): ")
                fecha_nac = datetime.strptime(fecha_nacStr, "%d/%m/%Y").date()
                dni = input("DNI: ")
                email = input("Email: ")
                nacionalidad = input("Nacionalidad: ")
                telefono = input("Teléfono: ")
                direccion = input("Dirección: ")

                usuario = UsuarioService.crear_usuario(nombre, apellidos, fecha_nac,
                                                   dni, email, nacionalidad, telefono, direccion)
                if usuario:
                    print(f"El usuario con ID: {usuario.id} ha sido creado con éxito.")
                else:
                    print("No se pudo crear el usuario (DNI duplicado).")
            except ValueError:
                print("Error: formato de fecha incorrecto.")
            except Exception as e:
                print(f"Error inesperado: {e}")


        #2. Listar todos los usuarios
        elif opc == "2":
            usuarios = UsuarioService.listar_usuarios()
            print("\nUsuario: \n")
            for usuario in usuarios:
                print(f"Nombre: {usuario.nombre}, Apellidos: {usuario.apellidos}, DNI: {usuario.dni}\n")

        #3. Buscar usuario por DNI
        elif opc == "3":
            dni = input("Introduce el DNI del usuario: ")
            usuario = UsuarioService.buscar_por_dni(dni)

            if usuario:
                print(f"Usuario encontrado:\n Nombre: {usuario.nombre}, Apellidos: {usuario.apellidos}, DNI: {usuario.dni}\n")
            else:
                print("No existe un usuario con ese DNI, por favor, introduce uno válido.")

        #4. Dar de baja usuario
        elif opc == "4":
            dni = input("Introduce el dni del usuario a dar de baja: ")
            usuario = UsuarioService.dar_baja(dni)

            if usuario:
                print(f"El Usuario {usuario.nombre} {usuario.apellidos} ha sido dado de baja correctamente.")
            else:
                print(f"No existe un usuario con ese DNI.")

        elif opc == 0:
            print("Volviendo al menú principal...")
            break

        else:
            print("Opción no válida.")

def menu_tasaciones():
    while True:
        print("\n--Gestión de tasaciones--")
        print("1. Crear tasación")
        print("2. Listar tasaciones")
        print("3. Buscar tasación por ID")
        print("4. Obtener resumen tasaciones")
        print("0. Volver")

        opcion = int(input("Selecciona una opción: "))

        #1. Crear tasación
        if opcion == 1:
            dni = input("Introduce el DNI del usuario: ")
            usuario = UsuarioService.buscar_por_dni(dni)

            #Si el usuario no está registrado se lo indicamos
            if usuario is None:
                print("El usuario no existe. Debe registrarlo antes de crear una tasación")
                continue

            try:
                peso = float(input("Peso en gramos: "))
            except ValueError:
                print("El peso debe ser un número.")
                continue

            tasacion, msg = TasacionService.crear_tasacion(dni, peso)
            print(msg)

        #2. Listar tasaciones
        elif opcion == 2:
            tasaciones = TasacionService.listar_tasaciones()

            if tasaciones:
                for t in tasaciones:
                    print(f"Tasación nº: {t['id']} - Usuario: {t['usuario']} - Importe: {t['importe']} €")
                else:
                    print("No hay tasaciones registradas.")

        #3. Buscar tasación por ID
        elif opcion == 3:
            try:
                id_ = int(input("ID de tasación: "))
            except ValueError:
                print("Debes introducir un número válido.")
                continue

            t = TasacionService.obtener_tasacion_por_id(id_)
            if t:
                print(f"Tasación {t['id']} | Usuario: {t['usuario']} ({t['dni']})")
                print(f"Peso: {t['peso']} g | Valor: {t['valor']} €/kg | Importe: {t['importe']} €")
                print(f"Fecha: {t['fecha']}")
            else:
                print("Tasación no encontrada.")

        #Obtener resumen tasaciones
        elif opcion == 4:
            resumen = TasacionService.obtener_resumen_tasaciones()
        elif opcion == 0:
            break
        else:
            print("Opción no válida.")

def menu_ventas():
    while True:
        print("\n--- Gestión de Ventas ---")
        print("1. Aceptar tasación")
        print("2. Rechazar tasación")
        print("3. Listar ventas")
        print("0. Volver")

        opcion = input("Selecciona una opción: ")

        #1. Aceptar tasación
        if opcion == "1":
            try:
                id = int(input("ID de tasación: "))
            except ValueError:
                print("Introduce un ID válido.")
                continue

            venta, msg = VentaService.aceptar_tasacion(id)
            print(msg)

        #2. Rechazar tasación
        elif opcion == "2":
            try:
                id_ = int(input("ID de tasación: "))
            except ValueError:
                print("Debes introducir un número válido.")

            venta, msg = VentaService.rechazar_tasacion(id_)
            print(msg)

        #3. Listar ventas
        elif opcion == "3":
            ventas = VentaService.listar_ventas()

            if ventas:
                for v in ventas:
                    print(f"Venta {v.id}: - Tasación nº {v.id_tasacion} - Estado: {v.estado.descripcion} - Precio: {v.precio} €")
            else:
                print("No hay ventas registradas.")

        elif opcion == "0":
            break

        else:
            print("Opción no válida.")

def menu_estadisticas():
    while True:
        print("\n--- Estadísticas ---")
        print("1. Resumen de tasaciones")
        print("2. Ventas por mes")
        print("3. Ventas por cliente")
        print("4. Tasaciones no aceptadas")
        print("5. Cliente con más ventas")
        print("6. Clientes sin ventas en 3 meses")
        print("0. Volver")

        opc = input("Opción: ")

        if opc == "1":
            TasacionService.obtener_estadisticas_tasaciones()
        elif opc == "2":
            Gestion.ventas_por_mes()
        elif opc == "3":
            Gestion.ventas_por_cliente()
        elif opc == "4":
            Gestion.tasaciones_no_aceptadas()
        elif opc == "5":
            Gestion.cliente_con_mas_ventas()
        elif opc == "6":
            Gestion.clientes_inactivos_3_meses()
        elif opc == "0":
            break
        else:
            print("Opción no válida.")


if __name__ == '__main__':
    menu()