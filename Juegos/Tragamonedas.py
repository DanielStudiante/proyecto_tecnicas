import random
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from controller.jugador_controller  import buscar_jugador, guardar_jugadores, cargar_jugadores

simbolos = ["🍒", "🍋", "7️⃣", "BAR", "🔔"]
tabla_ganadora = {
    ("7️⃣", "7️⃣", "7️⃣"): 100,
    ("BAR", "BAR", "BAR"): 50,
    ("🍒", "🍒", "🍒"): 20,
    ("🔔", "🔔", "🔔"): 15,
    ("🍒", "🍒", "*"): 5,
    ("🍒", "*", "*"): 2,
}

def evaluar(combo):
    if combo in tabla_ganadora:
        return tabla_ganadora[combo]
    for regla, premio in tabla_ganadora.items():
        if all(regla[i] == "*" or regla[i] == combo[i] for i in range(3)):
            return premio
    return 0

def jugar_tragamonedas_con_usuario():
    id = input("Ingresa tu ID: ").upper()
    jugador = buscar_jugador(id)
    if not jugador:
        print("Jugador no encontrado.")
        return

    saldo = jugador.saldo_inicial
    costo_jugada = 10

    print(f"\n🎰 Bienvenido {jugador.nombre}")
    print(f"💰 Saldo actual: ${saldo:.2f}")

    while saldo >= costo_jugada:
        eleccion = input("¿Jugar tragamonedas? (S/N): ").upper()
        if eleccion != "S":
            print("👋 ¡Gracias por jugar!")
            break

        saldo -= costo_jugada
        jugada = (random.choice(simbolos), random.choice(simbolos), random.choice(simbolos))
        print(f"🎲 Jugada: {jugada[0]} | {jugada[1]} | {jugada[2]}")

        premio = 0
        for a in simbolos:
            for b in simbolos:
                for c in simbolos:
                    if (a, b, c) == jugada:
                        premio = evaluar(jugada)
                        break

        if premio > 0:
            print(f"🎉 ¡Ganaste ${premio}!")
            saldo += premio
            jugador.agregar_historial(f"Ganó ${premio} con {jugada}")
        else:
            print("😢 No ganaste esta vez.")
            jugador.agregar_historial(f"Perdió ${costo_jugada} con {jugada}")

        print(f"💰 Saldo actualizado: ${saldo:.2f}")

    if saldo < costo_jugada:
        print("💸 Te has quedado sin saldo.")

    jugador.saldo_inicial = saldo
    jugadores = cargar_jugadores()
    for i, j in enumerate(jugadores):
        if j.id == jugador.id:
            jugadores[i] = jugador
            break
    guardar_jugadores(jugadores)

if __name__ == "__main__":
    jugar_tragamonedas_con_usuario()