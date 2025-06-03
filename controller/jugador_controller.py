import json
import os
from model.jugador import Jugador

ARCHIVO = os.path.join("data", "jugadores.json")
#mostrar todos los jugadores

def cargar_jugadores():
    if not os.path.exists(ARCHIVO):
        return []
    with open(ARCHIVO, "r") as f:
        data = json.load(f)
        return [Jugador.from_dict(j) for j in data]
#leer jugador 
def guardar_jugadores(jugadores):
    with open(ARCHIVO, "w") as f:
        json.dump([j.to_dict() for j in jugadores], f, indent=4)
#nuevo jugador 
def registrar_jugador(jugador):
    jugadores = cargar_jugadores()
    if any(j.id == jugador.id for j in jugadores):
        print("Ya existe un jugador con ese ID.")
        return
    jugadores.append(jugador)
    guardar_jugadores(jugadores)
    print(" Jugador registrado exitosamente.")

def listar_jugadores():
    return cargar_jugadores()
#buscar un jugador por id 
def buscar_jugador(id):
    jugadores = cargar_jugadores()
    for jugador in jugadores:
        if jugador.id == id:
            return jugador
    return None
#eliminar un jugador por id 
def eliminar_jugador(id):
    jugadores = cargar_jugadores()
    jugadores = [j for j in jugadores if j.id != id]
    guardar_jugadores(jugadores)
    print(" Jugador eliminado.")

def modificar_jugador(id, nuevo_nombre=None, nuevo_saldo=None):
    jugadores = cargar_jugadores()
    for jugador in jugadores:
        if jugador.id == id:
            if nuevo_nombre:
                jugador.nombre = nuevo_nombre
            if nuevo_saldo is not None:
                jugador.saldo_actual = float(nuevo_saldo)
            guardar_jugadores(jugadores)
            print(" Jugador modificado.")
            return
    print(" Jugador no encontrado.")
