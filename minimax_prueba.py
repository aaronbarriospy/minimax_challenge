# Importamos herramientas que Python ya trae de fábrica.
import random # Lo usamos para el azar (mezclar las posiciones de inicio).
import math   # Lo usamos para acceder a math.inf (el concepto de "infinito" en matemáticas).

# --- 1. PREPARANDO EL TABLERO ---

# Prof: Esta función es nuestra regla de medir. Calcula a cuántos "pasos" está una cosa de otra.
def distancia(p1, p2):
    # Restamos las posiciones 'x' e 'y', las volvemos positivas con abs() y las sumamos.
    # Es como contar las cuadras en una ciudad.
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# Prof: Aquí creamos el mundo donde van a jugar. 
def crear_escenario(filas, col, num_obs):
    raton = (0, 0) # El ratón arranca en la esquina de arriba a la izquierda.
    gato = (filas - 1, col - 1) # El gato arranca en la esquina de abajo a la derecha.
    
    # Creamos una lista con absolutamente todas las coordenadas del tablero.
    posiciones = [(f, c) for f in range(filas) for c in range(col)]
    
    # Sacamos las coordenadas donde ya están el ratón y el gato para no ponerles nada encima.
    posiciones.remove(raton)
    posiciones.remove(gato)
    
    # Mezclamos la lista como si fuera un mazo de cartas.
    random.shuffle(posiciones) 
    
    # Sacamos la última "carta" (coordenada) del mazo y decimos: "Esta será la meta".
    meta = posiciones.pop()    
    
    obs = set() # Creamos una "bolsa" vacía para guardar los obstáculos.
    for p in posiciones: # Revisamos las coordenadas que sobraron.
        if len(obs) >= num_obs: break # Si ya pusimos todas las paredes que queríamos, paramos.
        
        # Prof: Esta es la regla de oro para no encerrar a nadie desde el turno 1.
        # Si la coordenada está a 2 pasos o menos del ratón, o del gato, o es la meta...
        if distancia(p, raton) <= 2 or distancia(p, gato) <= 2 or p == meta:
            continue # ...la ignoramos y pasamos a la siguiente coordenada.
            
        obs.add(p) # Si pasó la prueba, la guardamos en la bolsa de obstáculos.
        
    # Entregamos todos los personajes y objetos listos para usar.
    return gato, raton, meta, obs

# Prof: Esta función nos dice hacia dónde podemos dar un paso sin chocarnos.
def movimientos_validos(pos, filas, col, obs):
    f, c = pos # Desempaquetamos la fila y columna actuales (ej. estamos en la fila 2, columna 3).
    # Estas son las direcciones matemáticas: (Arriba, Abajo, Izquierda, Derecha).
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
    validos = [] # Lista vacía para anotar a dónde sí podemos ir.
    
    for df, dc in dirs: # Probamos cada una de las 4 direcciones.
        nf, nc = f + df, c + dc # nf y nc son la "Nueva Fila" y "Nueva Columna".
        
        # Preguntamos: ¿La nueva posición no se sale del mapa y tampoco es una pared?
        if 0 <= nf < filas and 0 <= nc < col and (nf, nc) not in obs:
            validos.append((nf, nc)) # Si es seguro, lo anotamos en la lista.
            
    return validos # Devolvemos la lista de pasos permitidos.

# --- 2. EL CEREBRO DEL GATO (IA) ---

# Prof: Esta es la parte más avanzada, donde el gato "imagina" el futuro.
def minimax(gato, raton, meta, profundidad, es_gato, filas, col, obs, alfa, beta):
    # --- CASOS FINALES (Cuando la imaginación se detiene) ---
    if gato == raton: return -1000 # Si imaginó que te atrapa, le pone puntaje negativo (para el gato lo negativo es victoria).
    if raton == meta: return 1000  # Si imaginó que escapas, le pone puntaje positivo (derrota para el gato).
    if profundidad == 0: 
        # Si ya imaginó 5 pasos a futuro y nadie ganó, devuelve la distancia que los separa.
        return distancia(gato, raton)

    # --- FASE DEL GATO (Busca el número más chico) ---
    if es_gato: 
        mejor = math.inf # Empieza con el número más grande posible.
        for mov in movimientos_validos(gato, filas, col, obs): # Imagina qué pasa si da un paso.
            # Se llama a sí misma (recursividad) para ver qué haría el ratón después.
            val = minimax(mov, raton, meta, profundidad - 1, False, filas, col, obs, alfa, beta)
            mejor = min(mejor, val) # Se queda con el camino que le dio el número más chico.
            beta = min(beta, mejor) # (Optimización para no pensar de más).
            if beta <= alfa: break  # Si ya vio que este camino es malo, deja de pensar por aquí.
        return mejor

    # --- FASE DEL RATÓN (Busca el número más grande) ---
    else: 
        mejor = -math.inf # Empieza con el número más chico posible.
        for mov in movimientos_validos(raton, filas, col, obs): # Imagina los escapes del ratón.
            val = minimax(gato, mov, meta, profundidad - 1, True, filas, col, obs, alfa, beta)
            mejor = max(mejor, val) # Se queda con el camino de número más grande (más lejos del gato).
            alfa = max(alfa, mejor) 
            if beta <= alfa: break 
        return mejor

