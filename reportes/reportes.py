import json
import os
from collections import Counter, defaultdict
from datetime import datetime
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from controller.jugador_controller import cargar_jugadores

class GeneradorReportes:
    def __init__(self):
        self.jugadores = cargar_jugadores()

    def reporte_jugadores_mayor_saldo(self):
        """1. Jugadores con mayor saldo actual"""
        print("\n" + "=" * 60)
        print("📊 REPORTE 1: JUGADORES CON MAYOR SALDO")
        print("=" * 60)
        
        if not self.jugadores:
            print("❌ No hay jugadores registrados.")
            return
        
        # Ordenar jugadores por saldo actual (descendente)
        jugadores_ordenados = sorted(self.jugadores, key=lambda x: x.saldo_actual, reverse=True)
        
        print(f"{'POSICIÓN':<10} {'NOMBRE':<25} {'ID':<10} {'SALDO ACTUAL':<15}")
        print("-" * 60)
        
        for i, jugador in enumerate(jugadores_ordenados, 1):
            print(f"{i:<10} {jugador.nombre[:24]:<25} {jugador.id:<10} ${jugador.saldo_actual:<14.2f}")
        
        # Estadísticas adicionales
        print("\n📈 ESTADÍSTICAS:")
        total_saldo = sum(j.saldo_actual for j in self.jugadores)
        promedio_saldo = total_saldo / len(self.jugadores)
        print(f"💰 Saldo total en el casino: ${total_saldo:.2f}")
        print(f"📊 Saldo promedio por jugador: ${promedio_saldo:.2f}")
        print(f"🏆 Jugador con más dinero: {jugadores_ordenados[0].nombre} (${jugadores_ordenados[0].saldo_actual:.2f})")
        print("=" * 60)
    
    
    
    def _analizar_historial_jugador(self, jugador):
        """Analiza el historial de un jugador para generar estadísticas"""
        if not jugador.historial:
            return
        
        print("\n🔍 ANÁLISIS DEL HISTORIAL:")
        
        # Contar juegos jugados
        juegos_blackjack = sum(1 for actividad in jugador.historial if "Blackjack" in actividad)
        juegos_tragamonedas = sum(1 for actividad in jugador.historial if any(simbolo in actividad for simbolo in ["🍒", "🍋", "7️⃣", "🔔", "BAR"]))
        
        print(f"🃏 Partidas de Blackjack: {juegos_blackjack}")
        print(f"🎰 Jugadas de Tragamonedas: {juegos_tragamonedas}")
        
        # Contar victorias y derrotas
        victorias = sum(1 for actividad in jugador.historial if "Ganó" in actividad)
        derrotas = sum(1 for actividad in jugador.historial if "Perdió" in actividad)
        
        if victorias + derrotas > 0:
            porcentaje_victoria = (victorias / (victorias + derrotas)) * 100
            print(f"🏆 Victorias: {victorias}")
            print(f"💸 Derrotas: {derrotas}")
            print(f"📊 Porcentaje de victorias: {porcentaje_victoria:.1f}%")
    
    def reporte_ranking_mejores_jugadores(self):
        """3. Ranking de los mejores jugadores (por ganancia total)"""
        print("\n" + "=" * 60)
        print("📊 REPORTE 3: RANKING DE MEJORES JUGADORES")
        print("=" * 60)
        
        if not self.jugadores:
            print("❌ No hay jugadores registrados.")
            return
        
        # Calcular ganancia/pérdida de cada jugador
        jugadores_con_ganancia = []
        for jugador in self.jugadores:
            ganancia = jugador.saldo_actual - jugador.saldo_inicial
            jugadores_con_ganancia.append((jugador, ganancia))
        
        # Ordenar por ganancia (descendente)
        jugadores_con_ganancia.sort(key=lambda x: x[1], reverse=True)
        
        print(f"{'RANK':<6} {'NOMBRE':<25} {'ID':<10} {'GANANCIA/PÉRDIDA':<18} {'ESTADO':<10}")
        print("-" * 70)
        
        for i, (jugador, ganancia) in enumerate(jugadores_con_ganancia, 1):
            estado = "🏆 GANADOR" if ganancia > 0 else "💸 PERDEDOR" if ganancia < 0 else "🤝 EMPATE"
            signo = "+" if ganancia >= 0 else ""
            print(f"{i:<6} {jugador.nombre[:24]:<25} {jugador.id:<10} {signo}${ganancia:<17.2f} {estado}")
        
        # Estadísticas del ranking
        ganadores = sum(1 for _, ganancia in jugadores_con_ganancia if ganancia > 0)
        perdedores = sum(1 for _, ganancia in jugadores_con_ganancia if ganancia < 0)
        empates = len(jugadores_con_ganancia) - ganadores - perdedores
        
        print(f"\n📈 ESTADÍSTICAS DEL RANKING:")
        print(f"🏆 Ganadores netos: {ganadores}")
        print(f"💸 Perdedores netos: {perdedores}")
        print(f"🤝 Sin cambios: {empates}")
        
        if jugadores_con_ganancia:
            mejor_jugador, mejor_ganancia = jugadores_con_ganancia[0]
            print(f"👑 Mejor jugador: {mejor_jugador.nombre} (+${mejor_ganancia:.2f})")
        
        print("=" * 60)
    
    def reporte_jugadores_mas_perdidas(self):
        """4. Jugadores que más veces han perdido"""
        print("\n" + "=" * 60)
        print("📊 REPORTE 4: JUGADORES CON MÁS DERROTAS")
        print("=" * 60)
        
        if not self.jugadores:
            print("❌ No hay jugadores registrados.")
            return
        
        # Contar derrotas por jugador
        jugadores_derrotas = []
        for jugador in self.jugadores:
            derrotas = sum(1 for actividad in jugador.historial if "Perdió" in actividad)
            victorias = sum(1 for actividad in jugador.historial if "Ganó" in actividad)
            total_juegos = derrotas + victorias
            
            if total_juegos > 0:
                porcentaje_derrotas = (derrotas / total_juegos) * 100
                jugadores_derrotas.append((jugador, derrotas, victorias, porcentaje_derrotas))
        
        # Ordenar por número de derrotas (descendente)
        jugadores_derrotas.sort(key=lambda x: x[1], reverse=True)
        
        if not jugadores_derrotas:
            print("📋 No hay jugadores con historial de juegos.")
            return
        
        print(f"{'NOMBRE':<25} {'ID':<10} {'DERROTAS':<10} {'VICTORIAS':<10} {'% DERROTAS':<12}")
        print("-" * 70)
        
        for jugador, derrotas, victorias, porcentaje in jugadores_derrotas:
            print(f"{jugador.nombre[:24]:<25} {jugador.id:<10} {derrotas:<10} {victorias:<10} {porcentaje:<11.1f}%")
        
        # Estadísticas adicionales
        print(f"\n💸 ESTADÍSTICAS DE DERROTAS:")
        total_derrotas = sum(derrotas for _, derrotas, _, _ in jugadores_derrotas)
        total_victorias = sum(victorias for _, _, victorias, _ in jugadores_derrotas)
        
        print(f"📊 Total de derrotas en el casino: {total_derrotas}")
        print(f"🏆 Total de victorias en el casino: {total_victorias}")
        
        if jugadores_derrotas:
            peor_jugador = jugadores_derrotas[0]
            print(f"💔 Jugador con más derrotas: {peor_jugador[0].nombre} ({peor_jugador[1]} derrotas)")
        
        print("=" * 60)
    
    def reporte_juegos_mas_participacion(self):
        """5. Análisis de participación por juego"""
        print("\n" + "=" * 60)
        print("📊 REPORTE 5: JUEGOS CON MAYOR PARTICIPACIÓN")
        print("=" * 60)
        
        if not self.jugadores:
            print("❌ No hay jugadores registrados.")
            return
        
        # Contar participaciones por juego
        blackjack_partidas = 0
        tragamonedas_jugadas = 0
        
        # Análisis detallado por jugador
        jugadores_blackjack = set()
        jugadores_tragamonedas = set()
        
        for jugador in self.jugadores:
            blackjack_jugador = 0
            tragamonedas_jugador = 0
            
            for actividad in jugador.historial:
                if "Blackjack" in actividad:
                    blackjack_partidas += 1
                    blackjack_jugador += 1
                    jugadores_blackjack.add(jugador.id)
                elif any(simbolo in actividad for simbolo in ["🍒", "🍋", "7️⃣", "🔔", "BAR"]):
                    tragamonedas_jugadas += 1
                    tragamonedas_jugador += 1
                    jugadores_tragamonedas.add(jugador.id)
        
        print("🎮 ESTADÍSTICAS DE PARTICIPACIÓN:")
        print(f"🃏 Blackjack:")
        print(f"   • Partidas totales: {blackjack_partidas}")
        print(f"   • Jugadores únicos: {len(jugadores_blackjack)}")
        print(f"   • Promedio partidas/jugador: {blackjack_partidas/len(jugadores_blackjack) if jugadores_blackjack else 0:.1f}")
        
        print(f"\n🎰 Tragamonedas:")
        print(f"   • Jugadas totales: {tragamonedas_jugadas}")
        print(f"   • Jugadores únicos: {len(jugadores_tragamonedas)}")
        print(f"   • Promedio jugadas/jugador: {tragamonedas_jugadas/len(jugadores_tragamonedas) if jugadores_tragamonedas else 0:.1f}")
        
        # Determinar juego más popular
        total_actividades = blackjack_partidas + tragamonedas_jugadas
        if total_actividades > 0:
            print(f"\n🏆 JUEGO MÁS POPULAR:")
            if blackjack_partidas > tragamonedas_jugadas:
                porcentaje = (blackjack_partidas / total_actividades) * 100
                print(f"🃏 Blackjack ({porcentaje:.1f}% de todas las partidas)")
            elif tragamonedas_jugadas > blackjack_partidas:
                porcentaje = (tragamonedas_jugadas / total_actividades) * 100
                print(f"🎰 Tragamonedas ({porcentaje:.1f}% de todas las partidas)")
            else:
                print("🤝 Empate entre ambos juegos")
        
        print("=" * 60)
    
