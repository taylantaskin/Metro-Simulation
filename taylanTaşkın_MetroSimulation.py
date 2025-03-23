from collections import defaultdict, deque
import heapq
from typing import Dict, List, Set, Tuple, Optional


# Represents a metro station with its identifier, name, line, and connections
class Station:
    def __init__(self, idx: str, name: str, line: str):
        self.idx = idx  # Unique identifier for the station
        self.name = name  # Name of the station
        self.line = line  # Line that the station belongs to
        self.neighbors: List[Tuple['Station', int]] = []  # List of connected stations and travel time

    # Adds a neighboring station with travel time between them
    def add_neighbor(self, station: 'Station', time: int):
        self.neighbors.append((station, time))


# Represents a metro network with stations and connections
class MetroNetwork:
    def __init__(self):
        self.stations: Dict[str, Station] = {}  # Maps station IDs to Station objects
        self.lines: Dict[str, List[Station]] = defaultdict(list)  # Maps line names to lists of stations

    # Adds a new station to the network
    def add_station(self, idx: str, name: str, line: str) -> None:
        if idx not in self.stations:
            station = Station(idx, name, line)
            self.stations[idx] = station
            self.lines[line].append(station)

    # Adds a bi-directional connection between two stations with given travel time
    def add_connection(self, station1_id: str, station2_id: str, time: int) -> None:
        station1 = self.stations[station1_id]
        station2 = self.stations[station2_id]
        station1.add_neighbor(station2, time)
        station2.add_neighbor(station1, time)

    # Finds the route with minimum number of line transfers using BFS
    def find_min_transfer_route(self, start_id: str, target_id: str) -> Optional[List[Station]]:
        if start_id not in self.stations or target_id not in self.stations:
            return None

        start = self.stations[start_id]
        target = self.stations[target_id]

        # Queue for BFS: stores (current_station, path_to_current_station, current_line)
        queue = deque([(start, [start], start.line)])
        visited = set()  # Set of visited stations to prevent re-processing

        while queue:
            current, path, current_line = queue.popleft()

            # If we reached the target station, return the path
            if current == target:
                return path

            # If we have already visited this station in this line, continue to the next
            if (current, current_line) in visited:
                continue

            visited.add((current, current_line))

            # Explore neighboring stations
            for neighbor, time in current.neighbors:
                # If the neighbor is on a different line, we count it as a transfer
                if neighbor.line != current_line:
                    queue.append((neighbor, path + [neighbor], neighbor.line))
                else:
                    queue.append((neighbor, path + [neighbor], current_line))

        return None  # No path found

    # Finds the fastest route (minimum total travel time) using A* algorithm
    def find_fastest_route(self, start_id: str, target_id: str) -> Optional[Tuple[List[Station], int]]:
        """Finds the fastest route using A* algorithm

        Complete this function:
        1. Check if the start and target stations exist
        2. Use A* algorithm to find the fastest route
        3. Return None if no route is found, otherwise return (station_list, total_time) tuple
        4. Remove the # TODO and pass lines after completing the function
        Hints:
        - Use heapq module to create a priority queue, HINT: pq = [(0, id(start), start, [start])]
        - Keep track of visited stations
        - Calculate the total time at each step
        - Select the route with the lowest time
        """
        # TODO: Complete this function
        pass
        if start_id not in self.stations or target_id not in self.stations:
            return None

        start = self.stations[start_id]
        target = self.stations[target_id]
        visited = set()


# Example Usage section - demonstrates how to create and use the metro network
if __name__ == "__main__":
    metro = MetroNetwork()

    # Add stations to the network
    # Red Line stations
    metro.add_station("K1", "Kızılay", "Red Line")
    metro.add_station("K2", "Ulus", "Red Line")
    metro.add_station("K3", "Demetevler", "Red Line")
    metro.add_station("K4", "OSB", "Red Line")

    # Blue Line stations
    metro.add_station("M1", "AŞTİ", "Blue Line")
    metro.add_station("M2", "Kızılay", "Blue Line")  # Transfer point
    metro.add_station("M3", "Sıhhiye", "Blue Line")
    metro.add_station("M4", "Gar", "Blue Line")

    # Orange Line stations
    metro.add_station("T1", "Batıkent", "Orange Line")
    metro.add_station("T2", "Demetevler", "Orange Line")  # Transfer point
    metro.add_station("T3", "Gar", "Orange Line")  # Transfer point
    metro.add_station("T4", "Keçiören", "Orange Line")

    # Add connections between stations with travel times
    # Red Line connections
    metro.add_connection("K1", "K2", 4)  # Kızılay -> Ulus
    metro.add_connection("K2", "K3", 6)  # Ulus -> Demetevler
    metro.add_connection("K3", "K4", 8)  # Demetevler -> OSB

    # Blue Line connections
    metro.add_connection("M1", "M2", 5)  # AŞTİ -> Kızılay
    metro.add_connection("M2", "M3", 3)  # Kızılay -> Sıhhiye
    metro.add_connection("M3", "M4", 4)  # Sıhhiye -> Gar

    # Orange Line connections
    metro.add_connection("T1", "T2", 7)  # Batıkent -> Demetevler
    metro.add_connection("T2", "T3", 9)  # Demetevler -> Gar
    metro.add_connection("T3", "T4", 5)  # Gar -> Keçiören

    # Transfer connections (same station different lines)
    metro.add_connection("K1", "M2", 2)  # Kızılay transfer
    metro.add_connection("K3", "T2", 3)  # Demetevler transfer
    metro.add_connection("M4", "T3", 2)  # Gar transfer

    # Test different routing scenarios
    print("\n=== Test Scenarios ===")

    # Scenario 1: From AŞTİ to OSB
    print("\n1. From AŞTİ to OSB:")
    route = metro.find_min_transfer_route("M1", "K4")
    if route:
        print("Route with least transfers:", " -> ".join(i.name for i in route))

    result = metro.find_fastest_route("M1", "K4")
    if result:
        route, time = result
        print(f"Fastest route ({time} minutes):", " -> ".join(i.name for i in route))

    # Scenario 2: From Batıkent to Keçiören
    print("\n2. From Batıkent to Keçiören:")
    route = metro.find_min_transfer_route("T1", "T4")
    if route:
        print("Route with least transfers:", " -> ".join(i.name for i in route))

    result = metro.find_fastest_route("T1", "T4")
    if result:
        route, time = result
        print(f"Fastest route ({time} minutes):", " -> ".join(i.name for i in route))

    # Scenario 3: From Keçiören to AŞTİ
    print("\n3. From Keçiören to AŞTİ:")
    route = metro.find_min_transfer_route("T4", "M1")
    if route:
        print("Route with least transfers:", " -> ".join(i.name for i in route))

    result = metro.find_fastest_route("T4", "M1")
    if result:
        route, time = result
        print(f"Fastest route ({time} minutes):", " -> ".join(i.name for i in route))