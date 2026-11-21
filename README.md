# Búsqueda de rutas en el metro con A* (Python)

Planificador de rutas en una red de metro (un modelo reducido del metro de Lyon) con algoritmos de búsqueda de inteligencia artificial: búsqueda en profundidad, en anchura, de coste uniforme y **A\***.

Práctica 1 de la asignatura *Intel·ligència Artificial* (Grado en Ingeniería Informática, UAB).

## Qué implementa (`SearchAlgorithm.py`)

- **Búsqueda no informada:** DFS (`depth_first_search`) y BFS (`breadth_first_search`), con eliminación de ciclos.
- **Coste uniforme** (`uniform_cost_search`) con cuatro criterios de coste: número de paradas, tiempo, distancia y número de transbordos.
- **A\*** (`Astar`) con heurísticas según el criterio elegido y eliminación de caminos redundantes.
- **A\* desde coordenadas** (`Astar_improved`): calcula la ruta entre dos puntos cualquiera del mapa: busca la estación más cercana al origen y al destino y une los dos tramos con A*.

`SubwayMap.py`, `utils.py`, los datos del mapa y `TestCases.py` los daba la asignatura.

## Cómo ejecutarlo

```bash
python TestCases.py
```

## Tecnologías

Python · Algoritmos de búsqueda (DFS, BFS, UCS, A*) · Heurísticas · Grafos
