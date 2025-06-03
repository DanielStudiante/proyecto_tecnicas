from views.menu import viewMenu
from controller.jugador_controller import *
def controllerMenu():
    while True:
        viewMenu()#esta funcion llama al view para mostrar el menu 

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Nombre completo: ")
            id = input("ID único: ").upper()
            saldo_inicial = input("Saldo inicial: ")
            registrar_jugador(Jugador(nombre, id, saldo_inicial))
        elif opcion == "2":
            for j in listar_jugadores():
                print(j)
        elif opcion == "3":
            id = input("ID del jugador: ").upper()
            jugador = buscar_jugador(id)
            if jugador:
                print(jugador)
            else:
                print("Jugador no encontrado.")
        elif opcion == "4":
            id = input("ID del jugador a modificar: ")
            nuevo_nombre = input("Nuevo nombre (enter para dejar igual): ")
            nuevo_saldo = input("Nuevo saldo (enter para dejar igual): ")
            nuevo_saldo = float(nuevo_saldo) if nuevo_saldo else None
            modificar_jugador(id, nuevo_nombre or None, nuevo_saldo)
        elif opcion == "5":
            id = input("ID del jugador a eliminar: ").upper()
            eliminar_jugador(id)
        elif opcion == "6":
            break 
        else:
            print("Opción inválida.")