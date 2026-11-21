# This file contains all the required routines to make an A* search algorithm.
#
__author__ = 'Pau Tusón'
# _________________________________________________________________________________________
# Intel.ligencia Artificial
# Curs 2023 - 2024
# Universitat Autonoma de Barcelona
# _______________________________________________________________________________________

from SubwayMap import *
from utils import *
import os
import math
import copy


def expand(path, map):
    """
     It expands a SINGLE station and returns the list of class Path.
     Args:
         path (object of Path class): Specific path to be expanded
         map (object of Map class):: All the information needed to expand the node
     Returns:
         path_list (list): List of paths that are connected to the given path.
    """
    path_list = []
    last_station = path.last
    
    if last_station in map.connections:
        for neighbor in map.connections[last_station]:
            new_route = path.route.copy()
            new_route.append(neighbor)
            new_path = Path(new_route)
            path_list.append(new_path)
    
    return path_list


def remove_cycles(path_list):
    """
     It removes from path_list the set of paths that include some cycles in their path.
     Args:
         path_list (LIST of Path Class): Expanded paths
     Returns:
         path_list (list): Expanded paths without cycles.
    """
    result = []
    
    for path in path_list:
        if path.last not in path.route[:-1]:
            result.append(path)
    
    return result


def insert_depth_first_search(expand_paths, list_of_path):
    """
     expand_paths is inserted to the list_of_path according to DEPTH FIRST SEARCH algorithm
     Args:
         expand_paths (LIST of Path Class): Expanded paths
         list_of_path (LIST of Path Class): The paths to be visited
     Returns:
         list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """
    return expand_paths + list_of_path


def depth_first_search(origin_id, destination_id, map):
    """
     Depth First Search algorithm
     Args:
         origin_id (int): Starting station id
         destination_id (int): Final station id
         map (object of Map class): All the map information
     Returns:
         list_of_path[0] (Path Class): the route that goes from origin_id to destination_id
    """
    list_of_path = [Path(origin_id)]
    
    while list_of_path:
        current_path = list_of_path[0]
        
        if current_path.last == destination_id:
            return current_path
        
        list_of_path = list_of_path[1:]
        expanded = expand(current_path, map)
        expanded = remove_cycles(expanded)
        list_of_path = insert_depth_first_search(expanded, list_of_path)
    
    return None


