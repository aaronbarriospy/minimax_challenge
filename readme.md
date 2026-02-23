¿Que cree?
Un juego de "Gato y Raton" jugable desde la consola usando Python. El jugador controla al raton con el objetivo de llegar a la meta esquivando obstaculos, mientras es cazado por un gato controlado por una Inteligencia Artificial. La IA utiliza el algoritmo Minimax para predecir los movimientos del jugador y acorralarlo.

¿Que funciono super bien?
El sistema de renderizado en la consola y el manejo de coordenadas. Lograr que el mapa se dibuje de forma limpia recorriendo la matriz fila por fila hizo que la base del juego fuera muy estable y, sobre todo, facil de explicar paso a paso.

¿Que fue un desastre? (Los verdaderos retos)
Siendo totalmente honesto, el proceso fue sumamente dificil y me enfrente a dos grandes muros que casi me estancan:

El Algoritmo: Entender e implementar Minimax me costo muchisimo. Al principio, intente usar codigo que incluia conceptos demasiado avanzados (como la optimizacion con poda alfa y beta). Fue un desastre intentar asimilarlo, y me di cuenta de que no podia presentar ni defender ese codigo en una entrevista sin mentir sobre mis verdaderos conocimientos. Tuve que tomar la dificil decision de dar un paso atras, borrar esa complejidad extra y reescribir la logica de la IA para que fuera lo mas pura y sencilla posible. Priorice entender cada linea al 100% antes que mostrar algo que no dominaba.

GitHub y el Control de Versiones: Subir el codigo fue otro gran dolor de cabeza. Me tope con errores constantes en la terminal donde mis push eran rechazados (el clasico error de sincronizacion de Git). Tuve que investigar como unificar mi entorno local con el repositorio remoto usando tecnicas de pull y actualizacion de ramas para por fin lograr cargar los archivos sin sobreescribir nada por accidente.

Mi mejor momento "¡aja!"
Fueron dos. Con el codigo, fue el momento en que deje de ver a Minimax como matematicas abstractas y comprendi como la funcion se llama a si misma para simular y "ver el futuro" turno por turno. Con Git, fue la inmensa satisfaccion de resolver los bloqueos de la terminal y finalmente ver mi codigo reflejado correctamente en mi perfil de GitHub.