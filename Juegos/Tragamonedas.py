import random
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from controller.jugador_controller  import buscar_jugador, guardar_jugadores, cargar_jugadores

simbolos = ["🍒", "🍋", "7️⃣", "BAR", "🔔"]
tabla_ganadora = {
    # Combinaciones exactas (tres símbolos iguales)
    ("7️⃣", "7️⃣", "7️⃣"): 50000,     # Premio mayor
    ("BAR", "BAR", "BAR"): 25000,     # Premio alto
    ("🍒", "🍒", "🍒"): 20000,         # Premio medio
    ("🔔", "🔔", "🔔"): 15000,         # Premio medio-bajo
    ("🍋", "🍋", "🍋"): 10000,         # Premio bajo

    # Combinaciones parciales con *=(cualquier elemento en esa posicion)
    ("7️⃣", "*", "7️⃣"): 15000,        # Sietes en los extremos
    ("BAR", "BAR", "*"): 10000,        # Dos BAR al inicio
    ("🔔", "🔔", "*"): 7000,           # Dos campanas al inicio
    ("🍒", "*", "🍒"): 6000,           # Cerezas en los extremos
    ("🍒", "🍒", "*"): 5000,           # Dos cerezas al inicio
    ("*", "🍒", "🍒"): 5000,           # Dos cerezas al final
    ("*", "7️⃣", "*"): 3000,          # Un siete en el medio
    ("*", "BAR", "*"): 2000,          # Un BAR en el medio
    ("🍒", "*", "*"): 2000            # Una cereza al inicio
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

    saldo = jugador.saldo_actual
    costo_jugada = 1000

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

    jugador.saldo_actual = saldo #  Actualizar el saldo 
    jugadores = cargar_jugadores()
    for i, j in enumerate(jugadores):
        if j.id == jugador.id:
            jugadores[i] = jugador
            break
    guardar_jugadores(jugadores)


def mostrar_tabla_premios():
    """Muestra la tabla de premios del tragamonedas"""
    simbolos = ["🍒", "🍋", "7️⃣", "BAR", "🔔"]
    tabla_ganadora = {
        ("7️⃣", "7️⃣", "7️⃣"): 50000,
        ("BAR", "BAR", "BAR"): 25000,
        ("🍒", "🍒", "🍒"): 20000,
        ("🔔", "🔔", "🔔"): 15000,
        ("🍋", "🍋", "🍋"): 10000,
        ("7️⃣", "*", "7️⃣"): 15000,
        ("BAR", "BAR", "*"): 10000,
        ("🔔", "🔔", "*"): 7000,
        ("🍒", "*", "🍒"): 6000,
        ("🍒", "🍒", "*"): 5000,
        ("*", "🍒", "🍒"): 5000,
        ("*", "7️⃣", "*"): 3000,
        ("*", "BAR", "*"): 2000,
        ("🍒", "*", "*"): 2000
    }
    
    print("\n" + "=" * 50)
    print("🏆 TABLA DE PREMIOS - TRAGAMONEDAS")
    print("=" * 50)
    print("💰 COMBINACIONES GANADORAS:")
    print()
    
    premios_ordenados = sorted(tabla_ganadora.items(), key=lambda x: x[1], reverse=True)
    
    for combo, premio in premios_ordenados:
        combo_str = " | ".join(combo)
        combo_str = combo_str.replace("*", "❓")
        print(f"  {combo_str:<15} → ${premio:,}")
    
    print("\n📋 NOTAS:")
    print("  • ❓ = Cualquier símbolo")
    print("  • Costo por jugada: $100")
    print(f"  • Premio máximo: ${max(tabla_ganadora.values()):,}")
    print("=" * 50)

def mostrar_reglas():
    """Muestra las reglas del juego"""
    print("\n📋 REGLAS DEL TRAGAMONEDAS:")
    print("=" * 50)
    print("🎯 OBJETIVO:")
    print("   Conseguir combinaciones ganadoras de símbolos")
    print("\n🎮 CÓMO JUGAR:")
    print("   • Cada jugada cuesta: $100")
    print("   • Se generan 3 símbolos aleatorios")
    print("   • Si formas una combinación ganadora, recibes un premio")
    print("   • Los premios varían según la combinación")
    print("\n🎰 SÍMBOLOS:")
    simbolos = ["🍒", "🍋", "7️⃣", "BAR", "🔔"]
    for simbolo in simbolos:
        print(f"   • {simbolo}")
    print("\n💡 CONSEJOS:")
    print("   • 7️⃣ 7️⃣ 7️⃣ es la combinación más valiosa")
    print("   • Algunas combinaciones parciales también premian")
    print("   • Gestiona tu saldo responsablemente")
    print("=" * 50)

def menu_tragamonedas():
    """Menú principal del tragamonedas"""
    while True:
        print("\n" + "=" * 50)
        print("🎰 CASINO - TRAGAMONEDAS DELUXE")
        print("=" * 50)
        print("1. 🎮 Jugar Tragamonedas")
        print("2. 🏆 Ver tabla de premios")
        print("3. 📋 Ver reglas del juego")
        print("4. 🚪 Salir")
        print("=" * 50)
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            print("\n🎰 Iniciando el juego...")
            # Aquí llamas tu función original
            jugar_tragamonedas_con_usuario()
            
            # Preguntar si quiere volver al menú
            while True:
                volver = input("\n¿Quieres volver al menú principal? (s/n): ").lower().strip()
                if volver in ['s', 'si', 'yes', 'y']:
                    break
                elif volver in ['n', 'no']:
                    print("👋 ¡Gracias por jugar!")
                    return
                else:
                    print("❌ Responde 's' para sí o 'n' para no.")
        
        elif opcion == "2":
            mostrar_tabla_premios()
        
        elif opcion == "3":
            mostrar_reglas()
        
        elif opcion == "4":
            print("👋 ¡Gracias por visitar nuestro casino!")
            print("🍀 ¡Que tengas mucha suerte en tu próxima visita!")
            break
        
        else:
            print("❌ Opción inválida. Por favor selecciona 1, 2, 3 o 4.")



    