from datetime import date, datetime

from db.config import session
from services.services import ClienteService


def menu ():
    print("Bienvenido a X, una aplicación")
    while True:
        print("--Menú principal--")
        print("1. Crear un nuevo cliente")
        print("2. Listar todos los clientes")
        print("3. Buscar cliente por DNI")
        print("4. Dar de baja cliente")
        print("15. Salir")

        opc = int(input("Dime qué quieres hacer"))

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

            cliente = ClienteService.crear_cliente(nombre, apellidos, fecha_nac,
                                                   dni, email, nacionalidad, telefono, direccion)
            print(f"El cliente con ID: {cliente.id} ha sido creado con éxito.")

        elif opc == 2:
            clientes = ClienteService.listar_clientes()
            print("\nClientes: \n")
            for cliente in clientes:
                print(f"Nombre: {cliente.nombre}, Apellidos: {cliente.apellidos}, DNI: {cliente.dni}\n")

        elif opc == 3:
            dni = input("Introduce el DNI del cliente: ")
            cliente = ClienteService.buscar_por_dni(dni)

            if cliente:
                print(f"Cliente encontrado:\n Nombre: {cliente.nombre}, Apellidos: {cliente.apellidos}, DNI: {cliente.dni}\n")
            else:
                print("No existe un cliente con ese DNI, por favor, introduce uno válido.")

        elif opc == 4:
            dni = input("Introduce el dni del cliente a dar de baja: ")
            cliente = ClienteService.dar_baja(dni)

            if cliente:
                print(f"El cliente {cliente.nombre} {cliente.apellidos} ha sido dado de baja correctamente.")
            else:
                print(f"No existe un cliente con ese DNI.")

        elif opc == 15:
            print("¡Hasta pronto!")
            break

        else:
            print("Opción no válida.")


if __name__ == '__main__':
    menu()