import random  # [001] Importa el módulo "random": viene de la librería estándar de Python y sirve para generar azar (ej: elegir movimientos aleatorios).
import math  # [002] Importa el módulo "math": trae funciones matemáticas (por ejemplo infinito con math.inf).
import time  # [003] Importa el módulo "time": sirve para pausar el programa (por ejemplo para ver el tablero más lento).
from collections import deque  # [004] Importa "deque" desde "collections": deque es una cola doble muy eficiente; la usamos en BFS para sacar/poner elementos rápido.


# ------------------------------
# DIRECCIONES DE MOVIMIENTO
# ------------------------------

DIRECCIONES_4 = [  # [005] Esto es una LISTA (list) en Python: una colección ordenada y modificable.
    (-1, 0),  # [006] Tupla (tuple) fila-columna: moverse arriba (fila - 1).
    (1, 0),   # [007] Abajo (fila + 1).
    (0, -1),  # [008] Izquierda (columna - 1).
    (0, 1),   # [009] Derecha (columna + 1).
]  # [010] Cierre de la lista de 4 direcciones.

DIRECCIONES_8 = DIRECCIONES_4 + [  # [011] Crea una lista nueva: toma DIRECCIONES_4 y le "suma" más direcciones (concatenación de listas).
    (-1, -1),  # [012] Arriba-izquierda (diagonal).
    (-1, 1),   # [013] Arriba-derecha (diagonal).
    (1, -1),   # [014] Abajo-izquierda (diagonal).
    (1, 1),    # [015] Abajo-derecha (diagonal).
]  # [016] Ahora tenemos 8 direcciones posibles.


# ------------------------------
# TABLERO 
# ------------------------------

def crear_tablero(filas, columnas, obstaculos, diagonales, queso):  # [017] Definimos una FUNCIÓN. Las funciones agrupan lógica reutilizable.
    """Crea un tablero 2D como diccionario (sin clases)."""  # [018] Docstring: texto para explicar qué hace la función (opcional pero útil).
    return {  # [019] "return" devuelve un valor. Acá devolvemos un DICCIONARIO (dict): pares clave→valor.
        "filas": filas,  # [020] Guardamos cantidad de filas del tablero.
        "columnas": columnas,  # [021] Guardamos cantidad de columnas del tablero.
        "obstaculos": set(obstaculos),  # [022] set() crea un CONJUNTO (set): colección sin repetidos y rápida para buscar "¿está?".
        "diagonales": diagonales,  # [023] Guardamos si se permiten diagonales (True/False).
        "direcciones": DIRECCIONES_8 if diagonales else DIRECCIONES_4,  # [024] Operador ternario: si diagonales True usa 8, si no usa 4.
        "queso": queso,  # [025] Posición del queso o None (None significa "no hay queso").
    }  # [026] Fin del diccionario del tablero.


def es_posicion_valida(tablero, posicion):  # [027] Función que valida si una celda se puede usar (no sale del tablero y no es obstáculo).
    f, c = posicion  # [028] Desempaquetado: posicion es una tupla (f, c); la separamos en variables f y c.
    return (  # [029] Devuelve True/False. Aquí usamos una expresión booleana compuesta.
        0 <= f < tablero["filas"]  # [030] Verifica que la fila esté dentro de [0, filas-1].
        and 0 <= c < tablero["columnas"]  # [031] Verifica que la columna esté dentro de [0, columnas-1].
        and posicion not in tablero["obstaculos"]  # [032] Verifica que la posición NO esté en el set de obstáculos.
    )  # [033] Fin del return booleando.


def vecinos(tablero, posicion):  # [034] Función que genera movimientos posibles desde una posición: esto son las "ramas" del árbol en Minimax.
    f, c = posicion  # [035] Separamos fila/columna.
    lista = []  # [036] Creamos una lista vacía donde guardaremos vecinos válidos.
    for df, dc in tablero["direcciones"]:  # [037] "for" recorre cada dirección (df, dc). df = delta fila, dc = delta columna.
        nueva = (f + df, c + dc)  # [038] Calculamos la nueva posición sumando el desplazamiento.
        if es_posicion_valida(tablero, nueva):  # [039] "if" verifica condición: si la nueva posición es legal...
            lista.append(nueva)  # [040] .append agrega un elemento al final de la lista.
    return lista  # [041] Devolvemos todas las posiciones a las que se puede mover.


