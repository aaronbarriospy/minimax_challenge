filas = 2
col = 2

def preparar_juego():
    todas_las_celdas = [(f, c) for f in range(filas) for c in range(col)]
    print(todas_las_celdas)
    
preparar_juego()