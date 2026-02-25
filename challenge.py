filas = 2
col = 2

def preparar_juego():
    todas_las_celdas = [(f, c) for f in range(filas) for c in range(col)]
    print(todas_las_celdas)
    
preparar_juego()



FUNCION existe_camino_posible(inicio, objetivo, paredes, filas, col):
    CREAR lista_por_visitar = [inicio]
    CREAR conjunto_visitados = vacio

    MIENTRAS lista_por_visitar NO este vacia:
        actual = EXTRAER PRIMER ELEMENTO de lista_por_visitar
        
        SI actual ES IGUAL a objetivo:
            RETORNAR VERDADERO

        AGREGAR actual a conjunto_visitados

        PARA CADA vecino EN obtener_vecinos_validos(actual):
            SI vecino NO esta en conjunto_visitados Y vecino NO esta en paredes:
                AGREGAR vecino AL FINAL DE lista_por_visitar

    RETORNAR FALSO


def existe_camino(inicio, objetivo, paredes, fila, col):
    lista_por_visitar = [inicio]
    conjunto_visitados = set()

    while lista_por_visitar:
        actual = lista_por_visitar.pop(0)

        if actual == objetivo:
            return True

        conjunto_visitados.add(actual)

        for vecino in pasos_permitidos(actual, fila, col, paredes):
            if vecino not in conjunto_visitados:
                lista_por_visitar.append(vecino)



### FUNCION iniciar_partida():
    # ... (tu configuración inicial de filas, columnas, etc.) ...
    
    CREAR variable turnos_jugados = 0

    MIENTRAS VERDADERO: # (Tu bucle 'while True')
        SUMAR 1 a turnos_jugados
        
        # ... (lógica donde el jugador ingresa su movimiento w/a/s/d) ...
        # ... (lógica donde el jugador se mueve) ...

        SI raton == salida:
            IMPRIMIR "¡Ganaste! Llegaste a la salida en " + turnos_jugados + " turnos."
            ROMPER BUCLE
            
        SI raton == gato:
            IMPRIMIR "¡Perdiste! El gato te atrapó en " + turnos_jugados + " turnos."
            ROMPER BUCLE

        # ... (turno del gato) ...
        
        SI gato == raton:
            IMPRIMIR "¡Perdiste! El gato te atrapó en " + turnos_jugados + " turnos."
            ROMPER BUCLE


def iniciar_partida():
    turnos_jugados = 0
    while True:
        turnos_jugados += 1

        if raton == salida:
            print(f'Ganaste! Llegaste a la salida en {turnos_jugados} turnos')
            break
        if raton == gato:
            print(f'Perdiste! El gato te atrapo en {turnos_jugados} turnos')
            break
        if gato == raton:
            print(f'Perdiste! El gato te atrapo en {turnos_jugados} turnos')
            break

### DENTRO DEL BUCLE MIENTRAS VERDADERO:
    # ... (después de pintar la consola en pantalla) ...
    
    distancia_actual = contar_pasos(raton, gato)
    
    SI distancia_actual ES MENOR O IGUAL A 2:
        IMPRIMIR "¡CUIDADO! El gato está muy cerca."
        
    # ... (luego sigue el código donde pides: input("Teclas (w/a/s/d): ")) ...

distancia_actual = contar_pasos(raton, gato)

if distancia_actual <= 2:
    print('Cuidado! El gato esta muy cerca')



### DENTRO DEL BUCLE PRINCIPAL (while True):
    # ... (se pinta la consola y se explican las reglas) ...
    
    LEER movimiento del jugador
    
    SI movimiento NO ESTA EN teclas:
        IMPRIMIR "Tecla incorrecta. Intenta de nuevo."
        CONTINUAR # Esta instrucción hace que el bucle ignore todo lo que está abajo y vuelva a empezar desde arriba.
        
    # (Si el código llega aquí, significa que la tecla SÍ es válida)
    # CALCULAR caída
    # ACTUALIZAR posición del ratón

if movimiento not in teclas:
    print('Tecla incorrecta, intenta de nuevo')
    continue


