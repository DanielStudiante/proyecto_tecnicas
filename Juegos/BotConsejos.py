import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from controller.jugador_controller import buscar_jugador, cargar_jugadores, guardar_jugadores
import copy

class OptimizadorApuestas:
    """
    Clase que implementa backtracking para encontrar la mejor estrategia de apuestas
    en el casino, maximizando las ganancias sin quedarse sin saldo.
    """
    
    def __init__(self):
        # Tabla de apuestas disponibles con sus probabilidades estimadas de ganancia
        # Formato: (nombre_juego, monto_apuesta, probabilidad_ganar, multiplicador_ganancia)
        self.tabla_apuestas = [
            # Blackjack - Mayor probabilidad, menor multiplicador
            ("Blackjack Conservador", 100, 0.48, 1.0),    # Apuesta baja, juego conservador
            ("Blackjack Moderado", 500, 0.45, 1.0),       # Apuesta media
            ("Blackjack Agresivo", 1000, 0.42, 1.0),      # Apuesta alta
            ("Blackjack Premium", 2000, 0.40, 1.0),       # Apuesta muy alta
            
            # Tragamonedas - Menor probabilidad, mayor multiplicador potencial
            ("Tragamonedas Básico", 100, 0.25, 2.0),      # Multiplicador promedio
            ("Tragamonedas Medio", 500, 0.20, 3.0),       # Mejor multiplicador
            ("Tragamonedas Premium", 1000, 0.15, 5.0),    # Alto riesgo, alta recompensa
            ("Tragamonedas Jackpot", 2000, 0.10, 10.0),   # Máximo riesgo y recompensa
            
            # Apuestas especiales combinadas
            ("Estrategia Mixta 1", 300, 0.35, 1.5),       # Combinación balanceada
            ("Estrategia Mixta 2", 750, 0.30, 2.5),       # Riesgo medio-alto
        ]
        
        self.mejor_ruta = []
        self.mayor_ganancia = 0
        self.saldo_inicial = 0
        self.max_turnos = 10  # Máximo número de apuestas a considerar
        self.saldo_minimo = 100  # Saldo mínimo para no quedarse en cero
        
    def mostrar_tabla_apuestas(self):
        """Muestra la tabla completa de apuestas disponibles"""
        print("\n" + "=" * 80)
        print("📊 TABLA DE APUESTAS DISPONIBLES")
        print("=" * 80)
        print(f"{'#':<3} {'Estrategia':<25} {'Costo':<8} {'Prob.':<8} {'Mult.':<8} {'Ganancia Esp.':<15}")
        print("-" * 80)
        
        for i, (nombre, costo, prob, mult, ) in enumerate(self.tabla_apuestas, 1):
            ganancia_esperada = (prob * costo * mult) - ((1 - prob) * costo)
            color = "🟢" if ganancia_esperada > 0 else "🔴" if ganancia_esperada < -50 else "🟡"
            print(f"{i:<3} {nombre:<25} ${costo:<7} {prob:<8.2f} {mult:<8.1f}x {color} ${ganancia_esperada:<12.2f}")
        
        print("-" * 80)
        print("📈 Ganancia Esperada = (Probabilidad × Costo × Multiplicador) - ((1-Probabilidad) × Costo)")
        print("🟢 Positiva | 🟡 Neutral | 🔴 Negativa")
        print("=" * 80)
    
    def calcular_ganancia_esperada(self, apuesta):
        """
        Calcula la ganancia esperada de una apuesta
        Args:
            apuesta: tupla (nombre, costo, probabilidad, multiplicador)
        Returns:
            float: ganancia esperada
        """
        nombre, costo, prob, mult = apuesta
        return (prob * costo * mult) - ((1 - prob) * costo)
    
    def es_apuesta_valida(self, saldo_actual, apuesta):
        """
        Verifica si una apuesta es válida dado el saldo actual
        Args:
            saldo_actual: saldo disponible
            apuesta: tupla de la apuesta
        Returns:
            bool: True si la apuesta es válida
        """
        nombre, costo, prob, mult = apuesta
        return saldo_actual >= costo and (saldo_actual - costo) >= self.saldo_minimo
    
    def simular_apuesta(self, saldo_actual, apuesta, ganar=True):
        """
        Simula el resultado de una apuesta
        Args:
            saldo_actual: saldo antes de la apuesta
            apuesta: tupla de la apuesta
            ganar: si gana (True) o pierde (False)
        Returns:
            int: nuevo saldo
        """
        nombre, costo, prob, mult = apuesta
        if ganar:
            return saldo_actual + int(costo * mult)
        else:
            return saldo_actual - costo
    
    def backtrack_optimizar(self, saldo_actual, ruta_actual, turno, ganancia_actual):
        """
        Función principal de backtracking para encontrar la mejor ruta de apuestas
        
        Args:
            saldo_actual: saldo disponible en este punto
            ruta_actual: lista de apuestas realizadas hasta ahora
            turno: número de turno actual
            ganancia_actual: ganancia acumulada hasta ahora
        
        El algoritmo explora todas las combinaciones posibles de apuestas,
        considerando tanto escenarios de victoria como de derrota.
        """
        
        # Caso base 1: Se alcanzó el máximo de turnos
        if turno >= self.max_turnos:
            if ganancia_actual > self.mayor_ganancia:
                self.mayor_ganancia = ganancia_actual
                self.mejor_ruta = copy.deepcopy(ruta_actual)
            return
        
        # Caso base 2: Saldo insuficiente para cualquier apuesta
        apuestas_posibles = [ap for ap in self.tabla_apuestas if self.es_apuesta_valida(saldo_actual, ap)]
        if not apuestas_posibles:
            if ganancia_actual > self.mayor_ganancia:
                self.mayor_ganancia = ganancia_actual
                self.mejor_ruta = copy.deepcopy(ruta_actual)
            return
        
        # Poda: Si incluso en el mejor escenario no podemos superar la mejor ganancia actual
        ganancia_maxima_teorica = ganancia_actual
        saldo_temporal = saldo_actual
        turnos_restantes = self.max_turnos - turno
        
        # Calcular ganancia máxima teórica asumiendo que todas las apuestas futuras ganan
        for _ in range(turnos_restantes):
            mejor_apuesta_teorica = None
            mejor_ganancia_teorica = -float('inf')
            
            for apuesta in self.tabla_apuestas:
                if self.es_apuesta_valida(saldo_temporal, apuesta):
                    nombre, costo, prob, mult = apuesta
                    ganancia_teorica = costo * mult
                    if ganancia_teorica > mejor_ganancia_teorica:
                        mejor_ganancia_teorica = ganancia_teorica
                        mejor_apuesta_teorica = apuesta
            
            if mejor_apuesta_teorica:
                nombre, costo, prob, mult = mejor_apuesta_teorica
                ganancia_maxima_teorica += costo * mult
                saldo_temporal = saldo_temporal + int(costo * mult)
            else:
                break
        
        # Poda: Si la ganancia máxima teórica no supera la mejor actual, no continuar
        if ganancia_maxima_teorica <= self.mayor_ganancia:
            return
        
        # Explorar cada apuesta posible
        for apuesta in apuestas_posibles:
            nombre, costo, prob, mult = apuesta
            
            # Escenario 1: La apuesta GANA
            nuevo_saldo_ganar = self.simular_apuesta(saldo_actual, apuesta, ganar=True)
            nueva_ganancia_ganar = ganancia_actual + int(costo * mult)
            nueva_ruta_ganar = ruta_actual + [(nombre, costo, "GANA", int(costo * mult), nuevo_saldo_ganar)]
            
            # Llamada recursiva para el caso de ganar
            self.backtrack_optimizar(nuevo_saldo_ganar, nueva_ruta_ganar, turno + 1, nueva_ganancia_ganar)
            
            # Escenario 2: La apuesta PIERDE
            nuevo_saldo_perder = self.simular_apuesta(saldo_actual, apuesta, ganar=False)
            nueva_ganancia_perder = ganancia_actual - costo
            nueva_ruta_perder = ruta_actual + [(nombre, costo, "PIERDE", -costo, nuevo_saldo_perder)]
            
            # Solo explorar el caso de perder si el saldo resultante es válido
            if nuevo_saldo_perder >= self.saldo_minimo:
                # Llamada recursiva para el caso de perder
                self.backtrack_optimizar(nuevo_saldo_perder, nueva_ruta_perder, turno + 1, nueva_ganancia_perder)
    
    def encontrar_mejor_estrategia(self, saldo_inicial, max_turnos=10):
        """
        Encuentra la mejor estrategia de apuestas usando backtracking
        
        Args:
            saldo_inicial: saldo con el que se inicia
            max_turnos: máximo número de apuestas a considerar
        
        Returns:
            tuple: (mejor_ruta, mayor_ganancia)
        """
        print(f"\n🔍 Iniciando optimización con backtracking...")
        print(f"💰 Saldo inicial: ${saldo_inicial}")
        print(f"🎯 Máximo turnos: {max_turnos}")
        print(f"⚠️  Saldo mínimo: ${self.saldo_minimo}")
        print("⏳ Esto puede tomar unos segundos...\n")
        
        # Reiniciar variables
        self.saldo_inicial = saldo_inicial
        self.max_turnos = max_turnos
        self.mejor_ruta = []
        self.mayor_ganancia = 0
        
        # Iniciar backtracking
        self.backtrack_optimizar(saldo_inicial, [], 0, 0)
        
        return self.mejor_ruta, self.mayor_ganancia
    
    def mostrar_resultado_optimizacion(self, mejor_ruta, mayor_ganancia):
        """Muestra los resultados de la optimización de forma detallada"""
        print("\n" + "=" * 80)
        print("🏆 RESULTADO DE LA OPTIMIZACIÓN")
        print("=" * 80)
        
        if not mejor_ruta:
            print("❌ No se encontró ninguna estrategia viable.")
            print("💡 Sugerencias:")
            print("   • Aumentar el saldo inicial")
            print("   • Reducir el saldo mínimo")
            print("   • Aumentar el número máximo de turnos")
            return
        
        print(f"💰 Ganancia máxima encontrada: ${mayor_ganancia}")
        print(f"📊 Número de apuestas en la estrategia: {len(mejor_ruta)}")
        print(f"💹 ROI: {(mayor_ganancia / self.saldo_inicial) * 100:.2f}%")
        print("\n📋 ESTRATEGIA ÓPTIMA:")
        print("-" * 80)
        print(f"{'Turno':<6} {'Estrategia':<25} {'Costo':<8} {'Result.':<8} {'Ganancia':<10} {'Saldo':<10}")
        print("-" * 80)
        
        for i, (nombre, costo, resultado, ganancia, saldo_final) in enumerate(mejor_ruta, 1):
            color = "🟢" if resultado == "GANA" else "🔴"
            print(f"{i:<6} {nombre:<25} ${costo:<7} {color}{resultado:<7} ${ganancia:<9} ${saldo_final:<9}")
        
        print("-" * 80)
        print(f"💳 Saldo final: ${mejor_ruta[-1][4] if mejor_ruta else self.saldo_inicial}")
        print(f"📈 Ganancia neta: ${mayor_ganancia}")
        print("=" * 80)
    
    def ejecutar_estrategia_real(self, id_jugador, mejor_ruta):
        """
        Permite al jugador ejecutar la estrategia encontrada en el casino real
        NOTA: Esta es una simulación educativa - en un casino real los resultados son aleatorios
        """
        jugador = buscar_jugador(id_jugador)
        if not jugador:
            print("❌ Jugador no encontrado.")
            return
        
        print(f"\n🎮 Ejecutando estrategia para {jugador.nombre}")
        print(f"💰 Saldo actual: ${jugador.saldo_actual}")
        
        if not mejor_ruta:
            print("❌ No hay estrategia para ejecutar.")
            return
        
        print("\n⚠️  IMPORTANTE: Esta es una simulación educativa.")
        print("En un casino real, los resultados son completamente aleatorios.")
        print("Esta estrategia muestra el 'mejor caso teórico' encontrado por el algoritmo.")
        
        continuar = input("\n¿Deseas simular esta estrategia? (s/n): ").lower().strip()
        if continuar not in ['s', 'si', 'yes', 'y']:
            return
        
        saldo_simulado = jugador.saldo_actual
        ganancia_total = 0
        
        print(f"\n🎯 Simulando estrategia óptima...")
        print("-" * 60)
        
        for i, (nombre, costo, resultado_teorico, ganancia_teorica, saldo_teorico) in enumerate(mejor_ruta, 1):
            if saldo_simulado < costo:
                print(f"❌ Saldo insuficiente en el turno {i}. Simulación terminada.")
                break
            
            print(f"\n🎲 Turno {i}: {nombre}")
            print(f"💰 Saldo antes: ${saldo_simulado}")
            print(f"🎯 Apuesta: ${costo}")
            print(f"🔮 Resultado teórico: {resultado_teorico}")
            
            # En una implementación real, aquí habría lógica aleatoria
            # Para efectos educativos, mostramos el resultado "teórico óptimo"
            saldo_simulado += ganancia_teorica
            ganancia_total += ganancia_teorica
            
            print(f"💹 Ganancia/Pérdida: ${ganancia_teorica}")
            print(f"💳 Nuevo saldo: ${saldo_simulado}")
            
            # Registrar en el historial del jugador
            jugador.agregar_historial(f"[SIMULACIÓN] {nombre}: ${ganancia_teorica}")
        
        print(f"\n🏁 SIMULACIÓN COMPLETADA")
        print(f"💰 Ganancia total simulada: ${ganancia_total}")
        print(f"💳 Saldo final simulado: ${saldo_simulado}")
        
        # Actualizar saldo del jugador (solo para la simulación)
        # En un casino real, esto se haría después de cada juego real
        actualizar = input("\n¿Actualizar el saldo del jugador con esta simulación? (s/n): ").lower().strip()
        if actualizar in ['s', 'si', 'yes', 'y']:
            jugador.saldo_actual = saldo_simulado
            jugador.agregar_historial(f"Simulación de estrategia optimizada completada")
            
            # Guardar cambios
            jugadores = cargar_jugadores()
            for i, j in enumerate(jugadores):
                if j.id == jugador.id:
                    jugadores[i] = jugador
                    break
            guardar_jugadores(jugadores)
            print("✅ Saldo actualizado exitosamente.")

