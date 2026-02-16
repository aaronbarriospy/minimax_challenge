import math
import random

# --- CONSTANTES ---
VACIO = '.'
PARED = '#'
GATO = 'G'
RATON = 'R'
QUESO = 'Q'

# --- 1. DEFINE EL TERRENO DE JUEGO ---

def inicializar_juego(ancho, alto, cantidad_paredes=5):
    # Crea un tablero bidimensional (matriz)
    tablero = [[VACIO for _ in range(ancho)] for _ in range(alto)]
    
    # Define el punto de inicio para el gato y el ratón (y el queso)
    posicion_gato = (0, 0)
    posicion_raton = (alto - 1, ancho - 1)
    posicion_queso = (alto // 2, ancho // 2)
    
    tablero[posicion_gato[0]][posicion_gato[1]] = GATO
    tablero[posicion_raton[0]][posicion_raton[1]] = RATON
    tablero[posicion_queso[0]][posicion_queso[1]] = QUESO
    
    # Bonus: Agrega obstáculos en el tablero
    paredes = set()
    contador = 0
    while contador < cantidad_paredes:
        f = random.randint(0, alto - 1)
        c = random.randint(0, ancho - 1)
        if (f, c) not in [posicion_gato, posicion_raton, posicion_queso] and tablero[f][c] == VACIO:
            tablero[f][c] = PARED
            paredes.add((f, c))
            contador += 1
            
    # Retornamos todo el estado empaquetado en un diccionario
    return {
        'tablero': tablero,
        'ancho': ancho,
        'alto': alto,
        'posicion_gato': posicion_gato,
        'posicion_raton': posicion_raton,
        'posicion_queso': posicion_queso
    }

def imprimir_tablero(estado):
    """Bonus: Añade visualizaciones simples del tablero en consola."""
    print("\n" + "="*20)
    for fila in estado['tablero']:
        print(" ".join(fila))
    print("="*20 + "\n")

def obtener_movimientos_validos(estado, posicion):
    """Permite movimientos en 4 direcciones evitando obstáculos."""
    movimientos = []
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Arriba, Abajo, Izquierda, Derecha
    for df, dc in direcciones:
        f, c = posicion[0] + df, posicion[1] + dc
        # Verifica que no se salga del mapa
        if 0 <= f < estado['alto'] and 0 <= c < estado['ancho']:
            if estado['tablero'][f][c] != PARED:
                movimientos.append((f, c))
    # Permitimos que la entidad decida quedarse quieta
    movimientos.append(posicion) 
    return movimientos

def mover_entidad(estado, entidad, posicion_vieja, posicion_nueva):
    """Actualiza la matriz y las coordenadas en el diccionario de estado."""
    if posicion_vieja != posicion_nueva:
        estado['tablero'][posicion_vieja[0]][posicion_vieja[1]] = VACIO
        
        # Si el gato pasa por encima del queso, el queso debe seguir ahí
        if posicion_vieja == estado['posicion_queso'] and entidad != RATON:
             estado['tablero'][posicion_vieja[0]][posicion_vieja[1]] = QUESO
             
        estado['tablero'][posicion_nueva[0]][posicion_nueva[1]] = entidad
        
        if entidad == GATO:
            estado['posicion_gato'] = posicion_nueva
        elif entidad == RATON:
            estado['posicion_raton'] = posicion_nueva

# --- 2. IMPLEMENTA EL ALGORITMO MINIMAX ---

def distancia_manhattan(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def evaluar_estado(estado):
    """
    Evalúa quién va ganando.
    El ratón (Maximizador) quiere puntajes altos.
    El gato (Minimizador) quiere puntajes bajos.
    """
    distancia_gato_raton = distancia_manhattan(estado['posicion_gato'], estado['posicion_raton'])
    distancia_raton_queso = distancia_manhattan(estado['posicion_raton'], estado['posicion_queso'])

    # Condiciones de victoria (Punto 4)
    if estado['posicion_gato'] == estado['posicion_raton']:
        return -1000  # Gato atrapó al ratón (Pésimo para el ratón)
    if estado['posicion_raton'] == estado['posicion_queso']:
        return 1000   # Ratón consiguió el queso (Excelente para el ratón)

    # Lógica pura: El ratón maximiza alejarse del gato y acercarse al queso
    puntaje = (distancia_gato_raton * 10) - (distancia_raton_queso * 5)
    return puntaje

def minimax(estado, profundidad, alfa, beta, es_maximizador):
    """
    Algoritmo Minimax con Optimización (Poda Alfa-Beta).
    Cada nodo es un estado, cada rama un movimiento.
    """
    # Condición de parada
    if profundidad == 0 or estado['posicion_gato'] == estado['posicion_raton'] or estado['posicion_raton'] == estado['posicion_queso']:
        return evaluar_estado(estado), None

    if es_maximizador: # Turno del Ratón (Busca el valor Máximo)
        evaluacion_maxima = -math.inf
        mejor_movimiento = estado['posicion_raton']
        
        for movimiento in obtener_movimientos_validos(estado, estado['posicion_raton']):
            posicion_vieja = estado['posicion_raton']
            mover_entidad(estado, RATON, posicion_vieja, movimiento) # Simula el movimiento
            
            evaluacion, _ = minimax(estado, profundidad - 1, alfa, beta, False)
            
            mover_entidad(estado, RATON, movimiento, posicion_vieja) # Deshace el movimiento (Backtracking)
            
            if evaluacion > evaluacion_maxima:
                evaluacion_maxima = evaluacion
                mejor_movimiento = movimiento
                
            alfa = max(alfa, evaluacion)
            if beta <= alfa:
                break # Optimización: Poda Alfa-Beta
        return evaluacion_maxima, mejor_movimiento

    else: # Turno del Gato (Busca el valor Mínimo)
        evaluacion_minima = math.inf
        mejor_movimiento = estado['posicion_gato']
        
        for movimiento in obtener_movimientos_validos(estado, estado['posicion_gato']):
            posicion_vieja = estado['posicion_gato']
            mover_entidad(estado, GATO, posicion_vieja, movimiento) # Simula el movimiento
            
            evaluacion, _ = minimax(estado, profundidad - 1, alfa, beta, True)
            
            mover_entidad(estado, GATO, movimiento, posicion_vieja) # Deshace el movimiento
            
            if evaluacion < evaluacion_minima:
                evaluacion_minima = evaluacion
                mejor_movimiento = movimiento
                
            beta = min(beta, evaluacion)
            if beta <= alfa:
                break # Optimización: Poda Alfa-Beta
        return evaluacion_minima, mejor_movimiento

# --- 3. SIMULACIÓN DE MOVIMIENTO (FASES INICIALES) ---

def movimiento_aleatorio_raton(estado):
    """Comienza con un ratón que se mueve al azar (aún no ha despertado)."""
    movimientos = obtener_movimientos_validos(estado, estado['posicion_raton'])
    return random.choice(movimientos)

# --- BUCLE PRINCIPAL DEL JUEGO ---

def jugar():
    print("🧀 ¡BIENVENIDO AL LABERINTO DEL GATO Y EL RATÓN! 🐱")
    print("1. Jugar como el Gato (Cazar al Ratón IA)")
    print("2. Jugar como el Ratón (Escapar del Gato IA)")
    print("3. IA vs IA")
    
    eleccion = input("Elige tu rol (1/2/3): ")
    dificultad = int(input("Elige la dificultad (Profundidad Minimax, ej: 3, 5): "))
    turnos_maximos = int(input("¿Límite de turnos? (ej: 20): "))
    
    # Define cuándo termina el juego (Punto 4)
    estado = inicializar_juego(6, 6, cantidad_paredes=5)
    turno = 0
    
    while turno < turnos_maximos:
        imprimir_tablero(estado)
        print(f"--- Turno {turno + 1}/{turnos_maximos} ---")
        
        # --- MOVIMIENTO DEL RATÓN ---
        if eleccion == '2': # Humano
            print("Movimientos válidos:", obtener_movimientos_validos(estado, estado['posicion_raton']))
            f = int(input("Fila: "))
            c = int(input("Columna: "))
            nuevo_movimiento_raton = (f, c)
        else: # IA
            if turno < 2:
                # El ratón huye al azar primero
                nuevo_movimiento_raton = movimiento_aleatorio_raton(estado)
                print("El ratón se mueve al azar (Instinto inicial).")
            else:
                # El ratón se transforma en una mente brillante
                print("El ratón IA está calculando su escape...")
                _, nuevo_movimiento_raton = minimax(estado, dificultad, -math.inf, math.inf, True)
                
        mover_entidad(estado, RATON, estado['posicion_raton'], nuevo_movimiento_raton)
        
        if estado['posicion_raton'] == estado['posicion_queso']:
            imprimir_tablero(estado)
            print("🎉 ¡EL RATÓN CONSIGUIÓ EL QUESO Y ESCAPÓ!")
            return
        if estado['posicion_raton'] == estado['posicion_gato']:
            imprimir_tablero(estado)
            print("💀 ¡EL GATO ATRAPÓ AL RATÓN!")
            return

        # --- MOVIMIENTO DEL GATO ---
        if eleccion == '1': # Humano
            imprimir_tablero(estado)
            print("Movimientos válidos:", obtener_movimientos_validos(estado, estado['posicion_gato']))
            f = int(input("Fila: "))
            c = int(input("Columna: "))
            nuevo_movimiento_gato = (f, c)
        else: # IA
            print("El Gato IA está acechando...")
            # El gato anticipa y traza estrategias
            _, nuevo_movimiento_gato = minimax(estado, dificultad, -math.inf, math.inf, False)
            
        mover_entidad(estado, GATO, estado['posicion_gato'], nuevo_movimiento_gato)
        
        if estado['posicion_gato'] == estado['posicion_raton']:
            imprimir_tablero(estado)
            print("💀 ¡EL GATO ATRAPÓ AL RATÓN!")
            return
            
        turno += 1

    print("⏳ ¡TIEMPO AGOTADO! El ratón sobrevivió los turnos requeridos.")

if __name__ == "__main__":
    jugar()