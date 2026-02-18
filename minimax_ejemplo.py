import random # Necesito esto para mezclar las cosas al principio, así no es siempre igual.
import math   # Esto me da 'math.inf', que es una forma fácil de decirle a Python "infinito".

# --- 1. ARMANDO EL MAPA ---

# Primero, necesito saber contar la distancia. Uso "Manhattan" porque no podemos caminar en diagonal.
def contar_pasos(pos1, pos2):
    # Resto las filas, le saco el signo (abs) y le sumo la diferencia de las columnas.
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

# Aquí preparo el terreno de juego antes de empezar.
def preparar_juego(filas, col, cantidad_paredes):
    raton = (0, 0) # Te pongo en la esquina de arriba.
    gato = (filas - 1, col - 1) # Pongo al gato en la esquina opuesta.
    
    # Armo una lista con todas las coordenadas posibles del tablero.
    todas_las_celdas = [(f, c) for f in range(filas) for c in range(col)]
    
    # Saco al ratón y al gato de esa lista para no poner cosas encima de ellos.
    todas_las_celdas.remove(raton)
    todas_las_celdas.remove(gato)
    
    # Mezclo las celdas para que todo sea al azar.
    random.shuffle(todas_las_celdas) 
    
    # Tomo la última celda de la lista mezclada y esa va a ser la puerta de salida.
    salida = todas_las_celdas.pop()    
    
    paredes = set() # Uso un 'set' (conjunto) porque buscar cosas ahí es súper rápido.
    for celda in todas_las_celdas:
        if len(paredes) >= cantidad_paredes: # Si ya puse todas las paredes que me pidieron, freno.
            break 
        
        # Ojo acá: no pongo paredes cerca tuyo ni del gato para que no queden encerrados de entrada.
        if contar_pasos(celda, raton) <= 2 or contar_pasos(celda, gato) <= 2 or celda == salida:
            continue # Salteo esta celda.
            
        paredes.add(celda) # Agrego la pared.
        
    return gato, raton, salida, paredes # Devuelvo todas las posiciones iniciales.

# Esta funcion me dice si puedo dar un paso hacia un lado o si me voy a chocar.
def pasos_permitidos(posicion_actual, filas, col, paredes):
    f, c = posicion_actual 
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Arriba, Abajo, Izquierda, Derecha.
    pasos_ok = [] # Acá voy a guardar los que sí se pueden hacer.
    
    for df, dc in direcciones:
        nueva_fila, nueva_col = f + df, c + dc 
        
        # Verifico que la nueva posición esté dentro de los bordes y no sea una pared.
        if 0 <= nueva_fila < filas and 0 <= nueva_col < col and (nueva_fila, nueva_col) not in paredes:
            pasos_ok.append((nueva_fila, nueva_col)) 
            
    return pasos_ok 

# --- 2. LA IA DEL GATO (MINIMAX PURO) ---

# Este es el corazón inteligente del gato. Es recursivo, se llama a sí mismo para ver el futuro.
def minimax_basico(gato, raton, salida, turnos_a_futuro, es_turno_gato, filas, col, paredes):
    
    # --- LOS CORTES (Cuando dejo de pensar) ---
    if gato == raton: 
        return -100 # Si el gato te come, es excelente para él. Devuelve un número muy negativo.
    if raton == salida: 
        return 100  # Si te escapas, es terrible para el gato. Devuelve un número muy positivo.
    if turnos_a_futuro == 0: 
        # Si ya pensé muchos turnos adelante, freno y me fijo a cuántos pasos estoy.
        return contar_pasos(gato, raton)

    # --- TURNO DE PENSAR DEL GATO ---
    if es_turno_gato: 
        # El gato quiere el número MÁS CHICO posible. Empieza asumiendo lo peor (infinito positivo).
        mejor_puntaje = math.inf 
        
        # Prueba todos sus pasos permitidos en su imaginación.
        for paso in pasos_permitidos(gato, filas, col, paredes): 
            # Llama a minimax de nuevo, asumiendo que ahora le toca al ratón.
            puntaje = minimax_basico(paso, raton, salida, turnos_a_futuro - 1, False, filas, col, paredes)
            # Se queda con el camino que le dé el puntaje más bajo.
            mejor_puntaje = min(mejor_puntaje, puntaje) 
            
        return mejor_puntaje

    # --- TURNO DE PENSAR DEL RATÓN ---
    else: 
        # El ratón quiere el número MÁS GRANDE posible. Empieza con lo peor (infinito negativo).
        mejor_puntaje = -math.inf 
        
        # Imagina todos los pasos del ratón.
        for paso in pasos_permitidos(raton, filas, col, paredes): 
            puntaje = minimax_basico(gato, paso, salida, turnos_a_futuro - 1, True, filas, col, paredes)
            mejor_puntaje = max(mejor_puntaje, puntaje) 
            
        return mejor_puntaje