# Prof: Esta función es la que el gato usa en el turno real para decidir.
def turno_gato_ia(gato, raton, meta, filas, col, obs, profundidad=5):
    mejor_val = math.inf 
    mejor_mov = gato 
    
    # El gato prueba sus 4 direcciones...
    for mov in movimientos_validos(gato, filas, col, obs):
        # ...y usa minimax para ver cuál de esas direcciones le asegura atraparte.
        val = minimax(mov, raton, meta, profundidad, False, filas, col, obs, -math.inf, math.inf)
        if val < mejor_val: # Si encuentra una buena jugada, la guarda.
            mejor_val = val
            mejor_mov = mov
            
    return mejor_mov # Da el paso definitivo.

# --- 3. EL JUEGO Y LA PANTALLA ---

# Prof: Esto simplemente dibuja los emojis en la consola.
def dibujar(filas, col, gato, raton, meta, obs):
    print("\n" + "===" * col) # Techo del tablero
    for f in range(filas): # Vamos fila por fila
        fila_str = "" 
        for c in range(col): # Vamos columna por columna
            p = (f, c) # Posición que estamos pintando ahora mismo.
            
            # Prof: Una simple cadena de IFs para decidir qué emoji poner.
            if p == gato and p == raton: fila_str += " 💥" # Te comieron.
            elif p == raton and p == meta: fila_str += " 🚪" # Te salvaste.
            elif p == gato: fila_str += " 🐱" 
            elif p == raton: fila_str += " 🐭" 
            elif p == meta: fila_str += " 🏁" 
            elif p in obs: fila_str += " 🧱" 
            else: fila_str += " ⬛" # Piso vacío.
        print(fila_str) # Imprime la fila terminada.
    print("===" * col + "\n") # Piso del tablero.

# Prof: El motor principal. Acá arranca todo.
def jugar():
    print("🏁 EL ESCAPE DEL RATÓN 🏁")
    # Le pedimos al humano que escriba el tamaño y lo convertimos a número entero (int).
    filas = int(input("Filas del tablero (ej. 10): "))
    col = int(input("Columnas del tablero (ej. 10): "))
    num_obs = int(input("Cantidad de obstáculos (ej. 20): "))
    
    # Construimos el mundo.
    gato, raton, meta, obs = crear_escenario(filas, col, num_obs)
    
    # Prof: Un diccionario para traducir letras del teclado a movimientos matemáticos.
    controles = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1)}

    while True: # Bucle infinito (hasta que alguien gane o pierda).
        dibujar(filas, col, gato, raton, meta, obs) # Mostramos la pantalla.
        print("Misión: Llega a la meta (🏁) sin que te atrape el gato (🐱).")
        
        # --- TURNO DEL ALUMNO (RATÓN) ---
        mov = input("Tu turno (w/a/s/d): ").lower() # Pedimos la tecla.
        if mov in controles:
            # Sumamos la posición actual + lo que dice la tecla.
            nueva_pos = (raton[0] + controles[mov][0], raton[1] + controles[mov][1])
            if nueva_pos in movimientos_validos(raton, filas, col, obs):
                raton = nueva_pos # Si no hay pared, te moves.
            else:
                print("❌ Movimiento inválido. Pierdes el turno por chocar la pared.")
        else:
            print("❌ Tecla incorrecta. Pierdes el turno por dudar.")

        # Prof: Verificamos si ganaste o perdiste antes de que el gato se mueva.
        if raton == meta:
            dibujar(filas, col, gato, raton, meta, obs)
            print("🎉 ¡ESCAPASTE! Llegaste a la meta y venciste a la IA.")
            break # El break rompe el "while True" y termina el juego.
            
        if raton == gato:
            dibujar(filas, col, gato, raton, meta, obs)
            print("💀 ¡Te entregaste a las garras del gato!")
            break

        # --- TURNO DE LA IA (GATO) ---
        print("🤖 El gato IA está calculando su salto...")
        gato = turno_gato_ia(gato, raton, meta, filas, col, obs) # El gato piensa y actúa.

        # Verificamos si el gato te alcanzó después de saltar.
        if gato == raton:
            dibujar(filas, col, gato, raton, meta, obs)
            print("🩸 ¡GAME OVER! El algoritmo Minimax te ha acorralado.")
            break

# Esta línea hace que el juego arranque solo si ejecutas este archivo.
if __name__ == "__main__":
    jugar()