def dibujar_tablero(tablero, gato, raton):  # [042] Función BONUS: dibuja el tablero en texto para ver la simulación.
    lineas = []  # [043] Guardaremos cada fila como string en esta lista.
    for f in range(tablero["filas"]):  # [044] range(n) genera 0..n-1. Recorremos cada fila.
        fila = []  # [045] Lista de símbolos para esta fila.
        for c in range(tablero["columnas"]):  # [046] Recorremos cada columna.
            p = (f, c)  # [047] La celda actual.
            ch = "."  # [048] Por defecto dibujamos "." como espacio vacío.
            if p in tablero["obstaculos"]:  # [049] Si la celda es un obstáculo...
                ch = "#"  # [050] Dibujamos "#".
            if tablero["queso"] is not None and p == tablero["queso"]:  # [051] Si hay queso y estamos en su celda...
                ch = "Q"  # [052] Dibujamos "Q".
            if p == raton:  # [053] Si el ratón está aquí...
                ch = "M"  # [054] Dibujamos "M".
            if p == gato:  # [055] Si el gato está aquí...
                ch = "X" if p == raton else "C"  # [056] Si coincide con ratón: "X" (atrapado). Si no: "C" (gato).
            fila.append(ch)  # [057] Agregamos el símbolo de esta celda a la fila.
        lineas.append(" ".join(fila))  # [058] Convertimos la fila en string uniendo con espacios (para que se vea prolijo).
    return "\n".join(lineas)  # [059] Unimos todas las filas con saltos de línea.


# ------------------------------
# DISTANCIAS (BFS) para heurística y estrategia
# ------------------------------

def distancia_bfs(tablero, inicio, objetivo):  # [060] BFS = Breadth-First Search (búsqueda en anchura). Encuentra el camino más corto en un grafo sin pesos.
    if inicio == objetivo:  # [061] Caso simple: si ya estamos en el objetivo...
        return 0  # [062] Distancia 0.

    cola = deque([inicio])  # [063] Creamos una cola (deque) con el inicio. deque es eficiente para popleft().
    dist = {inicio: 0}  # [064] Diccionario de distancias: dist[posicion] = pasos desde inicio. Iniciamos con 0.

    while cola:  # [065] Mientras la cola no esté vacía...
        actual = cola.popleft()  # [066] Sacamos el primer elemento (FIFO). popleft() en deque es O(1) aprox.
        for sig in vecinos(tablero, actual):  # [067] Recorremos los vecinos del nodo actual.
            if sig in dist:  # [068] Si ya visitamos esa celda...
                continue  # [069] "continue" salta a la siguiente iteración del for.
            dist[sig] = dist[actual] + 1  # [070] Guardamos distancia al vecino: la del actual + 1 paso.
            if sig == objetivo:  # [071] Si ya llegamos al objetivo...
                return dist[sig]  # [072] Devolvemos la distancia mínima encontrada.
            cola.append(sig)  # [073] Si no es objetivo, lo encolamos para seguir explorando más adelante.

    return tablero["filas"] * tablero["columnas"] + 999  # [074] Si no hay camino, devolvemos un número grande (como “infinito práctico”).


# ------------------------------
# CONDICIONES DE FINALIZACIÓN (terminales)
# ------------------------------

def es_terminal(tablero, gato, raton, pasos_restantes):  # [075] Devuelve un puntaje si el juego terminó; si no terminó devuelve None.
    if gato == raton:  # [076] Condición 1: el gato atrapó al ratón (misma celda).
        return -10000  # [077] Puntaje MUY negativo para el ratón: perder (Minimax lo evitará).

    if tablero["queso"] is not None and raton == tablero["queso"]:  # [078] Condición BONUS: el ratón llegó al queso.
        return 10000  # [079] Puntaje MUY positivo para el ratón: ganar.

    if pasos_restantes <= 0:  # [080] Condición 2: se acabaron los pasos/turnos -> el ratón escapó tras X turnos.
        return 5000  # [081] Puntaje positivo (no tan alto como el queso, pero gana por supervivencia).

    return None  # [082] None significa: "no es terminal todavía".