def insert_breadth_first_search(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to BREADTH FIRST SEARCH algorithm
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            list_of_path (LIST of Path Class): The paths to be visited
        Returns:
            list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """
    return list_of_path + expand_paths


def breadth_first_search(origin_id, destination_id, map):
    """
     Breadth First Search algorithm
     Args:
         origin_id (int): Starting station id
         destination_id (int): Final station id
         map (object of Map class): All the map information
     Returns:
         list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    list_of_path = [Path(origin_id)]
    
    while list_of_path:
        current_path = list_of_path[0]
        
        if current_path.last == destination_id:
            return current_path
        
        list_of_path = list_of_path[1:]
        expanded = expand(current_path, map)
        expanded = remove_cycles(expanded)
        list_of_path = insert_breadth_first_search(expanded, list_of_path)
    
    return None


def calculate_cost(expand_paths, map, type_preference=0):
    """
         Calculate the cost according to type preference
         Args:
             expand_paths (LIST of Paths Class): Expanded paths
             map (object of Map class): All the map information
             type_preference: INTEGER Value to indicate the preference selected:
                             0 - Adjacency
                             1 - minimum Time
                             2 - minimum Distance
                             3 - minimum Transfers
         Returns:
             expand_paths (LIST of Paths): Expanded path with updated cost
    """
    for path in expand_paths:
        if len(path.route) == 1:
            path.g = 0
            continue
        
        last_station = path.last
        prev_station = path.penultimate
        
        if prev_station in map.connections and last_station in map.connections[prev_station]:
            if type_preference == 0:  # Adjacency
                path.g = 1  # Cada aresta compta com 1
                
            elif type_preference == 1:  # Time - USA LA MATRIU DE COSTOS!
                # Agafa el temps directament de la matriu Time.txt
                path.g = map.connections[prev_station][last_station]
                
            elif type_preference == 2:  # Distance - temps del tram x velocitat de la línia
                # Un transbord (canvi de línia a la mateixa estació) no suma distància
                if map.stations[prev_station]['line'] == map.stations[last_station]['line']:
                    temps = map.connections[prev_station][last_station]
                    path.g = temps * map.stations[prev_station]['velocity']
                else:
                    path.g = 0
                
            elif type_preference == 3:  # Transfers
                prev_line = map.stations[prev_station]['line']
                curr_line = map.stations[last_station]['line']
                path.g = 1 if prev_line != curr_line else 0
        else:
            path.g = 9999
    
    return expand_paths


def insert_cost(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to COST VALUE
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            list_of_path (LIST of Path Class): The paths to be visited
        Returns:
            list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to cost
    """
    all_paths = list_of_path + expand_paths
    all_paths.sort(key=lambda path: path.g)
    return all_paths


def uniform_cost_search(origin_id, destination_id, map, type_preference=0):
    """
     Uniform Cost Search algorithm
     Args:
         origin_id (int): Starting station id
         destination_id (int): Final station id
         map (object of Map class): All the map information
         type_preference: INTEGER Value to indicate the preference selected:
                         0 - Adjacency
                         1 - minimum Time
                         2 - minimum Distance
                         3 - minimum Transfers
     Returns:
         list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    start_path = Path(origin_id)
    start_path.g = 0
    list_of_path = [start_path]
    
    while list_of_path:
        # Ordenar per cost
        list_of_path.sort(key=lambda p: p.g)
        current_path = list_of_path[0]
        list_of_path = list_of_path[1:]
        
        if current_path.last == destination_id:
            return current_path
        
        expanded = expand(current_path, map)
        expanded = remove_cycles(expanded)
        expanded = calculate_cost(expanded, map, type_preference)
        
        for path in expanded:
            if len(path.route) > 1:
                path.g += current_path.g
        
        list_of_path.extend(expanded)
        list_of_path = insert_cost([], list_of_path)  # Reordenar
    
    return None


def calculate_heuristics(expand_paths, map, destination_id, type_preference=0):
    """
     Calculate and UPDATE the heuristics of a path according to type preference
     Args:
         expand_paths (LIST of Path Class): Expanded paths
         map (object of Map class): All the map information
         destination_id (int): Final station id
         type_preference: INTEGER Value to indicate the preference selected:
                         0 - Adjacency
                         1 - minimum Time
                         2 - minimum Distance
                         3 - minimum Transfers
     Returns:
         expand_paths (LIST of Path Class): Expanded paths with updated heuristics
    """
    for path in expand_paths:
        last_station = path.last
        
        if type_preference == 0:  # Adjacency heuristic
            # Heurística simple: 1 si no és el destí, 0 si és el destí
            path.h = 0 if last_station == destination_id else 1
            
        elif type_preference == 1:  # Time heuristic
            # Heurística: temps en línia recta (distància / velocitat màxima)
            x1, y1 = map.stations[last_station]['x'], map.stations[last_station]['y']
            x2, y2 = map.stations[destination_id]['x'], map.stations[destination_id]['y']
            distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
            max_velocity = max(map.velocity.values())
            path.h = distance / max_velocity
            
        elif type_preference == 2:  # Distance heuristic
            # Distància euclidiana directa
            x1, y1 = map.stations[last_station]['x'], map.stations[last_station]['y']
            x2, y2 = map.stations[destination_id]['x'], map.stations[destination_id]['y']
            path.h = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
            
        elif type_preference == 3:  # Transfers heuristic
            # Heurística optimista: 1 si són línies diferents, 0 si són iguals
            curr_line = map.stations[last_station]['line']
            dest_line = map.stations[destination_id]['line']
            path.h = 1 if curr_line != dest_line else 0
    
    return expand_paths


def update_f(expand_paths):
    """
      Update the f of a path
      Args:
          expand_paths (LIST of Path Class): Expanded paths
      Returns:
          expand_paths (LIST of Path Class): Expanded paths with updated costs
    """
    for path in expand_paths:
        path.f = path.g + path.h
    return expand_paths


def remove_redundant_paths(expand_paths, list_of_path, visited_stations_cost):
    """
      It removes the Redundant Paths.
      Args:
          expand_paths (LIST of Path Class): Expanded paths
          list_of_path (LIST of Path Class): All the paths to be expanded
          visited_stations_cost (dict): All visited stations cost
      Returns:
          new_paths (LIST of Path Class): Expanded paths without redundant paths
          list_of_path (LIST of Path Class): list_of_path without redundant paths
          visited_stations_cost (dict): Updated visited stations cost
    """
    new_paths = []
    
    for path in expand_paths:
        last_station = path.last
        if last_station not in visited_stations_cost or path.g < visited_stations_cost[last_station]:
            visited_stations_cost[last_station] = path.g
            new_paths.append(path)
    
    filtered_list = []
    for path in list_of_path:
        last_station = path.last
        if last_station in visited_stations_cost and path.g <= visited_stations_cost[last_station]:
            filtered_list.append(path)
        elif last_station not in visited_stations_cost:
            filtered_list.append(path)
    
    return new_paths, filtered_list, visited_stations_cost


def insert_cost_f(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to f VALUE
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            list_of_path (LIST of Path Class): The paths to be visited
        Returns:
            list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to f
    """
    all_paths = list_of_path + expand_paths
    all_paths.sort(key=lambda path: path.f)
    return all_paths


def distance_to_stations(coord, map):
    """
        From coordinates, it computes the distance to all stations in map.
        Args:
            coord (list): Two REAL values, which refer to the coordinates of a point in the city.
            map (object of Map class): All the map information
        Returns:
            (dict): Dictionary containing as keys, all the Indexes of all the stations in the map, and as values, the
            distance between each station and the coord point
    """
    distances = {}
    
    for station_id, station_info in map.stations.items():
        station_coord = (station_info['x'], station_info['y'])
        dist = math.sqrt((coord[0] - station_coord[0]) ** 2 + (coord[1] - station_coord[1]) ** 2)
        distances[station_id] = dist
    
    sorted_distances = dict(sorted(distances.items(), key=lambda item: (item[1], item[0])))
    return sorted_distances


def Astar(origin_id, destination_id, map, type_preference=0):
    """
     A* Search algorithm
     Args:
         origin_id (int): Starting station id
         destination_id (int): Final station id
         map (object of Map class): All the map information
         type_preference: INTEGER Value to indicate the preference selected:
                         0 - Adjacency
                         1 - minimum Time
                         2 - minimum Distance
                         3 - minimum Transfers
     Returns:
         list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    start_path = Path(origin_id)
    start_path.g = 0
    
    # Calcular heurística inicial
    heuristics = calculate_heuristics([start_path], map, destination_id, type_preference)
    start_path = heuristics[0]
    start_path.f = start_path.g + start_path.h
    
    list_of_path = [start_path]
    visited_stations_cost = {}
    
    while list_of_path:
        # Ordenar per f (menor primer)
        list_of_path.sort(key=lambda p: p.f)
        current_path = list_of_path[0]
        list_of_path = list_of_path[1:]
        
        if current_path.last == destination_id:
            return current_path
        
        # Marcar com visitat
        last_station = current_path.last
        if last_station not in visited_stations_cost or current_path.g < visited_stations_cost[last_station]:
            visited_stations_cost[last_station] = current_path.g
        
        # Expandir
        expanded = expand(current_path, map)
        expanded = remove_cycles(expanded)
        expanded = calculate_cost(expanded, map, type_preference)
        
        # Acumular cost
        for path in expanded:
            path.g += current_path.g
        
        # Calcular heurística i f
        expanded = calculate_heuristics(expanded, map, destination_id, type_preference)
        for path in expanded:
            path.f = path.g + path.h
        
        # Eliminar redundants
        expanded, list_of_path, visited_stations_cost = remove_redundant_paths(
            expanded, list_of_path, visited_stations_cost)
        
        # Afegir a la llista
        list_of_path.extend(expanded)
    
    return None


def Astar_improved(origin_coord, destination_coord, map):
    """
     A* Search algorithm
     Args:
         origin_coord (list): Two REAL values, which refer to the coordinates of the starting position
         destination_coord (list): Two REAL values, which refer to the coordinates of the final position
         map (object of Map class): All the map information
     Returns:
         list_of_path[0] (Path Class): The route that goes from origin_coord to destination_coord
    """
    velocitat_caminant = 5

    # Mapa ampliat: l'origen (0) i el destí (-1) són dos nodes més, connectats a peu
    # amb totes les estacions i també entre ells
    mapa = copy.deepcopy(map)
    mapa.stations[0] = {'name': 'origen', 'line': 0, 'x': origin_coord[0], 'y': origin_coord[1], 'velocity': velocitat_caminant}
    mapa.stations[-1] = {'name': 'desti', 'line': -1, 'x': destination_coord[0], 'y': destination_coord[1], 'velocity': velocitat_caminant}

    dist_origen = distance_to_stations(origin_coord, map)
    dist_desti = distance_to_stations(destination_coord, map)

    mapa.connections[0] = {}
    for estacio, dist in dist_origen.items():
        mapa.connections[0][estacio] = dist / velocitat_caminant
        mapa.connections.setdefault(estacio, {})[-1] = dist_desti[estacio] / velocitat_caminant
    directe = math.sqrt((origin_coord[0] - destination_coord[0]) ** 2 +
                        (origin_coord[1] - destination_coord[1]) ** 2)
    mapa.connections[0][-1] = directe / velocitat_caminant
    mapa.connections[-1] = {}

    # A* minimitzant el temps (preferència 1) sobre el mapa ampliat
    return Astar(0, -1, mapa, 1)