### DENTRO DEL BUCLE PRINCIPAL (while True):
    # ... (El ratón ya se movió y validamos si llegó a la salida) ...
    
    SI turnos_jugados ES PAR:
        IMPRIMIR "El gato esta pensando..."
        gato = turno_del_gato(gato, raton, salida, filas, col, paredes)
    SINO:
        IMPRIMIR "El gato esta descansando..."

    # ... (Vuelvo a revisar si el gato me comió) ...

    if turnos_jugados is % 2 == 0:
        print("El gato esta pensando...")
        gato = turno_del_gato(gato, raton, salida, filas, col, paredes)
    else:
        print("El gato esta descansando")


### FUNCION crear_matriz_tablero(filas, col, gato, raton, salida, paredes):
    CREAR lista vacia llamada 'matriz_final'

    PARA f DESDE 0 HASTA filas - 1:
        CREAR lista vacia llamada 'fila_actual'

        PARA c DESDE 0 HASTA col - 1:
            posicion = (f, c)

            SI posicion ES IGUAL a gato Y posicion ES IGUAL a raton:
                AGREGAR "X" a 'fila_actual'
            SINO SI posicion ES IGUAL a gato:
                AGREGAR "G" a 'fila_actual'
            SINO SI posicion ES IGUAL a raton:
                AGREGAR "R" a 'fila_actual'
            SINO SI posicion ES IGUAL a salida:
                AGREGAR "S" a 'fila_actual'
            SINO SI posicion ESTA ADENTRO DE paredes:
                AGREGAR "#" a 'fila_actual'
            SINO:
                AGREGAR "." a 'fila_actual'

        AGREGAR 'fila_actual' a 'matriz_final'

    RETORNAR 'matriz_final'

def crear_matriz_tablero(filas, col, gato, raton, salida, paredes):
    matriz_final = []
    for f in range(filas):
        fila_actual = []
        for c in range(col):
            posicion = (f,c)
            if posicion == gato and posicion == raton:
                fila_actual.append('x')
            elif posicion == gato:
                fila_actual.append('g')
            elif posicion == raton:
                fila_actual.append('r')
            elif posicion == salida:
                fila_actual.append('s')
            elif posicion in paredes:
                fila_actual.append('#')
            else:
                fila_actual.append('.')
        matriz_final.append(fila_actual)

    return matriz_final

### FUNCION raton_atrapado(raton, filas, col, paredes):
    CREAR variable 'movimientos_posibles' y asignarle el resultado de la función pasos_permitidos(raton, filas, col, paredes)

    SI la longitud de 'movimientos_posibles' ES IGUAL A 0:
        RETORNAR VERDADERO
    SINO:
        RETORNAR FALSO


def raton_atrapado(raton, filas, col, paredes):
    movimientos_posibles = pasos_permitidos(raton, filas, col, paredes)

    if len(movimientos_posibles) == 0:
        return True
    else:
        return False


### FUNCION iniciar_partida():
    # ... (código existente donde defines filas, columnas y llamas a preparar_juego) ...
    gato, raton, salida, paredes = preparar_juego(filas, col, paredes_cant)
    
    # --- NUEVA LÓGICA A IMPLEMENTAR ---
    CREAR variable 'distancia_meta' que almacene el resultado de contar_pasos entre raton y salida
    IMPRIMIR "El juego comienza. Estás a " + distancia_meta + " pasos de la salida."
    # ----------------------------------

    # ... (luego sigue el bucle: while True:) ...

distancia_meta = contar_pasos(raton, salida)
print(f'El juego comienza! estas a {distancia_meta} pasos de la salida')

### FUNCION minimax_cartas(estado_mesa, profundidad, es_turno_ia):

    # --- CASO BASE ---
    SI profundidad ES IGUAL A 0 O juego_terminado(estado_mesa) ES VERDADERO:
        RETORNAR evaluar_mesa(estado_mesa)

    # --- TURNO DE LA IA (Maximizador) ---
    SI es_turno_ia ES VERDADERO:
        mejor_puntaje = -INFINITO
        
        PARA CADA jugada EN obtener_jugadas(estado_mesa):
            puntaje = minimax_cartas(jugada, profundidad - 1, FALSO)
            mejor_puntaje = MAX(mejor_puntaje, puntaje)
            
        RETORNAR mejor_puntaje

    # --- TURNO DEL RIVAL (Minimizador) ---
    SINO:
        mejor_puntaje = INFINITO
        
        PARA CADA jugada EN obtener_jugadas(estado_mesa):
            puntaje = minimax_cartas(jugada, profundidad - 1, VERDADERO)
            mejor_puntaje = MIN(mejor_puntaje, puntaje)
            
        RETORNAR mejor_puntaje