def menu_optimizador():
    """Menú principal del optimizador de apuestas"""
    optimizador = OptimizadorApuestas()
    
    while True:
        print("\n" + "=" * 60)
        print("🧠 OPTIMIZADOR DE APUESTAS - BACKTRACKING")
        print("=" * 60)
        print("1. 📊 Ver tabla de apuestas disponibles")
        print("2. 🔍 Optimizar estrategia de apuestas")
        print("3. 🎮 Ejecutar estrategia encontrada")
        print("4. 🚪 Volver al menú principal")
        print("=" * 60)
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            optimizador.mostrar_tabla_apuestas()
        
        elif opcion == "2":
            try:
                id_jugador = input("Ingresa tu ID de jugador: ").strip().upper()
                jugador = buscar_jugador(id_jugador)
                
                if not jugador:
                    print("❌ Jugador no encontrado.")
                    continue
                
                print(f"\n👤 Jugador: {jugador.nombre}")
                print(f"💰 Saldo actual: ${jugador.saldo_actual}")
                
                # Configuración de parámetros
                saldo_a_usar = input(f"¿Cuánto quieres usar para optimizar? (máx ${jugador.saldo_actual}): $")
                saldo_a_usar = float(saldo_a_usar)
                
                if saldo_a_usar <= 0 or saldo_a_usar > jugador.saldo_actual:
                    print("❌ Monto inválido.")
                    continue
                
                max_turnos = input("¿Máximo número de apuestas a considerar? (recomendado 5-8): ")
                max_turnos = int(max_turnos) if max_turnos.isdigit() else 6
                
                if max_turnos > 10:
                    print("⚠️  Números altos pueden tomar mucho tiempo. Limitando a 10.")
                    max_turnos = 10
                
                # Ejecutar optimización
                mejor_ruta, mayor_ganancia = optimizador.encontrar_mejor_estrategia(saldo_a_usar, max_turnos)
                optimizador.mostrar_resultado_optimizacion(mejor_ruta, mayor_ganancia)
                
            except ValueError:
                print("❌ Valores inválidos. Intenta de nuevo.")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif opcion == "3":
            if not hasattr(optimizador, 'mejor_ruta') or not optimizador.mejor_ruta:
                print("❌ Primero debes optimizar una estrategia (opción 2).")
                continue
            
            id_jugador = input("Ingresa tu ID de jugador: ").strip().upper()
            optimizador.ejecutar_estrategia_real(id_jugador, optimizador.mejor_ruta)
        
        elif opcion == "4":
            print("👋 ¡Volviendo al menú principal!")
            break
        
        else:
            print("❌ Opción inválida. Por favor selecciona 1, 2, 3 o 4.")

# Función para integrar con el sistema existente
def integrar_optimizador():
    """Esta función se puede llamar desde menu_controller.py"""
    menu_optimizador()

if __name__ == "__main__":
    menu_optimizador()