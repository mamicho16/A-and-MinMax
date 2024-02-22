import random

# VARIABLES GLOBALES
jugadores = ["MinMax", "Humano", "Aleatorio"]  # Lista de jugadores disponibles
contador_min = 0  # Contador para las victorias de MinMax
contador_perdidas = 0  # Contador para las derrotas de MinMax

# FUNCIONES MINIMAX

def hay_mas_movimientos(tablero):
    """
    Verifica si hay más movimientos posibles en el tablero.
    """
    return any(" " in fila for fila in tablero)

def evaluar(tablero, simbolo, oponente):
    """
    Evalúa el estado actual del tablero y asigna un puntaje en función del jugador pasado como parámetro.
    """
    # Revisar filas
    for fila in tablero:
        if all(casilla == simbolo for casilla in fila):
            return 1
        elif all(casilla == oponente for casilla in fila):
            return -1

    # Revisar columnas
    for col in range(3):
        if all(tablero[fila][col] == simbolo for fila in range(3)):
            return 1
        elif all(tablero[fila][col] == oponente for fila in range(3)):
            return -1

    # Revisar diagonales
    if all(tablero[i][i] == simbolo for i in range(3)) or all(tablero[i][2 - i] == simbolo for i in range(3)):
        return 1
    elif all(tablero[i][i] == oponente for i in range(3)) or all(tablero[i][2 - i] == oponente for i in range(3)):
        return -1

    return 0

def minimax(tablero, profundidad, es_max, simbolo, oponente):
    """
    Implementación del algoritmo Minimax para encontrar el mejor movimiento.
    """
    puntaje = evaluar(tablero, simbolo, oponente)

    # Si ya hay un ganador, retorna el puntaje
    if puntaje in {1, -1}:
        return puntaje

    # Si no hay más movimientos posibles, retorna empate
    if not hay_mas_movimientos(tablero):
        return 0

    # Inicializa el mejor puntaje dependiendo de si es una jugada de maximizar o minimizar
    mejor = float('-inf') if es_max else float('inf')

    # Recorre el tablero buscando los espacios vacíos
    for fila in range(3):
        for col in range(3):
            if tablero[fila][col] == " ":
                # Realiza el movimiento y llama recursivamente a minimax
                tablero[fila][col] = simbolo if es_max else oponente
                puntaje_actual = minimax(tablero, profundidad + 1, not es_max, simbolo, oponente)
                tablero[fila][col] = " "  # Deshace el movimiento

                # Actualiza el mejor puntaje
                mejor = max(puntaje_actual, mejor) if es_max else min(puntaje_actual, mejor)

    return mejor

def encontrar_mejor_movimiento(tablero, simbolo, oponente):
    """
    Encuentra el mejor movimiento posible utilizando el algoritmo Minimax.
    """
    mejor_valor = float('-inf')  # Inicializa el mejor valor como menos infinito
    mejores_movimientos = []  # Lista para almacenar los mejores movimientos encontrados

    # Recorre el tablero buscando los espacios vacíos
    for fila in range(3):
        for col in range(3):
            if tablero[fila][col] == " ":
                # Realiza el movimiento y llama a minimax para evaluar el tablero
                tablero[fila][col] = simbolo
                valor_movimiento = minimax(tablero, 0, False, simbolo, oponente)
                tablero[fila][col] = " "  # Deshace el movimiento

                # Actualiza el mejor valor y la lista de mejores movimientos
                if valor_movimiento > mejor_valor:
                    mejores_movimientos = [(fila, col)]
                    mejor_valor = valor_movimiento
                elif valor_movimiento == mejor_valor:
                    mejores_movimientos.append((fila, col))

    # Imprime el valor del mejor movimiento y retorna uno aleatorio entre los mejores movimientos
    print("El valor del mejor movimiento es:", mejor_valor)
    print()
    return random.choice(mejores_movimientos)

# FUNCIONES DE TABLERO
def seleccionar_jugadores():
    """
    Permite al usuario seleccionar los jugadores para la partida.
    """
    print("Por favor elige el número de jugadores:")
    for i, jugador in enumerate(jugadores):
        print(f"{i}. {jugador}")
    jugador1 = int(input("Jugador 1: "))
    jugador2 = int(input("Jugador 2: "))
    print(f"El jugador {jugadores[jugador1]} será el símbolo X")
    print(f"El jugador {jugadores[jugador2]} será el símbolo O")
    return {"X": jugador1, "O": jugador2}

def imprimir_tablero(tablero):
    """
    Imprime el tablero de juego.
    """
    print("Aquí está el tablero de juego:")
    for fila in tablero:
        print(" | ".join(fila))
        print("-" * 9)

def jugar(tablero, simbolo, oponente, funcion_jugada):
    """
    Ejecuta un movimiento en el tablero utilizando la función de jugada proporcionada.
    """
    fila, columna = funcion_jugada(tablero, simbolo, oponente)
    tablero[fila][columna] = simbolo

def humano_juega(tablero, simbolo, oponente):
    """
    Permite al jugador humano realizar un movimiento.
    """
    print("Turno del jugador humano:")
    return int(input("Fila: ")), int(input("Columna: "))

def aleatorio_juega(tablero, simbolo, oponente):
    """
    Realiza un movimiento aleatorio en el tablero.
    """
    print("Turno del jugador aleatorio:")
    return random.choice([(fila, columna) for fila in range(3) for columna in range(3) if tablero[fila][columna] == " "])

def minMax_juega(tablero, simbolo, oponente):
    """
    Permite a MinMax realizar un movimiento utilizando el algoritmo Minimax.
    """
    print("Turno del jugador MinMax:")
    return encontrar_mejor_movimiento(tablero, simbolo, oponente)

def main():
    """
    Función principal para jugar una partida normalmente.
    """
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
        if evaluar(tablero, turno, "O" if turno == "X" else "X") in {1, -1}:
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
    """
    Realiza una simulación de varios juegos entre MinMax y Aleatorio.
    """
    global contador_min, contador_perdidas
    contador_min = 0  # Reinicia el contador de victorias de MinMax
    contador_perdidas = 0  # Reinicia el contador de derrotas de MinMax
    contador_empates = 0  # Contador de empates
    juegos = 500  # Número de juegos a simular
    for _ in range(juegos):
        tablero = [[" " for _ in range(3)] for _ in range(3)]  # Inicializa un nuevo tablero
        jugadores_seleccionados = {"X": 0, "O": 2}  # MinMax juega primero
        turno = "X"  # Inicia el turno en X
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
    print(f"Perdidas contra Aleatorio: {contador_perdidas}")
    print(f"Empates: {contador_empates}")

if __name__ == "__main__":
    opcion = input("Ingresa 1 para jugar normalmente o 2 para hacer una simulación: ")
    if opcion == "1":
        main()
    elif opcion == "2":
        simulacion_varios_juegos()
    else:
        print("Opción no válida. Por favor ingresa 1 o 2.")