# ------------------------------
# FUNCIÓN DE EVALUACIÓN (heurística)
# ------------------------------
# Heurística = una “estimación inteligente” cuando no llegamos al final del juego.
# Minimax necesita un número para comparar estados cuando se corta por profundidad.
# ------------------------------

def evaluar_estado(tablero, gato, raton, pasos_restantes):  # [083] Devuelve un puntaje del estado (qué tan bueno es para el ratón).
    terminal = es_terminal(tablero, gato, raton, pasos_restantes)  # [084] Primero revisamos si el juego ya terminó.
    if terminal is not None:  # [085] Si terminal no es None, significa que terminó...
        return terminal  # [086] Devolvemos el puntaje final directamente.

    d_gato_raton = distancia_bfs(tablero, gato, raton)  # [087] Distancia real entre gato y ratón (con obstáculos).
    if tablero["queso"] is None:  # [088] Si no hay queso activo...
        d_raton_queso = 0  # [089] No aportamos nada por queso.
    else:  # [090] Si sí hay queso...
        d_raton_queso = distancia_bfs(tablero, raton, tablero["queso"])  # [091] Distancia del ratón al queso.

    # [092] Construimos el puntaje:
    # - Más lejos del gato (d_gato_raton grande) es mejor => lo multiplicamos por 3.
    # - Más pasos restantes también es mejor => lo multiplicamos por 2.
    # - Si hay queso: mientras más cerca del queso (d_raton_queso chico), mejor => lo RESTAMOS.
    return (3 * d_gato_raton) + (2 * pasos_restantes) - d_raton_queso  # [093] Esto define el “criterio” de decisión del ratón.


# ------------------------------
# MINIMAX con poda alpha-beta y memoización
# ------------------------------
# Minimax: algoritmo para juegos de 2 jugadores con objetivos opuestos.
# - El ratón (MAX) intenta MAXIMIZAR el puntaje.
# - El gato (MIN) intenta MINIMIZAR el puntaje del ratón.
#
# Alpha-beta: técnica para podar ramas que ya no pueden mejorar el resultado.
# Memoización: guardar resultados ya calculados para no recomputar (optimización).
# ------------------------------

