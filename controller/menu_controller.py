from views.menu import menu_principal, menu_jugadores, menu_juegos
from controller.jugador_controller import *
from Juegos.Tragamonedas import menu_tragamonedas #llamado a la funcion de tragamonedas
from Juegos.BlackJack import menu_blackjack
from Juegos.BotConsejos import menu_optimizador
from reportes.reportes import menu_reportes  # Importar el sistema de reportes
# from Juegos.BlackJack import jugar_blackjack


def menu_principal_controller():
    while True:
        menu_principal()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            controllerMenu()
        elif opcion == "2":
            menu_juegos_controller()
        elif opcion == "3":
            id = input("ID del jugador: ").upper()
            jugador = buscar_jugador(id)
            if jugador:
                print("Historial de actividades:")
                for actividad in jugador.historial:
                    print("-", actividad)
            else: 
                print("Jugador no encontrado.")
        elif opcion == "4":
            menu_optimizador()
        elif opcion == "5" :
            menu_reportes()
        elif opcion == "6":
            print("¡ESPERAMOS VERTE DE NUEVO EN EL CASINO!")
            break
        else:
            print("Opción inválida.")

def controllerMenu():
    while True:
        menu_jugadores()
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

def menu_juegos_controller():
    while True:
        menu_juegos()
        opcion = input("Seleccione un juego: ")
        if opcion == "1":
            menu_blackjack()
            # jugar blackjack()
        elif opcion == "2":
            menu_tragamonedas()
            # jugar tragamonedas
        elif opcion == "3":
            break
        else:
            print("Opción inválida.")