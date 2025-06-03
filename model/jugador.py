import json
#Definir la clase del jugador
class Jugador:
    def __init__(self, nombre, id, saldo_inicial):
        self.nombre = nombre
        self.id = id
        self.saldo_inicial = float(saldo_inicial)
        self.saldo_actual = float(saldo_inicial)
        self.historial = [] # Lista en la que guardaremos el hsitorial 
    
    def agregar_historial(self, actividad):#Fubncion a la que entra el objeto y actividad
       # Agrega una actividad al historial del jugador (máx 10 elementos).
        self.historial.append(actividad)# ->Añadir en el historial la actividad 
        if len(self.historial) > 10:
            self.historial.pop(0) # Eliminar el ultimo registro 

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "id": self.id,
            "saldo_inicial": self.saldo_inicial,
            "saldo_actual": self.saldo_actual,
            "historial": self.historial
        }

    @staticmethod
    def from_dict(data):
        jugador = Jugador(data["nombre"], data["id"], data["saldo_inicial"])
        jugador.saldo_actual = data.get("saldo_actual", jugador.saldo_inicial)
        jugador.historial = data.get("historial", [])
        return jugador

    def __str__(self):
        return f"Jugador: {self.nombre} | ID: {self.id} | Saldo actual: ${self.saldo_actual:.2f}"