def minimax(tablero, gato, raton, pasos_restantes, jugador, profundidad, alfa, beta, memo):  # [094] Función recursiva: se llama a sí misma.
    clave = (gato, raton, jugador, profundidad, pasos_restantes)  # [095] La "clave" identifica un estado+parámetros para memoización.
    if clave in memo:  # [096] Si ya calculamos este caso...
        return memo[clave]  # [097] Devolvemos el resultado guardado.

    terminal = es_terminal(tablero, gato, raton, pasos_restantes)  # [098] Revisamos si el estado es final.
    if terminal is not None or profundidad == 0:  # [099] Si es final o si llegamos al límite de profundidad...
        valor = evaluar_estado(tablero, gato, raton, pasos_restantes)  # [100] Evaluamos con heurística o valor final.
        memo[clave] = valor  # [101] Guardamos en memo para reutilizar.
        return valor  # [102] Devolvemos el valor.

    if jugador == "raton":  # [103] Turno del ratón: quiere maximizar (MAX).
        mejor = -math.inf  # [104] Iniciamos con -infinito: cualquier cosa será mejor que esto.
        opciones = vecinos(tablero, raton)  # [105] Todas las jugadas posibles del ratón.

        if not opciones:  # [106] Si no hay movimientos posibles (atrapado por obstáculos)...
            valor = evaluar_estado(tablero, gato, raton, pasos_restantes)  # [107] Evaluamos como está.
            memo[clave] = valor  # [108] Guardamos.
            return valor  # [109] Devolvemos.

        for mov in opciones:  # [110] Probamos cada movimiento posible del ratón.
            valor = minimax(  # [111] Calculamos el valor futuro si el ratón se mueve a "mov".
                tablero,  # [112] Pasamos el mismo tablero.
                gato,  # [113] El gato no se movió todavía en esta mitad.
                mov,  # [114] Nuevo ratón.
                pasos_restantes - 1,  # [115] Consumimos 1 paso (porque se hizo una decisión/movimiento).
                "gato",  # [116] Próximo jugador: gato.
                profundidad - 1,  # [117] Bajamos profundidad del árbol: nos acercamos al corte.
                alfa,  # [118] Pasamos alfa actual.
                beta,  # [119] Pasamos beta actual.
                memo,  # [120] Pasamos el diccionario memo para reutilizar resultados.
            )  # [121] Fin de la llamada recursiva.
            mejor = max(mejor, valor)  # [122] MAX: el ratón se queda con el mejor valor (más alto).
            alfa = max(alfa, mejor)  # [123] Actualizamos alfa: lo mejor que el MAX puede asegurar.
            if beta <= alfa:  # [124] Condición de poda alpha-beta: si ya no puede mejorar...
                break  # [125] Cortamos el for (no analizamos más ramas).

        memo[clave] = int(mejor)  # [126] Guardamos el resultado final del mejor movimiento del ratón.
        return memo[clave]  # [127] Devolvemos.

    # [128] Si no era turno del ratón, entonces es turno del gato: minimiza (MIN).
    mejor = math.inf  # [129] Iniciamos con +infinito: cualquier cosa será menor.
    opciones = vecinos(tablero, gato)  # [130] Movimientos posibles del gato.

    if not opciones:  # [131] Si el gato no tiene movimientos (muy raro, pero posible con obstáculos)...
        valor = evaluar_estado(tablero, gato, raton, pasos_restantes)  # [132] Evaluamos.
        memo[clave] = valor  # [133] Guardamos.
        return valor  # [134] Devolvemos.

    for mov in opciones:  # [135] Probamos cada movimiento posible del gato.
        valor = minimax(  # [136] Calculamos el valor futuro si el gato se mueve.
            tablero,  # [137] Tablero igual.
            mov,  # [138] Nuevo gato.
            raton,  # [139] Ratón sin cambiar en esta mitad.
            pasos_restantes - 1,  # [140] Consumimos 1 paso.
            "raton",  # [141] Próximo jugador: ratón.
            profundidad - 1,  # [142] Bajamos profundidad.
            alfa,  # [143] Alfa actual.
            beta,  # [144] Beta actual.
            memo,  # [145] Memo.
        )  # [146] Fin llamada.
        mejor = min(mejor, valor)  # [147] MIN: el gato elige el menor valor (peor para el ratón).
        beta = min(beta, mejor)  # [148] Actualizamos beta: lo mejor que el MIN puede asegurar.
        if beta <= alfa:  # [149] Poda alpha-beta.
            break  # [150] Cortamos ramas que no pueden cambiar el resultado.

    memo[clave] = int(mejor)  # [151] Guardamos el mejor resultado para el gato.
    return memo[clave]  # [152] Devolvemos.


# ------------------------------
# ELEGIR EL MEJOR MOVIMIENTO inmediato
# ------------------------------

