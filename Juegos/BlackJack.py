import random
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from controller.jugador_controller import buscar_jugador, cargar_jugadores , guardar_jugadores


class CartaBlackjack:
    def __init__(self, valor, nombre):
        self.valor = valor
        self.nombre = nombre
    
    def __str__(self):
        return self.nombre

class BlackjackSimplificado:
    def __init__(self):
        self.cartas = self._crear_baraja()
        self.mano_jugador = []
        self.mano_dealer = []
        self.jugador_actual = None
        self.apuesta = 0
    
    def _crear_baraja(self):
        """Crea una baraja simplificada para Blackjack"""
        cartas = []
        valores = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]  # J, Q, K = 10, A = 11
        nombres = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        
        # Crear 4 copias de cada carta (4 palos)
        for _ in range(4):
            for i, valor in enumerate(valores):
                cartas.append(CartaBlackjack(valor, nombres[i]))
        
        return cartas
    
    def _barajar_cartas(self):
        """Baraja las cartas aleatoriamente"""
        random.shuffle(self.cartas)
    
    def _repartir_carta(self):
        """Reparte una carta de la baraja"""
        if not self.cartas:
            self.cartas = self._crear_baraja()
            self._barajar_cartas()
        return self.cartas.pop()
    
    def _calcular_puntaje_recursivo(self, mano, indice=0, suma_actual=0, ases=0):
        """
        Calcula el puntaje de una mano usando recursión de pila.
        Maneja los ases de forma inteligente (1 u 11).
        """
        # Caso base: hemos procesado todas las cartas
        if indice >= len(mano):
            # Ajustar ases si es necesario
            while suma_actual > 21 and ases > 0:
                suma_actual -= 10  # Cambiar As de 11 a 1
                ases -= 1
            return suma_actual
        
        # Caso recursivo: procesar la carta actual
        carta_actual = mano[indice]
        nueva_suma = suma_actual + carta_actual.valor
        nuevos_ases = ases + (1 if carta_actual.valor == 11 else 0)
        
        # Llamada recursiva para procesar la siguiente carta
        return self._calcular_puntaje_recursivo(mano, indice + 1, nueva_suma, nuevos_ases)
    
    def _mostrar_mano(self, mano, ocultar_primera=False):
        """Muestra las cartas de una mano"""
        if ocultar_primera:
            print("Cartas: [OCULTA]", end="")
            for carta in mano[1:]:
                print(f", {carta}", end="")
        else:
            print("Cartas:", end="")
            for i, carta in enumerate(mano):
                if i == 0:
                    print(f" {carta}", end="")
                else:
                    print(f", {carta}", end="")
        print()
    
    def _es_blackjack(self, mano):
        """Verifica si una mano es Blackjack (21 con 2 cartas)"""
        return len(mano) == 2 and self._calcular_puntaje_recursivo(mano) == 21
    
    def iniciar_juego(self, id_jugador, apuesta):
        """Inicia una nueva partida de Blackjack"""
        # Buscar jugador
        self.jugador_actual = buscar_jugador(id_jugador)
        if not self.jugador_actual:
            print("❌ Jugador no encontrado.")
            return False
        
        # Verificar saldo suficiente
        if self.jugador_actual.saldo_actual < apuesta:
            print(f"❌ Saldo insuficiente. Saldo actual: ${self.jugador_actual.saldo_actual}")
            return False
        
        self.apuesta = apuesta
        print(f"\n🎰 ¡Bienvenido al Blackjack, {self.jugador_actual.nombre}!")
        print(f"💰 Apuesta: ${apuesta}")
        print(f"💳 Saldo actual: ${self.jugador_actual.saldo_actual}")
        print("=" * 50)
        
        # Reiniciar el juego
        self.mano_jugador = []
        self.mano_dealer = []
        self.cartas = self._crear_baraja()
        self._barajar_cartas()
        
        # Repartir cartas iniciales
        self.mano_jugador.append(self._repartir_carta())
        self.mano_dealer.append(self._repartir_carta())
        self.mano_jugador.append(self._repartir_carta())
        self.mano_dealer.append(self._repartir_carta())
        
        return True
    
    def mostrar_estado_juego(self, mostrar_dealer_completo=False):
        """Muestra el estado actual del juego"""
        print(f"\n👤 {self.jugador_actual.nombre}:")
        self._mostrar_mano(self.mano_jugador)
        puntaje_jugador = self._calcular_puntaje_recursivo(self.mano_jugador)
        print(f"Puntaje: {puntaje_jugador}")
        
        print(f"\n🏠 Dealer:")
        self._mostrar_mano(self.mano_dealer, not mostrar_dealer_completo)
        if mostrar_dealer_completo:
            puntaje_dealer = self._calcular_puntaje_recursivo(self.mano_dealer)
            print(f"Puntaje: {puntaje_dealer}")
        else:
            # Solo mostrar el puntaje de la carta visible
            puntaje_visible = self.mano_dealer[1].valor if len(self.mano_dealer) > 1 else 0
            if self.mano_dealer[1].valor == 11 and puntaje_visible > 21:
                puntaje_visible = 1
            print(f"Puntaje visible: {puntaje_visible}")
    
    def turno_jugador(self):
        """Maneja el turno del jugador"""
        while True:
            self.mostrar_estado_juego()
            puntaje = self._calcular_puntaje_recursivo(self.mano_jugador)
            
            # Verificar Blackjack
            if self._es_blackjack(self.mano_jugador):
                print("\n🎉 ¡BLACKJACK! ¡21 con 2 cartas!")
                return "blackjack"
            
            # Verificar si se pasó de 21
            if puntaje > 21:
                print(f"\n💥 ¡Te pasaste! Puntaje: {puntaje}")
                return "bust"
            
            # Pedir acción al jugador
            while True:
                accion = input("\n¿Qué deseas hacer? (h)it / (s)tand: ").lower().strip()
                if accion in ['h', 'hit', 's', 'stand']:
                    break
                print("❌ Opción inválida. Usa 'h' para pedir carta o 's' para plantarte.")
            
            if accion in ['s', 'stand']:
                print(f"\n✋ Te plantas con {puntaje} puntos.")
                return "stand"
            else:
                self.mano_jugador.append(self._repartir_carta())
                nueva_carta = self.mano_jugador[-1]
                print(f"\n🃏 Nueva carta: {nueva_carta}")
    
    def turno_dealer(self):
        """Maneja el turno del dealer (automático)"""
        print(f"\n🏠 Turno del Dealer:")
        self.mostrar_estado_juego(True)
        
        while True:
            puntaje = self._calcular_puntaje_recursivo(self.mano_dealer)
            
            if puntaje >= 17:
                if puntaje > 21:
                    print(f"\n💥 ¡El dealer se pasó! Puntaje: {puntaje}")
                    return "bust"
                else:
                    print(f"\n✋ El dealer se planta con {puntaje} puntos.")
                    return "stand"
            else:
                nueva_carta = self._repartir_carta()
                self.mano_dealer.append(nueva_carta)
                print(f"\n🃏 Dealer toma carta: {nueva_carta}")
                nuevo_puntaje = self._calcular_puntaje_recursivo(self.mano_dealer)
                print(f"Nuevo puntaje del dealer: {nuevo_puntaje}")
    
    def determinar_ganador(self, resultado_jugador, resultado_dealer):
        """Determina el ganador y actualiza el saldo"""
        puntaje_jugador = self._calcular_puntaje_recursivo(self.mano_jugador)
        puntaje_dealer = self._calcular_puntaje_recursivo(self.mano_dealer)
        
        print("\n" + "=" * 50)
        print("📊 RESULTADO FINAL:")
        print(f"👤 {self.jugador_actual.nombre}: {puntaje_jugador} puntos")
        print(f"🏠 Dealer: {puntaje_dealer} puntos")
        print("=" * 50)

        # Registrar la apuesta
        self.jugador_actual.agregar_historial(f"Apostó ${self.apuesta} en Blackjack")
        
        # Casos de victoria/derrota
        if resultado_jugador == "blackjack" and not self._es_blackjack(self.mano_dealer):
            # Blackjack del jugador (paga 3:2)
            ganancia = int(self.apuesta * 1.5)
            nuevo_saldo = self.jugador_actual.saldo_actual + ganancia
            print(f"🎉 ¡BLACKJACK! ¡Ganaste ${ganancia}!")
            self.jugador_actual.agregar_historial(
                f"Apostó ${self.apuesta} | Ganó ${ganancia} (Blackjack) | Saldo: ${nuevo_saldo}")
            
        elif resultado_jugador == "bust":
            # Jugador se pasó
            nuevo_saldo = self.jugador_actual.saldo_actual - self.apuesta
            print(f"💸 Perdiste ${self.apuesta}. Te pasaste de 21.")
            self.jugador_actual.agregar_historial(
                f"Apostó ${self.apuesta} | Perdió ${self.apuesta} (Bust) | Saldo: ${nuevo_saldo}")
            
        elif resultado_dealer == "bust":
            # Dealer se pasó
            nuevo_saldo = self.jugador_actual.saldo_actual + self.apuesta
            print(f"🎉 ¡Ganaste ${self.apuesta}! El dealer se pasó.")
            self.jugador_actual.agregar_historial(
                f"Apostó ${self.apuesta} | Ganó ${self.apuesta} (Dealer Bust) | Saldo: ${nuevo_saldo}")
            
        elif self._es_blackjack(self.mano_jugador) and self._es_blackjack(self.mano_dealer):
            # Empate con Blackjack
            nuevo_saldo = self.jugador_actual.saldo_actual
            print("🤝 Empate - Ambos tienen Blackjack. Recuperas tu apuesta.")
            self.jugador_actual.agregar_historial(
                f"Apostó ${self.apuesta} | Empató con Blackjack | Saldo: ${nuevo_saldo}"
            )
            
        elif puntaje_jugador > puntaje_dealer:
            # Jugador gana por puntos
            nuevo_saldo = self.jugador_actual.saldo_actual + self.apuesta
            print(f"🎉 ¡Ganaste ${self.apuesta}! Mayor puntaje.")
            self.jugador_actual.agregar_historial(
                f"Apostó ${self.apuesta} | Ganó ${self.apuesta} (Mayor puntaje) | Saldo: ${nuevo_saldo}"
            )
            
        elif puntaje_jugador < puntaje_dealer:
            # Dealer gana por puntos
            nuevo_saldo = self.jugador_actual.saldo_actual - self.apuesta
            print(f"💸 Perdiste ${self.apuesta}. El dealer tiene mayor puntaje.")
            self.jugador_actual.agregar_historial(f"Perdió ${self.apuesta} (Dealer mayor puntaje)")
            
        else:
            # Empate
            nuevo_saldo = self.jugador_actual.saldo_actual
            print("🤝 Empate - Mismo puntaje. Recuperas tu apuesta.")
            self.jugador_actual.agregar_historial(
                f"Apostó ${self.apuesta} | Empató (Mismo puntaje) | Saldo: ${nuevo_saldo}")
        
        # Registrar saldo actualizado
        self.jugador_actual.agregar_historial(f"Saldo actualizado: ${nuevo_saldo}")
         
        # Actualizar saldo del jugador (sin pasar historial)
        self.jugador_actual.saldo_actual = nuevo_saldo

        # Guardar todos los jugadores (incluyendo el historial actualizado)
        jugadores = cargar_jugadores()
        for i, j in enumerate(jugadores):
            if j.id == self.jugador_actual.id:
                jugadores[i] = self.jugador_actual
                break
        guardar_jugadores(jugadores)
        
        
        print(f"💳 Nuevo saldo: ${nuevo_saldo}")
        print("=" * 50)
    
    def jugar_partida_completa(self, id_jugador, apuesta):
        """Juega una partida completa de Blackjack"""
        if not self.iniciar_juego(id_jugador, apuesta):
            return
        
        # Verificar Blackjack inmediato
        if self._es_blackjack(self.mano_jugador):
            self.mostrar_estado_juego(True)
            if self._es_blackjack(self.mano_dealer):
                self.determinar_ganador("blackjack", "blackjack")
            else:
                self.determinar_ganador("blackjack", "stand")
            return
        
        # Turno del jugador
        resultado_jugador = self.turno_jugador()
        
        # Si el jugador no se pasó, juega el dealer
        if resultado_jugador != "bust":
            resultado_dealer = self.turno_dealer()
        else:
            resultado_dealer = "no_play"
        
        # Determinar ganador
        self.determinar_ganador(resultado_jugador, resultado_dealer)


