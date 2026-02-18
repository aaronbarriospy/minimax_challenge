import random # Traigo 'random' de fábrica. Lo uso para mezclar (shuffle) posiciones al azar y que el mapa cambie.
import math   # Traigo 'math' para usar la calculadora científica, específicamente para pedirle el infinito (math.inf).

# --- 1. ARMANDO EL MAPA ---

# Primero, necesito saber contar la distancia. Uso la Distancia "Manhattan" porque acá no podemos caminar en diagonal.
def contar_pasos(pos1, pos2):
    # Uso abs() que es el "Valor Absoluto". Le saca el signo negativo a la resta (nadie camina "-3 pasos").
    # Resto las filas, le saco el signo, y le sumo la diferencia de las columnas.
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

# Aquí preparo el terreno de juego antes de empezar.
def preparar_juego(filas, col, cantidad_paredes):
    raton = (0, 0) # Me pongo en la esquina de arriba a la izquierda.
    gato = (filas - 1, col - 1) # Pongo al gato en la esquina opuesta de abajo.
    
    # Armo una lista con todas las coordenadas posibles del tablero usando comprensión de listas.
    todas_las_celdas = [(f, c) for f in range(filas) for c in range(col)]
    
    # Uso .remove() para buscar la coordenada del ratón y del gato y echarlas de esta lista.
    # Hago esto para asegurarme de no poner una pared encima de nosotros al arrancar.
    todas_las_celdas.remove(raton)
    todas_las_celdas.remove(gato)
    
    # Uso random.shuffle() para mezclar la lista de celdas como si fuera un mazo de cartas.
    random.shuffle(todas_las_celdas) 
    
    # Uso .pop() para sacar la última celda de la lista mezclada. 
    # .pop() la borra de la lista y me la entrega en la mano para guardarla en la variable 'salida'.
    salida = todas_las_celdas.pop()    
    
    # Armo un set() (conjunto) en vez de una lista normal []. 
    # Lo uso porque el set no permite repetidos y buscar si choqué con algo acá adentro es rapidísimo.
    paredes = set() 
    
    for celda in todas_las_celdas:
        if len(paredes) >= cantidad_paredes: 
            # Uso 'break' para romper este bucle si ya puse todas las paredes que necesitaba.
            break 
        
        # Regla de oro: verifico no poner paredes a 2 pasos o menos del ratón ni del gato para no encerrarnos de entrada.
        if contar_pasos(celda, raton) <= 2 or contar_pasos(celda, gato) <= 2 or celda == salida:
            # Uso 'continue' para decirle al código: "Ignorá esta celda y saltá directo a probar la siguiente".
            continue 
            
        # Uso .add() que es como el .append() pero exclusivo para los set(). Meto la pared a la bolsa.
        paredes.add(celda) 
        
    return gato, raton, salida, paredes # Devuelvo todas las posiciones listas para arrancar.

# Esta funcion me dice si puedo dar un paso hacia un lado o si me voy a chocar.
def pasos_permitidos(posicion_actual, filas, col, paredes):
    f, c = posicion_actual 
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Mis desplazamientos matemáticos: Arriba, Abajo, Izq, Der.
    
    # Uso una lista normal [] vacía para ir anotando con .append() los pasos que sí se pueden hacer.
    pasos_ok = [] 
    
    for df, dc in direcciones:
        nueva_fila, nueva_col = f + df, c + dc 
        
        # Verifico que mi nueva posición no se salga de los bordes del mapa y pregunto si NO está en el set de paredes.
        if 0 <= nueva_fila < filas and 0 <= nueva_col < col and (nueva_fila, nueva_col) not in paredes:
            pasos_ok.append((nueva_fila, nueva_col)) # Si es un paso seguro, lo agrego al final de mi lista.
            
    return pasos_ok 

# --- 2. LA IA DEL GATO (ALGORITMO MINIMAX PURO) ---

# Este es el corazón inteligente del gato. Es una función recursiva (se llama a sí misma para ver el futuro).
def minimax_basico(gato, raton, salida, turnos_a_futuro, es_turno_gato, filas, col, paredes):
    
    # --- LOS CORTES (Casos Base donde la recursividad se detiene) ---
    if gato == raton: 
        return -100 # Si en la imaginación el gato me come, es excelente para él. Devuelvo un número negativo.
    if raton == salida: 
        return 100  # Si me escapo, es terrible para el gato. Devuelvo un número positivo.
    if turnos_a_futuro == 0: 
        # Si ya pensé muchos turnos adelante (profundidad 0), freno y me fijo a cuántos pasos estoy usando mi función contar_pasos.
        return contar_pasos(gato, raton)

    # --- TURNO DE PENSAR DEL GATO (Minimizador) ---
    if es_turno_gato: 
        # El gato es el Minimizador, quiere el número MÁS CHICO posible. 
        # Empieza asumiendo lo peor usando math.inf (infinito positivo) para que cualquier número sea menor a esto.
        mejor_puntaje = math.inf 
        
        # Prueba todos sus pasos permitidos imaginando el futuro.
        for paso in pasos_permitidos(gato, filas, col, paredes): 
            # Se llama a sí misma pasando el turno al ratón (False).
            puntaje = minimax_basico(paso, raton, salida, turnos_a_futuro - 1, False, filas, col, paredes)
            
            # Uso min() para comparar el puntaje viejo con el nuevo y quedarme estrictamente con el más chico.
            mejor_puntaje = min(mejor_puntaje, puntaje) 
            
        return mejor_puntaje

    # --- TURNO DE PENSAR DEL RATÓN (Maximizador) ---
    else: 
        # El ratón es el Maximizador, quiere el número MÁS GRANDE posible. 
        # Empieza con lo peor: -math.inf (infinito negativo).
        mejor_puntaje = -math.inf 
        
        for paso in pasos_permitidos(raton, filas, col, paredes): 
            puntaje = minimax_basico(gato, paso, salida, turnos_a_futuro - 1, True, filas, col, paredes)
            
            # Uso max() para comparar y quedarme estrictamente con el número más grande (la mejor ruta de escape).
            mejor_puntaje = max(mejor_puntaje, puntaje) 
            
        return mejor_puntaje