def mejor_movimiento(tablero, gato, raton, pasos_restantes, jugador, profundidad):  # [153] Decide la jugada actual usando Minimax.
    memo = {}  # [154] Creamos memo nuevo para esta decisión (cache local de la búsqueda).

    if jugador == "raton":  # [155] Si quien elige es el ratón...
        opciones = vecinos(tablero, raton)  # [156] Lista de movimientos del ratón.
        if not opciones:  # [157] Si no hay opciones...
            return raton  # [158] Se queda en el mismo lugar (no puede moverse).

        mejor_valor = -math.inf  # [159] MAX: arrancamos con -infinito.
        mejor_mov = opciones[0]  # [160] Guardamos un movimiento inicial como “mejor” para tener algo por defecto.

        for mov in opciones:  # [161] Probamos cada posible movimiento.
            valor = minimax(  # [162] Evaluamos el futuro suponiendo que elegimos este movimiento.
                tablero,  # [163] Tablero.
                gato,  # [164] Gato sin moverse todavía.
                mov,  # [165] Ratón movido.
                pasos_restantes - 1,  # [166] Consumimos 1 paso.
                "gato",  # [167] Próximo: gato.
                profundidad - 1,  # [168] Menos profundidad.
                -10**9,  # [169] Alfa inicial muy bajo (como -infinito).
                10**9,  # [170] Beta inicial muy alto (como +infinito).
                memo,  # [171] Memo.
            )  # [172] Fin.
            if valor > mejor_valor:  # [173] Si este movimiento da un valor mejor...
                mejor_valor = valor  # [174] Actualizamos el mejor valor.
                mejor_mov = mov  # [175] Guardamos este movimiento como el mejor.
        return mejor_mov  # [176] Devolvemos el movimiento que MAX prefiere.

    # [177] Si no era ratón, entonces es gato.
    opciones = vecinos(tablero, gato)  # [178] Movimientos del gato.
    if not opciones:  # [179] Si no hay opciones...
        return gato  # [180] Se queda.

    mejor_valor = math.inf  # [181] MIN: arrancamos con +infinito.
    mejor_mov = opciones[0]  # [182] Movimiento por defecto.

    for mov in opciones:  # [183] Probamos cada movimiento del gato.
        valor = minimax(  # [184] Evaluamos el futuro si el gato hace este movimiento.
            tablero,  # [185] Tablero.
            mov,  # [186] Nuevo gato.
            raton,  # [187] Ratón igual.
            pasos_restantes - 1,  # [188] Consumimos 1 paso.
            "raton",  # [189] Próximo: ratón.
            profundidad - 1,  # [190] Menos profundidad.
            -10**9,  # [191] Alfa inicial.
            10**9,  # [192] Beta inicial.
            memo,  # [193] Memo.
        )  # [194] Fin.
        if valor < mejor_valor:  # [195] MIN elige el valor más chico.
            mejor_valor = valor  # [196] Actualizamos mejor valor.
            mejor_mov = mov  # [197] Guardamos movimiento.
    return mejor_mov  # [198] Devolvemos la decisión del gato.


# ------------------------------
# ESTRATEGIA “CODICIOSA” (greedy)
# ------------------------------
# Greedy = “elige lo que parece mejor ahora” sin mirar muchas jugadas adelante.
# Es más rápido que Minimax pero menos inteligente.
# ------------------------------

def movimiento_codicioso(tablero, inicio, objetivo):  # [199] Devuelve el vecino que más reduce la distancia BFS al objetivo.
    mejor = inicio  # [200] Inicialmente “mejor” es quedarse (por si no hay mejora).
    mejor_d = distancia_bfs(tablero, inicio, objetivo)  # [201] Distancia actual.
    for mov in vecinos(tablero, inicio):  # [202] Probamos moverse a cada vecino.
        d = distancia_bfs(tablero, mov, objetivo)  # [203] Distancia si nos movemos ahí.
        if d < mejor_d:  # [204] Si mejora (más cerca)...
            mejor = mov  # [205] Actualizamos mejor movimiento.
            mejor_d = d  # [206] Actualizamos mejor distancia.
    return mejor  # [207] Devolvemos el movimiento elegido.


# ------------------------------
# MOVIMIENTO HUMANO (interfaz por texto)
# ------------------------------

def movimiento_humano(tablero, quien, posicion_actual):  # [208] Permite que un humano decida la jugada con teclado.
    teclas = {  # [209] Diccionario tecla→desplazamiento.
        "w": (-1, 0),  # [210] w = arriba
        "s": (1, 0),   # [211] s = abajo
        "a": (0, -1),  # [212] a = izquierda
        "d": (0, 1),   # [213] d = derecha
        "q": (-1, -1), # [214] q = arriba-izquierda
        "e": (-1, 1),  # [215] e = arriba-derecha
        "z": (1, -1),  # [216] z = abajo-izquierda
        "c": (1, 1),   # [217] c = abajo-derecha
    }  # [218] Fin diccionario.

    permitidas = ["w", "a", "s", "d"]  # [219] Teclas básicas (4 direcciones).
    if tablero["diagonales"]:  # [220] Si diagonales está activado...
        permitidas += ["q", "e", "z", "c"]  # [221] Agregamos diagonales.

    while True:  # [222] Loop infinito hasta que el usuario haga un movimiento válido.
        cmd = input(f"{quien} mueve ({'/'.join(permitidas)}): ").strip().lower()  # [223] Leemos entrada; strip saca espacios; lower pasa a minúsculas.
        if cmd not in permitidas:  # [224] Si la tecla no está permitida...
            print("Entrada inválida.")  # [225] Avisamos.
            continue  # [226] Volvemos a pedir.

        df, dc = teclas[cmd]  # [227] Buscamos el desplazamiento asociado a la tecla.
        nueva = (posicion_actual[0] + df, posicion_actual[1] + dc)  # [228] Calculamos la nueva posición.

        if es_posicion_valida(tablero, nueva):  # [229] Si esa posición es válida...
            return nueva  # [230] La devolvemos como movimiento final.

        print("Bloqueado o fuera del tablero.")  # [231] Si no es válida, avisamos y seguimos en el while.