def menu_blackjack():
    """Menú principal del juego Blackjack"""
    juego = BlackjackSimplificado()
    
    while True:
        print("\n" + "=" * 50)
        print("🎰 CASINO - BLACKJACK SIMPLIFICADO")
        print("=" * 50)
        print("1. 🎮 Jugar Blackjack")
        print("2. 📊 Ver reglas")
        print("3. 🚪 Salir")
        print("=" * 50)
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            try:
                id_jugador = input("Ingresa tu ID de jugador: ").strip()
                apuesta = float(input("Ingresa el monto de tu apuesta: $"))
                
                if apuesta <= 0:
                    print("❌ La apuesta debe ser mayor a $0")
                    continue
                
                juego.jugar_partida_completa(id_jugador, apuesta)
                
                # Preguntar si quiere jugar otra partida
                while True:
                    otra = input("\n¿Quieres jugar otra partida? (s/n): ").lower().strip()
                    if otra in ['s', 'si', 'yes', 'y']:
                        break
                    elif otra in ['n', 'no']:
                        break
                    else:
                        print("❌ Responde 's' para sí o 'n' para no.")
                
                if otra in ['n', 'no']:
                    break
                    
            except ValueError:
                print("❌ Por favor ingresa un monto válido.")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif opcion == "2":
            print("\n📋 REGLAS DEL BLACKJACK SIMPLIFICADO:")
            print("=" * 50)
            print("🎯 OBJETIVO: Llegar a 21 o acercarse sin pasarse")
            print("🃏 VALORES:")
            print("   • Números 2-10: Su valor nominal")
            print("   • J, Q, K: Valen 10 puntos")
            print("   • As: Vale 11 o 1 (se ajusta automáticamente)")
            print("\n🎮 CÓMO JUGAR:")
            print("   • Recibes 2 cartas iniciales")
            print("   • El dealer recibe 2 cartas (1 oculta)")
            print("   • Puedes pedir más cartas (Hit) o plantarte (Stand)")
            print("   • El dealer debe pedir carta si tiene menos de 17")
            print("\n🏆 PAGOS:")
            print("   • Blackjack (21 con 2 cartas): Paga 3:2")
            print("   • Victoria normal: Paga 1:1")
            print("   • Empate: Recuperas tu apuesta")
            print("=" * 50)
        
        elif opcion == "3":
            print("👋 ¡Gracias por jugar! ¡Vuelve pronto!")
            break
        
        else:
            print("❌ Opción inválida. Por favor selecciona 1, 2 o 3.")

   