def menu_reportes():
    """Menú principal del sistema de reportes"""
    generador = GeneradorReportes()
    
    while True:
        print("\n" + "=" * 60)
        print("📊 SISTEMA DE REPORTES DEL CASINO")
        print("=" * 60)
        print("1. 💰 Jugadores con mayor saldo")
        print("2. 🏆 Ranking de mejores jugadores")
        print("3. 💸 Jugadores con más derrotas")
        print("4. 🎮 Juegos con mayor participación")
        print("5. 🚪 Salir")
        print("=" * 60)
        
        opcion = input("Selecciona una opción: ").strip()
        
        try:
            if opcion == "1":
                generador.reporte_jugadores_mayor_saldo()
            elif opcion == "2":
                generador.reporte_ranking_mejores_jugadores()
            elif opcion == "3":
                generador.reporte_jugadores_mas_perdidas()
            elif opcion == "4":
                generador.reporte_juegos_mas_participacion()
            elif opcion == "5":
                print("👋 ¡Gracias por usar el sistema de reportes!")
                break
            else:
                print("❌ Opción inválida. Por favor selecciona un número del 1 al 5.")
            
            # Pausa para que el usuario pueda leer el reporte
            input("\nPresiona Enter para continuar...")
            
        except Exception as e:
            print(f"❌ Error al generar el reporte: {e}")
            input("\nPresiona Enter para continuar...")