# ------------------------------
# GENERAR TABLERO aleatorio con obstáculos y queso (bonus)
# ------------------------------

def generar_tablero_aleatorio(  # [232] Función para construir tableros variados para pruebas (requisito “pruebas con tableros de distintos tamaños”).
    semilla,  # [233] semilla = número para que el azar sea repetible (mismo tablero si repetís la semilla).
    filas,  # [234] Tamaño tablero.
    columnas,  # [235] Tamaño tablero.
    densidad_obstaculos,  # [236] Proporción de celdas que serán obstáculos (0.0 a 0.35 recomendado).
    diagonales,  # [237] Permitir 4 u 8 direcciones.
    gato_inicio,  # [238] Posición inicial del gato.
    raton_inicio,  # [239] Posición inicial del ratón.
    activar_queso,  # [240] Si True, colocamos queso en una celda libre.
):  # [241] Fin de parámetros.
    rng = random.Random(semilla)  # [242] Creamos un generador de azar local con semilla (reproducible).
    celdas = []  # [243] Lista donde pondremos todas las celdas (f, c).
    for f in range(filas):  # [244] Recorremos filas.
        for c in range(columnas):  # [245] Recorremos columnas.
            celdas.append((f, c))  # [246] Agregamos cada celda a la lista.

    protegidas = {gato_inicio, raton_inicio}  # [247] Set de celdas que NO queremos bloquear (inicio del gato y ratón).
    cantidad = int(densidad_obstaculos * filas * columnas)  # [248] Número total de obstáculos calculado por densidad.

    tablero_final = None  # [249] Por si fallamos los reintentos, guardamos el último tablero generado.

    for _ in range(60):  # [250] Reintentamos hasta 60 veces para evitar tableros sin movimientos desde el inicio.
        candidatas = [p for p in celdas if p not in protegidas]  # [251] Lista por comprensión: celdas donde sí podemos poner obstáculos.
        k = min(cantidad, max(0, len(candidatas)))  # [252] k = cantidad real que podemos poner (sin pasarnos del tamaño).
        if k > 0:  # [253] Si hay obstáculos que poner...
            obstaculos = set(rng.sample(candidatas, k=k))  # [254] sample elige k elementos SIN repetir.
        else:  # [255] Si k es 0...
            obstaculos = set()  # [256] Set vacío.

        queso = None  # [257] Por defecto no hay queso.
        if activar_queso:  # [258] Si queremos queso...
            libres = [p for p in celdas if p not in obstaculos and p not in protegidas]  # [259] Celdas libres donde puede ir el queso.
            queso = rng.choice(libres) if libres else None  # [260] choice elige 1 elemento al azar; si no hay libres, queda None.

        tablero = crear_tablero(filas, columnas, obstaculos, diagonales, queso)  # [261] Construimos el tablero final.
        tablero_final = tablero  # [262] Guardamos como “último intento”.

        if vecinos(tablero, gato_inicio) and vecinos(tablero, raton_inicio):  # [263] Verificamos que ambos tengan al menos un movimiento posible.
            return tablero  # [264] Si está ok, devolvemos este tablero.

    return tablero_final  # [265] Si no se pudo encontrar uno perfecto, devolvemos el último generado.


# ------------------------------
# FUNCIÓN para pedir datos con valor por defecto
# ------------------------------

