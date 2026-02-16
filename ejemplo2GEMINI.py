import random
import math

# --- 1. CONFIGURACIÓN DEL TABLERO ---

def distancia(p1, p2):
    # Distancia Manhattan en bloques
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def crear_escenario(filas, col, num_obs):
    raton = (0, 0)
    gato = (filas - 1, col - 1) # El gato siempre en la esquina opuesta
    
    posiciones = [(f, c) for f in range(filas) for c in range(col)]
    posiciones.remove(raton)
    posiciones.remove(gato)
    
    random.shuffle(posiciones) # Mezclamos para aleatoriedad
    meta = posiciones.pop()    # La salida 
    queso = posiciones.pop()   # Los puntos 
    
    obs = set()
    for p in posiciones:
        if len(obs) >= num_obs: break
        # ÁREA SEGURA: No pone obstáculos a 2 o menos pasos del ratón ni del gato
        if distancia(p, raton) <= 2 or distancia(p, gato) <= 2 or p == meta or p == queso:
            continue
        obs.add(p)
        
    return gato, raton, meta, queso, obs

def movimientos_validos(pos, filas, col, obs):
    f, c = pos
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
    validos = []
    for df, dc in dirs:
        nf, nc = f + df, c + dc
        if 0 <= nf < filas and 0 <= nc < col and (nf, nc) not in obs:
            validos.append((nf, nc))
    return validos

# --- 2. LA MENTE DEL GATO (MINIMAX) ---

def minimax(gato, raton, meta, profundidad, es_gato, filas, col, obs, alfa, beta):
    if gato == raton: return -1000 
    if raton == meta: return 1000  
    if profundidad == 0: 
        return distancia(gato, raton)

    if es_gato: 
        mejor = math.inf
        for mov in movimientos_validos(gato, filas, col, obs):
            val = minimax(mov, raton, meta, profundidad - 1, False, filas, col, obs, alfa, beta)
            mejor = min(mejor, val)
            beta = min(beta, mejor)
            if beta <= alfa: break 
        return mejor

    else: 
        mejor = -math.inf
        for mov in movimientos_validos(raton, filas, col, obs):
            val = minimax(gato, mov, meta, profundidad - 1, True, filas, col, obs, alfa, beta)
            mejor = max(mejor, val)
            alfa = max(alfa, mejor)
            if beta <= alfa: break 
        return mejor

def turno_gato_ia(gato, raton, meta, filas, col, obs, profundidad=5):
    mejor_val = math.inf
    mejor_mov = gato
    for mov in movimientos_validos(gato, filas, col, obs):
        val = minimax(mov, raton, meta, profundidad, False, filas, col, obs, -math.inf, math.inf)
        if val < mejor_val:
            mejor_val = val
            mejor_mov = mov
    return mejor_mov

# --- 3. INTERFAZ GRÁFICA Y BUCLE PRINCIPAL ---

def dibujar(filas, col, gato, raton, meta, queso, obs):
    print("\n" + "===" * col)
    for f in range(filas):
        fila_str = ""
        for c in range(col):
            p = (f, c)
            if p == gato and p == raton: fila_str += " 💥"
            elif p == raton and p == meta: fila_str += " 🚪"
            elif p == gato: fila_str += " 🐱"
            elif p == raton: fila_str += " 🐭"
            elif p == meta: fila_str += " 🏁"
            elif queso and p == queso: fila_str += " 🧀"
            elif p in obs: fila_str += " 🧱"
            else: fila_str += " ⬛" # Camino libre más estético y uniforme
        print(fila_str)
    print("===" * col + "\n")

def jugar():
    print("🧀 EL ESCAPE DEL RATÓN 🏁")
    filas = int(input("Filas del tablero (ej. 10): "))
    col = int(input("Columnas del tablero (ej. 10): "))
    num_obs = int(input("Cantidad de obstáculos (ej. 20): "))
    
    gato, raton, meta, queso, obs = crear_escenario(filas, col, num_obs)
    controles = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1)}
    puntos = 0

    while True:
        dibujar(filas, col, gato, raton, meta, queso, obs)
        print(f"Puntos: {puntos} | Salida: 🏁 | Enemigo: 🐱")
        
        # --- TURNO DEL USUARIO ---
        mov = input("Tu turno (w/a/s/d): ").lower()
        if mov in controles:
            nueva_pos = (raton[0] + controles[mov][0], raton[1] + controles[mov][1])
            if nueva_pos in movimientos_validos(raton, filas, col, obs):
                raton = nueva_pos
            else:
                print("❌ Movimiento inválido. Pierdes el turno por chocar la pared.")
        else:
            print("❌ Tecla incorrecta. Pierdes el turno por dudar.")

        if queso and raton == queso:
            puntos += 1
            print(f"¡Atrapaste un queso! (+1 Punto)")
            queso = None 

        if raton == meta:
            dibujar(filas, col, gato, raton, meta, queso, obs)
            print(f"🎉 ¡ESCAPASTE! Llegaste a la meta con {puntos} puntos.")
            break
        if raton == gato:
            dibujar(filas, col, gato, raton, meta, queso, obs)
            print("💀 ¡Te entregaste a las garras del gato!")
            break

        # --- TURNO DE LA IA ---
        print("🤖 El gato IA está calculando su salto...")
        gato = turno_gato_ia(gato, raton, meta, filas, col, obs)

        if gato == raton:
            dibujar(filas, col, gato, raton, meta, queso, obs)
            print("🩸 ¡GAME OVER! El algoritmo Minimax te ha acorralado.")
            break

if __name__ == "__main__":
    jugar()