def minimax_cartas(estado_mesa, profundidad, es_turno_ia):
    if profundidad == 0 or juego_terminado(estado_mesa):
        return evaluar_mesa(estado_mesa)

    if es_turno_ia:
        mejor_puntaje = -math.inf

        for jugada in obtener_jugadas(estado_mesa):
            puntaje = minimax_cartas(jugada, profundidad -1, False)
            mejor_puntaje = max(mejor_puntaje, puntaje)
        return mejor_puntaje
    else:
        mejor_puntaje = math.inf
        for jugada in obtener_jugadas(estado_mesa):
            puntaje = minimax_cartas(jugada, profundidad -1, True)
            mejor_puntaje = min(mejor_puntaje, puntaje)
        return mejor_puntaje


### FUNCION verificar_victoria(tablero, jugador):
    
    # --- 1. Revisar todas las filas ---
    PARA CADA fila EN tablero:
        SI fila[0] ES IGUAL A jugador Y fila[1] ES IGUAL A jugador Y fila[2] ES IGUAL A jugador:
            RETORNAR VERDADERO

    # --- 2. Revisar todas las columnas ---
    PARA columna DESDE 0 HASTA 2:
        SI tablero[0][columna] ES IGUAL A jugador Y tablero[1][columna] ES IGUAL A jugador Y tablero[2][columna] ES IGUAL A jugador:
            RETORNAR VERDADERO

    # --- 3. Revisar la diagonal principal (arriba-izq a abajo-der) ---
    SI tablero[0][0] ES IGUAL A jugador Y tablero[1][1] ES IGUAL A jugador Y tablero[2][2] ES IGUAL A jugador:
        RETORNAR VERDADERO

    # --- 4. Revisar la diagonal inversa (arriba-der a abajo-izq) ---
    SI tablero[0][2] ES IGUAL A jugador Y tablero[1][1] ES IGUAL A jugador Y tablero[2][0] ES IGUAL A jugador:
        RETORNAR VERDADERO

    # Si pasa por todas las revisiones y no ganó...
    RETORNAR FALSO

def verificar_victoria(tablero, jugador):
    for fila in tablero:
        if fila[0] == jugador and fila[1] == jugador and fila[2] == jugador:
            return True

    for columna in range(0,3):
        if tablero[0][columna] == jugador and tablero[1][columna] == jugador and tablero[2][columna] == jugador:
            return True
            
    if tablero[0][0] == jugador and tablero[1][1] == jugador and tablero[2][2] == jugador:
        return True
    if tablero[0][2] == jugador and tablero[1][1] == jugador and tablero[2][0] == jugador:
        return True
    return False


### FUNCION contar_minas_adyacentes(tablero, fila_origen, col_origen, total_filas, total_cols):
    minas_encontradas = 0
    
    direcciones = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    PARA CADA df, dc EN direcciones:
        nueva_fila = fila_origen + df
        nueva_col = col_origen + dc

        SI nueva_fila >= 0 Y nueva_fila < total_filas:
            
            SI nueva_col >= 0 Y nueva_col < total_cols:
                
                SI tablero[nueva_fila][nueva_col] ES IGUAL A "*":
                    minas_encontradas += 1

    RETORNAR minas_encontradas

def contar_minas_adyacentes(tablero, fila_origen, col_origen, total_filas, total_cols):
    minas_encontradas = 0
    direcciones = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for df, dc in direcciones:
        nueva_fila = fila_origen + df
        nueva_col = col_origen + dc
        
        if nueva_fila >= 0 and nueva_fila < total_filas:
            if nueva_col >= 0 and nueva_col < total_cols:
                if tablero[nueva_fila][nueva_col] == "*":
                    minas_encontradas += 1
    return minas_encontradas


def rellenar_imagen(imagen, fila_inicial, col_inicial, color_nuevo):
    color_viejo = imagen[fila_inicial][col_inicial]
    if color_viejo == color_nuevo:
        return imagen

    lista_pendientes = [(fila_inicial, col_inicial)]

    while lista_pendientes:
        celda_actual = lista_pendientes.pop(0)
        f, c = celda_actual
        if 0 <= f < len(imagen) and 0 <= c < len(imagen[0]) and imagen[f][c] == color_viejo:
            imagen[f][c] = color_nuevo
            lista_pendientes.append((f + 1, c))
            lista_pendientes.append((f - 1, c))
            lista_pendientes.append((f, c + 1))
            lista_pendientes.append((f, c - 1))