def pedir(texto, convertir, por_defecto):  # [266] Pedimos un input al usuario y lo convertimos a int/float/str.
    entrada = input(f"{texto} [{por_defecto}]: ").strip()  # [267] Mostramos el texto y el default; strip quita espacios.
    if entrada == "":  # [268] Si el usuario no escribió nada...
        return por_defecto  # [269] Devolvemos el valor por defecto.
    return convertir(entrada)  # [270] Convertimos el texto al tipo deseado (int/float/str) y devolvemos.


# ------------------------------
# SIMULACIÓN DEL JUEGO (turno a turno)
# ------------------------------

def jugar(  # [271] Ejecuta el juego completo con turnos, finalización y decisiones del gato/ratón.
    tablero,  # [272] Tablero con filas/columnas/obstáculos/queso/direcciones.
    gato_inicio,  # [273] Posición inicial del gato.
    raton_inicio,  # [274] Posición inicial del ratón.
    turnos_maximos,  # [275] Condición de escape: si pasan X turnos, gana el ratón.
    dificultad,  # [276] Texto: "facil", "medio" o "dificil".
    profundidad,  # [277] Profundidad del árbol Minimax (más profundidad = más lento pero más inteligente).
    turnos_azar_raton,  # [278] Cuántos turnos el ratón se mueve aleatorio antes de volverse “inteligente”.
    humano,  # [279] "ninguno", "gato" o "raton" (bonus: interfaz por texto).
    pausa_segundos,  # [280] Pausa opcional entre turnos.
):  # [281] Fin parámetros.
    gato = gato_inicio  # [282] Guardamos posición actual del gato.
    raton = raton_inicio  # [283] Guardamos posición actual del ratón.

    # [284] Cada turno tiene 2 “medios turnos”: primero mueve ratón y luego mueve gato.
    # [285] Esto lo usamos para contar pasos y que la condición "pasos_restantes <= 0" represente el fin del tiempo.
    pasos_restantes = turnos_maximos * 2  # [286] Total de decisiones posibles en toda la partida.

    rng = random.Random()  # [287] Generador de azar sin semilla fija (solo para movimientos aleatorios durante el juego).
    for t in range(1, turnos_maximos + 1):  # [288] Loop de turnos completos (1..turnos_maximos).
        if pausa_segundos:  # [289] Si pausa_segundos no es 0...
            time.sleep(pausa_segundos)  # [290] Pausamos para ver el tablero más lento.

        print(f"\n=== Turno {t}/{turnos_maximos} ===")  # [291] Encabezado del turno.
        print(dibujar_tablero(tablero, gato, raton))  # [292] Dibujamos tablero actual.

        # -------- Turno del RATÓN --------
        if humano == "raton":  # [293] Si el humano controla al ratón...
            raton = movimiento_humano(tablero, "Ratón", raton)  # [294] Pedimos movimiento por teclado.
        elif t <= turnos_azar_raton or dificultad == "facil":  # [295] Si está en “modo random” o dificultad fácil...
            opciones = vecinos(tablero, raton)  # [296] Movimientos posibles.
            raton = rng.choice(opciones) if opciones else raton  # [297] Elegimos al azar (si no hay opciones, se queda).
        else:  # [298] Caso inteligente: usa Minimax.
            raton = mejor_movimiento(tablero, gato, raton, pasos_restantes, "raton", profundidad)  # [299] Decide con Minimax.

        pasos_restantes -= 1  # [300] Consumimos 1 paso (porque se hizo 1 movimiento/decisión).
        fin = es_terminal(tablero, gato, raton, pasos_restantes)  # [301] Revisamos si el juego terminó después del movimiento del ratón.
        if fin is not None:  # [302] Si terminó...
            print(dibujar_tablero(tablero, gato, raton))  # [303] Mostramos estado final.
            return "gato" if gato == raton else "raton"  # [304] Si están en misma celda gana gato, si no gana ratón (queso/escape).

        # -------- Turno del GATO --------
        if humano == "gato":  # [305] Si el humano controla al gato...
            gato = movimiento_humano(tablero, "Gato", gato)  # [306] Pedimos movimiento por teclado.
        elif dificultad in ("facil", "medio"):  # [307] En fácil/medio el gato usa estrategia rápida (codiciosa).
            gato = movimiento_codicioso(tablero, gato, raton)  # [308] Intenta acercarse al ratón.
        else:  # [309] En difícil el gato también usa Minimax.
            gato = mejor_movimiento(tablero, gato, raton, pasos_restantes, "gato", profundidad)  # [310] Decide con Minimax.

        pasos_restantes -= 1  # [311] Consumimos otro paso por el movimiento del gato.
        fin = es_terminal(tablero, gato, raton, pasos_restantes)  # [312] Revisamos si terminó tras el movimiento del gato.
        if fin is not None:  # [313] Si terminó...
            print(dibujar_tablero(tablero, gato, raton))  # [314] Mostramos final.
            return "gato" if gato == raton else "raton"  # [315] Devolvemos ganador.

    print("\nTiempo agotado: el ratón escapa por turnos.")  # [316] Si terminó el for, es porque se agotaron los turnos.
    return "raton"  # [317] Gana el ratón por sobrevivir.


