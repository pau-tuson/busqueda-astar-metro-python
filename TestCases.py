import unittest
from SearchAlgorithm import (
    __author__, expand, calculate_cost, calculate_heuristics, remove_cycles, depth_first_search,
    breadth_first_search, uniform_cost_search, remove_redundant_paths, distance_to_stations, Astar, Astar_improved)
from SubwayMap import Path
from utils import print_list_of_path_with_cost, read_station_information, read_cost_table, read_information
import os


def create_path_with_cost_g(list_nodes, cost_g):
    path = Path(list_nodes)
    path.g = cost_g
    return path


def print_paths(new_paths, list_of_path_removed):
    print('\nNew expanded paths:')
    print_list_of_path_with_cost(new_paths)
    print('List of paths:')
    print_list_of_path_with_cost(list_of_path_removed)


def get_cost(path, subway_map, type_preference):
    new_path = Path([path.head])
    for i in range(1, len(path.route)):
        new_path.add_route(path.route[i])
        paths_with_cost = calculate_cost([new_path], subway_map, type_preference)
        new_path = paths_with_cost[0]
    return new_path


class TestCases(unittest.TestCase):
    ROOT_FOLDER = 'CityInformation/Lyon_smallCity/'  # RUTA CORREGIDA!

    def setUp(self):
        subway_map = read_station_information(os.path.join(self.ROOT_FOLDER, 'Stations.txt'))
        connections = read_cost_table(os.path.join(self.ROOT_FOLDER, 'Time.txt'))
        subway_map.add_connection(connections)

        info_velocity_clean = read_information(os.path.join(self.ROOT_FOLDER, 'InfoVelocity.txt'))
        subway_map.add_velocity(info_velocity_clean)

        self.map = subway_map

    def test_Expand(self):
        expanded_paths = expand(Path(7), self.map)
        self.assertEqual(expanded_paths, [Path([7, 6]), Path([7, 8])])

        expanded_paths = expand(Path([13, 12]), self.map)
        self.assertEqual(expanded_paths, [Path([13, 12, 8]), Path([13, 12, 11]), Path([13, 12, 13])])

        expanded_paths = expand(Path([14, 13, 8, 12]), self.map)
        self.assertEqual(expanded_paths, [Path([14, 13, 8, 12, 8]),
                                          Path([14, 13, 8, 12, 11]),
                                          Path([14, 13, 8, 12, 13])])

    def test_RemoveCycles(self):
        expanded_paths = expand(Path(7), self.map)
        expanded_paths = remove_cycles(expanded_paths)
        self.assertEqual(expanded_paths, [Path([7, 6]), Path([7, 8])])

        expanded_paths = expand(Path([13, 12]), self.map)
        expanded_paths = remove_cycles(expanded_paths)
        self.assertEqual(expanded_paths, [Path([13, 12, 8]), Path([13, 12, 11])])

        expanded_paths = expand(Path([14, 13, 8, 12]), self.map)
        expanded_paths = remove_cycles(expanded_paths)
        self.assertEqual(expanded_paths, [Path([14, 13, 8, 12, 11])])

    def test_depth_first_search(self):
        route1 = depth_first_search(2, 7, self.map)
        route2 = depth_first_search(13, 1, self.map)
        route3 = depth_first_search(5, 12, self.map)
        route4 = depth_first_search(14, 10, self.map)

        self.assertEqual(route1, Path([2, 5, 6, 7]))
        self.assertEqual(route2, Path([13, 8, 7, 6, 5, 2, 1]))
        self.assertEqual(route3, Path([5, 2, 10, 11, 12]))
        self.assertEqual(route4, Path([14, 13, 8, 7, 6, 5, 2, 10]))

    def test_breadth_first_search(self):
        route1 = breadth_first_search(2, 7, self.map)
        route2 = breadth_first_search(13, 1, self.map)
        route3 = breadth_first_search(5, 12, self.map)
        route4 = breadth_first_search(14, 10, self.map)

        self.assertEqual(route1, Path([2, 5, 6, 7]))
        self.assertEqual(route2, Path([13, 12, 11, 10, 2, 1]))
        self.assertEqual(route3, Path([5, 10, 11, 12]))
        self.assertEqual(route4, Path([14, 13, 12, 11, 10]))

    def test_calculate_cost(self):
        list_of_path = [Path([7, 6]), Path([7, 8])]
        updated_paths = calculate_cost(list_of_path, self.map, type_preference=0)
        self.assertEqual([path.g for path in updated_paths], [1, 1])

        list_of_path = [Path([7, 6]), Path([7, 8])]
        updated_paths = calculate_cost(list_of_path, self.map, type_preference=1)
        self.assertEqual([round(path.g, 5) for path in updated_paths], [4.21429, 6.03739])

        list_of_path = [Path([7, 6]), Path([7, 8])]
        updated_paths = calculate_cost(list_of_path, self.map, type_preference=2)
        self.assertEqual([round(path.g, 5) for path in updated_paths], [59.00006, 84.52346])

        list_of_path = [Path([7, 6]), Path([7, 8])]
        updated_paths = calculate_cost(list_of_path, self.map, type_preference=3)
        self.assertEqual([path.g for path in updated_paths], [0, 0])

    def test_uniform_cost_search(self):
        route = uniform_cost_search(9, 3, self.map, 0)
        self.assertTrue(route == Path([9, 8, 7, 6, 5, 2, 3]) or route == Path([9, 8, 12, 11, 10, 2, 3]))

        route = uniform_cost_search(9, 3, self.map, 1)
        self.assertEqual(route, Path([9, 8, 12, 11, 10, 2, 3]))

        route = uniform_cost_search(9, 3, self.map, 2)
        self.assertEqual(route, Path([9, 8, 12, 11, 10, 2, 3]))

        route = uniform_cost_search(9, 3, self.map, 3)
        self.assertEqual(route, Path([9, 8, 7, 6, 5, 2, 3]))

    def test_calculate_heuristics(self):
        expanded_paths = [Path([12, 8, 7]), Path([12, 8, 9]), Path([12, 8, 13])]
        updated_paths = calculate_heuristics(expanded_paths, self.map, destination_id=9, type_preference=0)
        self.assertEqual([path.h for path in updated_paths], [1, 0, 1])

        expanded_paths = [Path([12, 8, 7]), Path([12, 8, 9]), Path([12, 8, 13])]
        updated_paths = calculate_heuristics(expanded_paths, self.map, destination_id=9, type_preference=1)
        self.assertEqual([round(path.h, 5) for path in updated_paths], [1.85446, 0.0, 0.62736])

        expanded_paths = [Path([12, 8, 7]), Path([12, 8, 9]), Path([12, 8, 13])]
        updated_paths = calculate_heuristics(expanded_paths, self.map, destination_id=9, type_preference=2)
        self.assertEqual([round(path.h, 5) for path in updated_paths], [83.45058, 0.0, 28.23119])

        expanded_paths = [Path([12, 8, 7]), Path([12, 8, 9]), Path([12, 8, 13])]
        updated_paths = calculate_heuristics(expanded_paths, self.map, destination_id=9, type_preference=3)
        self.assertEqual([path.h for path in updated_paths], [0, 0, 1])

    def test_remove_redundant_path(self):
        path_1 = create_path_with_cost_g([12, 8, 7], 84.52)
        path_2 = create_path_with_cost_g([12, 8, 13, 9], 235.23)
        path_3 = create_path_with_cost_g([12, 8, 15, 11], 350.12)
        list_of_path = [path_1, path_2, path_3]
        
        expand_paths = [create_path_with_cost_g([12, 8, 7, 11], 124.52),
                        create_path_with_cost_g([12, 8, 7, 15], 222.52)]
        cost_dict = {11: 350.12, 13: 135.87, 7: 84.52, 9: 235.23, 15: 400}
        
        new_paths, list_of_path_removed, _ = remove_redundant_paths(expand_paths, list_of_path, cost_dict)
        self.assertEqual(len(list_of_path_removed), 2)
        self.assertEqual(len(new_paths), 2)

        cost_dict = {11: 350.12, 13: 135.87, 7: 84.52, 9: 235.23, 15: 200.10}
        expand_paths = [create_path_with_cost_g([12, 8, 7, 11], 124.52),
                        create_path_with_cost_g([12, 8, 7, 15], 222.52)]
        new_paths, list_of_path_removed, _ = remove_redundant_paths(expand_paths, list_of_path, cost_dict)
        self.assertEqual(len(list_of_path_removed), 2)
        self.assertEqual(len(new_paths), 1)

    def test_distance_to_stations(self):
        distances = distance_to_stations([100, 200], self.map)
        self.assertEqual(
            {k: round(v, 2) for k, v in distances.items()},
            {8: 10.0, 12: 10.0, 13: 10.0, 9: 24.76, 7: 58.73, 14: 60.03, 11: 66.48, 6: 93.94,
             1: 125.42, 2: 149.45, 5: 149.45, 10: 149.45, 3: 151.61, 4: 177.56}
        )

    def test_Astar(self):
        optimal_path = Astar(8, 1, self.map, 0)
        self.assertEqual(optimal_path, Path([8, 7, 6, 5, 2, 1]))
        self.assertEqual(round(optimal_path.f, 2), 5.0)

        optimal_path = Astar(2, 6, self.map, 1)
        self.assertEqual(optimal_path, Path([2, 5, 6]))
        self.assertEqual(round(optimal_path.f, 2), 27.14)

        optimal_path = Astar(9, 4, self.map, 2)
        self.assertEqual(optimal_path, Path([9, 8, 12, 11, 10, 5, 4]))
        self.assertEqual(round(optimal_path.f, 2), 326.54)

        optimal_path = Astar(3, 14, self.map, 3)
        self.assertTrue(optimal_path == Path([3, 2, 10, 11, 12, 13, 14]) or
                        optimal_path == Path([3, 2, 5, 6, 7, 8, 13, 14]))
        self.assertEqual(optimal_path.f, 2)

    def test_Astar_improved(self):
        optimal_path = Astar_improved([80, 100], [100, 240], self.map)
        self.assertEqual(optimal_path.route, [0, 11, 12, -1])
        self.assertEqual(round(optimal_path.f, 6), 18.417006)

        optimal_path = Astar_improved([80, 180], [180, 50], self.map)
        self.assertEqual(optimal_path.route, [0, 12, 11, 10, -1])
        self.assertEqual(round(optimal_path.f, 6), 20.516129)

        optimal_path = Astar_improved([7, 250], [184, 127], self.map)
        self.assertEqual(optimal_path.route, [0, 9, 8, 7, -1])
        self.assertEqual(round(optimal_path.f, 6), 35.592522)

        optimal_path = Astar_improved([160, 180], [80, 170], self.map)
        self.assertEqual(optimal_path.route, [0, -1])
        self.assertEqual(round(optimal_path.f, 6), 16.124515)


if __name__ == "__main__":
    unittest.main()