return imagen


### FUNCION busqueda_binaria(lista, objetivo):
    izquierda = 0
    derecha = longitud de la lista - 1

    MIENTRAS izquierda sea menor o igual a derecha:
        medio = (izquierda + derecha) // 2
        
        SI lista[medio] es igual a objetivo:
            RETORNAR medio
            
        SI lista[medio] es menor a objetivo:
            izquierda = medio + 1
            
        SINO (si es mayor):
            derecha = medio - 1
            
    RETORNAR -1  # Si el bucle termina y no encontró nada

def busqueda_binaria(lista, objetivo):
    izquierda = 0
    derecha = len(lista) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2

        if lista[medio] == objetivo:
            return medio
        if lista[medio] < objetivo:
            izquierda = medio +1
        else:
            derecha = medio -1
    return -1

### FUNCION ordenar_burbuja(lista):
    n = longitud de la lista

    PARA i desde 0 hasta n - 1:
        PARA j desde 0 hasta n - i - 2:
            
            SI lista[j] es mayor que lista[j + 1]:
                # Intercambiamos los valores
                temporal = lista[j]
                lista[j] = lista[j + 1]
                lista[j + 1] = temporal
                
    RETORNAR lista

def ordenar_burbuja(lista):
    n = len(lista)

    for i in range(n - 1):
        for j in range(n - i - 2):
            if lista[j] > lista[j + 1]:
                temporal = lista[j]
                lista[j] = lista[j + 1]
                lista[j + 1] = temporal
    return lista


### FUNCION es_movimiento_seguro(posicion_destino, posicion_escudo):
    fila_d, col_d = posicion_destino
    fila_e, col_e = posicion_escudo

    # 1. ¿Es la posición exacta del escudo?
    SI fila_d == fila_e Y col_d == col_e:
        RETORNAR Falso

    # 2. ¿Está a un paso de distancia (arriba, abajo, izquierda o derecha)?
    SI fila_d == fila_e Y (col_d == col_e + 1 O col_d == col_e - 1):
        RETORNAR Falso
        
    SI col_d == col_e Y (fila_d == fila_e + 1 O fila_d == fila_e - 1):
        RETORNAR Falso

    # Si no entró en ningún IF anterior, el camino está despejado
    RETORNAR Verdadero

def es_movimiento_seguro(posicion_destino, posicion_escudo):
    fila_d, col_d = posicion_destino
    fila_e, col_e = posicion_escudo
    if fila_d == fila_e and col_d == col_e:
        return False
    
    if fila_d == fila_e and ((col_d == col_e + 1) or (col_d == col_e - 1)):
        return False
    if col_d == col_e and ((fila_d == fila_e + 1) or (fila_d == fila_e -1)):
        return False
    return True


### FUNCION decision_ia():
    camino_a = MINIMO entre 3 y 5
    camino_b = MINIMO entre 2 y 10
    
    mejor_resultado = MAXIMO entre camino_a y camino_b
    RETORNAR mejor_resultado

def decision_ia():
    camino_a = min(3 , 5)
    camino_b = min(2 , 10)
    mejor_resultado = max(camino_a, camino_b)
    return mejor_resultado


### FUNCION generar_mapa_calor():
    matriz = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    
    PARA f DESDE 0 HASTA 2:
        PARA c DESDE 0 HASTA 2:
            distancia = f + c
            matriz[f][c] = distancia
            
    RETORNAR matriz

def generar_mapa_calor():
    matriz = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

    for f in range(3):
        for c in range(3):
            distancia = f + c
            matriz[f][c] = distancia

    return matriz


### FUNCION elegir_movimiento_seguro():
    movimientos = [10, -100, 25]
    movimientos_filtrados = lista vacía
    
    PARA CADA valor EN movimientos:
        SI valor NO ES IGUAL A -100:
            AGREGAR valor A movimientos_filtrados
            
    mejor_opcion = MAXIMO de movimientos_filtrados
    RETORNAR mejor_opcion

def elegir_movimiento_seguro():
    movimientos = [10, -100, 25]
    movimientos_filtrados = []

    for valor in movimientos:
        if valor != -100:
            movimientos_filtrados.append(valor)
    mejor_opcion = max(movimientos_filtrados)
    return mejor_opcion