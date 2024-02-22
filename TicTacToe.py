import random

# VARIABLES GLOBALES
jugadores = ["MinMax", "Humano", "Aleatorio"]
contador_min = 0
contador_perdidas = 0

# FUNCIONES MINIMAX

def hay_mas_movimientos(tablero):
    return any(" " in fila for fila in tablero)

def evaluar(tablero, simbolo, oponente):
    for fila in tablero:
        if all(casilla == simbolo for casilla in fila):
            return 10
        elif all(casilla == oponente for casilla in fila):
            return -10

    for col in range(3):
        if all(tablero[fila][col] == simbolo for fila in range(3)):
            return 10
        elif all(tablero[fila][col] == oponente for fila in range(3)):
            return -10

    if all(tablero[i][i] == simbolo for i in range(3)) or all(tablero[i][2 - i] == simbolo for i in range(3)):
        return 10
    elif all(tablero[i][i] == oponente for i in range(3)) or all(tablero[i][2 - i] == oponente for i in range(3)):
        return -10

    return 0

def minimax(tablero, profundidad, es_max, simbolo, oponente):
    puntaje = evaluar(tablero, simbolo, oponente)

    if puntaje in {10, -10}:
        return puntaje
    if not hay_mas_movimientos(tablero):
        return 0

    mejor = float('-inf') if es_max else float('inf')
    for fila in range(3):
        for col in range(3):
            if tablero[fila][col] == " ":
                tablero[fila][col] = simbolo if es_max else oponente
                puntaje_actual = minimax(tablero, profundidad + 1, not es_max, simbolo, oponente)
                tablero[fila][col] = " "
                mejor = max(puntaje_actual, mejor) if es_max else min(puntaje_actual, mejor)
    return mejor

def encontrar_mejor_movimiento(tablero, simbolo, oponente):
    mejor_valor = float('-inf')
    mejores_movimientos = []
    for fila in range(3):
        for col in range(3):
            if tablero[fila][col] == " ":
                tablero[fila][col] = simbolo
                valor_movimiento = minimax(tablero, 0, False, simbolo, oponente)
                tablero[fila][col] = " "
                if valor_movimiento > mejor_valor:
                    mejores_movimientos = [(fila, col)]
                    mejor_valor = valor_movimiento
                elif valor_movimiento == mejor_valor:
                    mejores_movimientos.append((fila, col))
    print("El valor del mejor movimiento es:", mejor_valor)
    print()
    return random.choice(mejores_movimientos)

# FUNCIONES DE TABLERO
def seleccionar_jugadores():
    print("Por favor elige el número de jugadores:")
    for i, jugador in enumerate(jugadores):
        print(f"{i}. {jugador}")
    jugador1 = int(input("Jugador 1: "))
    jugador2 = int(input("Jugador 2: "))
    print(f"El jugador {jugadores[jugador1]} será el símbolo X")
    print(f"El jugador {jugadores[jugador2]} será el símbolo O")
    return {"X": jugador1, "O": jugador2}

def imprimir_tablero(tablero):
    print("Aquí está el tablero de juego:")
    for fila in tablero:
        print(" | ".join(fila))
        print("-" * 9)

def jugar(tablero, simbolo, oponente, funcion_jugada):
    fila, columna = funcion_jugada(tablero, simbolo, oponente)
    tablero[fila][columna] = simbolo

def humano_juega(tablero, simbolo, oponente):
    print("Turno del jugador humano:")
    return int(input("Fila: ")), int(input("Columna: "))

def aleatorio_juega(tablero, simbolo, oponente):
    print("Turno del jugador aleatorio:")
    return random.choice([(fila, columna) for fila in range(3) for columna in range(3) if tablero[fila][columna] == " "])

def minMax_juega(tablero, simbolo, oponente):
    print("Turno del jugador MinMax:")
    return encontrar_mejor_movimiento(tablero, simbolo, oponente)

def main():
    global contador_min, contador_perdidas
    tablero = [[" " for _ in range(3)] for _ in range(3)]
    imprimir_tablero(tablero)
    jugadores_seleccionados = seleccionar_jugadores()
    turno = "X"
    while hay_mas_movimientos(tablero):
        if jugadores_seleccionados[turno] == 0:
            jugar(tablero, turno, "O" if turno == "X" else "X", minMax_juega)
        elif jugadores_seleccionados[turno] == 1:
            jugar(tablero, turno, "O" if turno == "X" else "X", humano_juega)
        else:
            jugar(tablero, turno, "O" if turno == "X" else "X", aleatorio_juega)
        imprimir_tablero(tablero)
        if evaluar(tablero, turno, "O" if turno == "X" else "X") in {10, -10}:
            if jugadores_seleccionados[turno] == 0:
                contador_min += 1
            else:
                contador_perdidas += 1
            print(f"Ganador: {jugadores[jugadores_seleccionados[turno]]}")
            break
        turno = "O" if turno == "X" else "X"
    else:
        print("¡Empate!")

def simulacion_varios_juegos():
    contador_min = 0
    contador_perdidas = 0
    contador_empates = 0
    juegos = 2
    for _ in range(juegos):
        tablero = [[" " for _ in range(3)] for _ in range(3)]
        jugadores_seleccionados = {"X": 0, "O": 2}  # MinMax juega primero
        turno = "X"
        while hay_mas_movimientos(tablero):
            if jugadores_seleccionados[turno] == 0:
                jugar(tablero, turno, "O" if turno == "X" else "X", minMax_juega)
            else:
                jugar(tablero, turno, "O" if turno == "X" else "X", aleatorio_juega)
            if evaluar(tablero, turno, "O" if turno == "X" else "X") in {10, -10}:
                if jugadores_seleccionados[turno] == 0:
                    contador_min += 1
                else:
                    contador_perdidas += 1
                break
            turno = "O" if turno == "X" else "X"
        else:
            # Si el bucle termina sin un ganador, se considera un empate
            contador_empates += 1
    print("\nResultados de la simulación:")
    print(f"Ganadas por MinMax: {contador_min}")
    print(f"Ganadar por Aleatorio: {contador_perdidas}")
    print(f"Empates: {contador_empates}")

if __name__ == "__main__":
    opcion = input("Ingresa 1 para jugar normalmente o 2 para hacer una simulación: ")
    if opcion == "1":
        main()
    elif opcion == "2":
        simulacion_varios_juegos()
    else:
        print("Opción no válida. Por favor ingresa 1 o 2.")