# ------------------------------
# FUNCIÓN PRINCIPAL (entrada del programa)
# ------------------------------

def principal():  # [318] Función que arma la configuración y arranca el juego.
    print("Laberinto del Gato y el Ratón (Minimax) — solo funciones\n")  # [319] Mensaje inicial.

    filas = pedir("Filas", int, 9)  # [320] Pedimos filas; int convierte texto a entero.
    columnas = pedir("Columnas", int, 9)  # [321] Pedimos columnas.
    diagonales = (pedir("¿Movimientos diagonales? (0/1)", int, 0) == 1)  # [322] Convertimos 0/1 a booleano.
    densidad = pedir("Obstáculos (0.00 a 0.35)", float, 0.12)  # [323] float convierte a número decimal.
    turnos = pedir("Turnos máximos (escape)", int, 25)  # [324] Turnos máximos.
    dificultad = pedir("Dificultad (facil/medio/dificil)", str, "dificil").strip().lower()  # [325] Normalizamos texto: sin espacios y en minúsculas.
    humano = pedir("¿Humano controla? (ninguno/gato/raton)", str, "ninguno").strip().lower()  # [326] Quién controla.
    activar_queso = (pedir("¿Activar queso como objetivo? (0/1)", int, 1) == 1)  # [327] Activa queso.
    turnos_azar_raton = pedir("Turnos iniciales del ratón al azar", int, 2)  # [328] Cuántos turnos random.
    profundidad = pedir("Profundidad Minimax (más = más lento)", int, 5)  # [329] Profundidad.
    semilla = pedir("Semilla (repetible)", int, 42)  # [330] Semilla para tablero reproducible.
    pausa = pedir("Pausa entre turnos (segundos)", float, 0.0)  # [331] Pausa opcional.

    gato_inicio = (0, 0)  # [332] Posición inicial del gato (arriba-izquierda).
    raton_inicio = (filas - 1, columnas - 1)  # [333] Posición inicial del ratón (abajo-derecha).

    tablero = generar_tablero_aleatorio(  # [334] Generamos tablero con obstáculos/queso según configuración.
        semilla,  # [335] Semilla.
        filas,  # [336] Filas.
        columnas,  # [337] Columnas.
        densidad,  # [338] Densidad de obstáculos.
        diagonales,  # [339] Diagonales sí/no.
        gato_inicio,  # [340] Inicio gato.
        raton_inicio,  # [341] Inicio ratón.
        activar_queso,  # [342] Queso sí/no.
    )  # [343] Fin llamada.

    ganador = jugar(  # [344] Arrancamos el juego.
        tablero,  # [345] Tablero.
        gato_inicio,  # [346] Inicio gato.
        raton_inicio,  # [347] Inicio ratón.
        turnos,  # [348] Turnos máximos.
        dificultad,  # [349] Dificultad.
        profundidad,  # [350] Profundidad Minimax.
        turnos_azar_raton,  # [351] Turnos random del ratón.
        humano,  # [352] Control humano.
        pausa,  # [353] Pausa.
    )  # [354] Fin jugar.

    print(f"\n🏁 Ganador: {ganador}")  # [355] Mostramos el ganador.


if __name__ == "__main__":  # [356] Esto es un “punto de entrada”: se ejecuta solo si corrés este archivo directamente (no si lo importás).
    principal()  # [357] Llamamos a la función principal para iniciar el programa.