# Esta funcion la usa el gato en el juego real (no en su mente) para dar su paso definitivo.
def turno_del_gato(gato, raton, salida, filas, col, paredes, vision=4):
    mejor_puntaje = math.inf 
    paso_elegido = gato 
    
    # El gato mira todas las direcciones reales que puede tomar ahora mismo.
    for paso in pasos_permitidos(gato, filas, col, paredes):
        # Le pregunta al cerebro Minimax qué puntaje sacaría si da ese paso.
        puntaje = minimax_basico(paso, raton, salida, vision, False, filas, col, paredes)
        
        # Si ese paso le da un mejor resultado (más bajo que su infinito inicial), lo anota como el ganador.
        if puntaje < mejor_puntaje: 
            mejor_puntaje = puntaje
            paso_elegido = paso
            
    return paso_elegido

# --- 3. EL JUEGO EN LA CONSOLA ---

# Uso letras simples ASCII para pintar el tablero. Así mantengo el código súper limpio.
def pintar_consola(filas, col, gato, raton, salida, paredes):
    print("\n" + "-" * (col * 2)) 
    for f in range(filas): 
        linea = "" 
        for c in range(col): 
            pos = (f, c)
            # Voy chequeando qué hay en cada coordenada exacta y le asigno una letra a mi 'linea'.
            if pos == gato and pos == raton: linea += "X " # Choque
            elif pos == gato: linea += "G " # Gato
            elif pos == raton: linea += "R " # Ratón (Yo)
            elif pos == salida: linea += "S " # Puerta de Salida
            elif pos in paredes: linea += "# " # Pared obstáculo
            else: linea += ". " # Piso libre
        print(linea) 
    print("-" * (col * 2) + "\n")

# Aca meto todo el motor principal para que se pueda jugar interactivo.
def iniciar_partida():
    print("--- ESCAPE DEL GATO ---")
    filas = 8  # Fijo el tamaño en 8x8 para no perder tiempo tipiando en consola durante el live coding.
    col = 8
    paredes_cant = 12
    
    gato, raton, salida, paredes = preparar_juego(filas, col, paredes_cant)
    
    # Armo un diccionario para mapear las teclas de mi teclado con mis desplazamientos de coordenadas.
    teclas = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1)}

    # Uso un 'while True' para armar un bucle infinito. Esto mantiene el juego vivo hasta que alguien gane o pierda.
    while True: 
        pintar_consola(filas, col, gato, raton, salida, paredes) 
        print("Mueve al Raton (R) a la Salida (S). Huye del Gato (G).")
        
        # Uso input() para leer mi teclado, y le clavo .lower() al final para que pase todo a minúscula automáticamente.
        movimiento = input("Teclas (w/a/s/d): ").lower() 
        
        if movimiento in teclas:
            # Calculo a dónde caería si me muevo hacia ahí.
            df, dc = teclas[movimiento]
            caida = (raton[0] + df, raton[1] + dc)
            
            # Si mi caída está dentro de los pasos permitidos, actualizo mi posición.
            if caida in pasos_permitidos(raton, filas, col, paredes):
                raton = caida 
            else:
                print("Chocaste con la pared. Pierdes tu turno.")
        else:
            print("Tecla mala. Pierdes tu turno.")

        # Reviso si gané o perdí usando 'break' para romper el 'while True' y terminar el código.
        if raton == salida:
            pintar_consola(filas, col, gato, raton, salida, paredes)
            print("¡Ganaste! Llegaste a la salida.")
            break 
            
        if raton == gato:
            pintar_consola(filas, col, gato, raton, salida, paredes)
            print("¡Perdiste! El gato te atrapó.")
            break

        # Es el turno del gato. Llama a su función para pensar y dar su paso.
        print("El gato esta pensando...")
        gato = turno_del_gato(gato, raton, salida, filas, col, paredes) 

        # Vuelvo a revisar si el gato me comió al terminar de moverse.
        if gato == raton:
            pintar_consola(filas, col, gato, raton, salida, paredes)
            print("¡Perdiste! El gato te atrapó.")
            break

# Este bloque final es el botón de encendido. 
# Si ejecuto el archivo directamente en mi consola, arranca la partida.
if __name__ == "__main__":
    iniciar_partida()