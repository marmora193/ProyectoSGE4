from datetime import date, datetime

from services.services import UsuarioService, TasacionService, VentaService


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

        opcion = int(input("Selecciona una opción: "))

        if opcion == 1:
            menu_usuarios()
        elif opcion == 2:
            menu_tasaciones()
        elif opcion == 3:
            menu_ventas()
        elif opcion == 4:
            print("Estadísticas: ")
        elif opcion == 5:
            print("Gráficos: ")
        elif opcion == 0:
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

        opc = int(input("Dime qué quieres hacer: "))

        #1. Crear un nuevo usuario
        if opc == 1:
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
            print(f"El cliente con ID: {usuario.id} ha sido creado con éxito.")

        #2. Listar todos los usuarios
        elif opc == 2:
            usuarios = UsuarioService.listar_usuarios()
            print("\nUsuario: \n")
            for usuario in usuarios:
                print(f"Nombre: {usuario.nombre}, Apellidos: {usuario.apellidos}, DNI: {usuario.dni}\n")

        #3. Buscar usuario por DNI
        elif opc == 3:
            dni = input("Introduce el DNI del usuario: ")
            usuario = UsuarioService.buscar_por_dni(dni)

            if usuario:
                print(f"Usuario encontrado:\n Nombre: {usuario.nombre}, Apellidos: {usuario.apellidos}, DNI: {usuario.dni}\n")
            else:
                print("No existe un usuario con ese DNI, por favor, introduce uno válido.")

        #4. Dar de baja usuario
        elif opc == 4:
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
        print("0. Volver")

        opcion = int(input("Selecciona una opción: "))

        #1. Crear tasación
        if opcion == 1:
            dni = input("Introduce el DNI del usuario: ")
            usuario = UsuarioService.buscar_por_dni(dni)

            #Si el usuario no está registrado se lo indicamos
            if usuario is None:
                print("El usuario no existe. Debe registrarlo antes de crear una tasación")
                return

            peso = float(input("Peso en gramos: "))
            tasacion, msg = TasacionService.crear_tasacion(dni, peso)
            print(msg)

        #2. Listar tasaciones
        elif opcion == 2:
            tasaciones = TasacionService.listar_tasaciones()
            for t in tasaciones:
                print(f"Tasación nº: {t['id']} - Usuario: {t['usuario']} - Importe: {t['importe']} €")

        #3. Buscar tasación por ID
        elif opcion == 3:
            id_ = int(input("ID de tasación: "))
            t = TasacionService.obtener_tasacion_por_id(id_)
            if t:
                print(f"Tasación nº {t['id']} - Usuario: {t['usuario']} - Importe: {t['importe']} € - Peso: {t['peso']}g - Valor: {t['valor']} €/kg - Fecha: {t['fecha']}")
            else:
                print("Tasación no encontrada.")

        elif opcion == 0:
            break

def menu_ventas():
    while True:
        print("\n--- Gestión de Ventas ---")
        print("1. Aceptar tasación")
        print("2. Rechazar tasación")
        print("3. Listar ventas")
        print("0. Volver")

        opcion = int(input("Selecciona una opción: "))

        if opcion == 1:
            id = int(input("ID de tasación: "))
            venta, msg = VentaService.aceptar_tasacion(id)
            print(msg)

        elif opcion == 2:
            id_ = int(input("ID de tasación: "))
            venta, msg = VentaService.rechazar_tasacion(id_)
            print(msg)

        elif opcion == 3:
            ventas = VentaService.listar_ventas()
            for v in ventas:
                print(f"Venta {v.id}: - Tasación nº {v.id_tasacion} - Estado: {v.estado.descripcion} - Precio: {v.precio} €")

        elif opcion == "0":
            break


if __name__ == '__main__':
    menu()