# Esta funcion la usa el gato en el juego real para decidir su paso final.
def turno_del_gato(gato, raton, salida, filas, col, paredes, vision=4):
    mejor_puntaje = math.inf 
    paso_elegido = gato 
    
    # El gato mira todas las direcciones que puede tomar ahora mismo.
    for paso in pasos_permitidos(gato, filas, col, paredes):
        # Le pregunta a Minimax qué pasaría si da ese paso.
        puntaje = minimax_basico(paso, raton, salida, vision, False, filas, col, paredes)
        
        # Si ese paso le da un mejor resultado (más bajo), lo anota como el ganador.
        if puntaje < mejor_puntaje: 
            mejor_puntaje = puntaje
            paso_elegido = paso
            
    return paso_elegido

# --- 3. EL JUEGO EN LA CONSOLA ---

# Uso letras simples para pintar el tablero. Nada de emojis raros.
def pintar_consola(filas, col, gato, raton, salida, paredes):
    print("\n" + "-" * (col * 2)) 
    for f in range(filas): 
        linea = "" 
        for c in range(col): 
            pos = (f, c)
            # Voy chequeando qué hay en cada coordenada y pongo su letra.
            if pos == gato and pos == raton: linea += "X " # Choque
            elif pos == gato: linea += "G " # Gato
            elif pos == raton: linea += "R " # Ratón
            elif pos == salida: linea += "S " # Salida
            elif pos in paredes: linea += "# " # Pared
            else: linea += ". " # Piso
        print(linea) 
    print("-" * (col * 2) + "\n")

# Aca meto todo en un bucle para que se pueda jugar.
def iniciar_partida():
    print("--- ESCAPE DEL GATO ---")
    filas = 8  # Fijo el tamaño para que sea más directo, sin preguntar tanto.
    col = 8
    paredes_cant = 12
    
    gato, raton, salida, paredes = preparar_juego(filas, col, paredes_cant)
    teclas = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1)}

    while True: # Esto corre hasta que ganes o pierdas.
        pintar_consola(filas, col, gato, raton, salida, paredes) 
        print("Mueve al Raton (R) a la Salida (S). Huye del Gato (G).")
        
        # Pido tu movimiento.
        movimiento = input("Teclas (w/a/s/d): ").lower() 
        if movimiento in teclas:
            # Calculo a dónde caerías.
            df, dc = teclas[movimiento]
            caida = (raton[0] + df, raton[1] + dc)
            
            # Si podés pisar ahí, muevo al ratón.
            if caida in pasos_permitidos(raton, filas, col, paredes):
                raton = caida 
            else:
                print("Chocaste con la pared. Pierdes tu turno.")
        else:
            print("Tecla mala. Pierdes tu turno.")

        # Reviso si ganaste o perdiste antes de que se mueva el gato.
        if raton == salida:
            pintar_consola(filas, col, gato, raton, salida, paredes)
            print("¡Ganaste! Llegaste a la salida.")
            break 
            
        if raton == gato:
            pintar_consola(filas, col, gato, raton, salida, paredes)
            print("¡Perdiste! El gato te atrapó.")
            break

        # Es el turno del gato. Piensa y se mueve.
        print("El gato esta pensando...")
        gato = turno_del_gato(gato, raton, salida, filas, col, paredes) 

        # Reviso si el gato te comió al moverse.
        if gato == raton:
            pintar_consola(filas, col, gato, raton, salida, paredes)
            print("¡Perdiste! El gato te atrapó.")
            break

# Ejecuto el juego
if __name__ == "__main__":
    iniciar_partida()