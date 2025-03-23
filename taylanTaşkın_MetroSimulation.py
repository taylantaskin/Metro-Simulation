from collections import defaultdict, deque
import heapq


# A metro station with name, line and connections
class Station:
    def __init__(self, idx, name, line):
        self.idx = idx  # Unique ID for the station
        self.name = name  # Name of the station
        self.line = line  # Line the station belongs to
        self.neighbors = []  # Connected stations and travel times

    # Add a connection to another station
    def add_neighbor(self, station, time):
        self.neighbors.append((station, time))


# Metro network with stations and connections
class MetroNetwork:
    def __init__(self):
        self.stations = {}  # Maps station IDs to Station objects
        self.lines = defaultdict(list)  # Maps line names to stations

    # Add a new station to the network
    def add_station(self, idx, name, line):
        station = Station(idx, name, line)
        self.stations[idx] = station
        self.lines[line].append(station)

    # Connect two stations with travel time
    def add_connection(self, station1_id, station2_id, time):
        station1 = self.stations[station1_id]
        station2 = self.stations[station2_id]
        station1.add_neighbor(station2, time)
        station2.add_neighbor(station1, time)

    # Find route with minimum transfers
    def find_min_transfer_route(self, start_id, target_id):
        start = self.stations[start_id]
        target = self.stations[target_id]

        queue = deque([(start, [start], start.line)])
        visited = set()

        while queue:
            current, path, current_line = queue.popleft()

            if current.idx == target.idx:  # Manuel karşılaştırma
                return self._clean_path(path)

            if (current.idx, current_line) in visited:
                continue

            visited.add((current.idx, current_line))

            for neighbor, _ in current.neighbors:
                new_path = path.copy()

                if neighbor.line != current_line:
                    if neighbor.name != current.name:
                        new_path.append(neighbor)
                    queue.append((neighbor, new_path, neighbor.line))
                else:
                    # Check if neighbor is already in path
                    in_path = False
                    for station in path:
                        if station.idx == neighbor.idx:
                            in_path = True
                            break

                    if not in_path:
                        new_path.append(neighbor)
                        queue.append((neighbor, new_path, current_line))

        return None

    # Find fastest route considering transfer times
    def find_fastest_route(self, start_id, target_id):
        start = self.stations[start_id]
        target = self.stations[target_id]

        # Transfer penalty in minutes
        def heuristic(station, target):
            return 0 if station.line == target.line else 5

        counter = 0
        queue = [(heuristic(start, target), counter, 0, start, [start], start.line)]
        visited = {}

        while queue:
            _, _, current_time, current, path, current_line = heapq.heappop(queue)

            if current.idx == target.idx:  # Manuel karşılaştırma
                return self._clean_path(path), current_time

            if (current.idx, current_line) in visited and visited[(current.idx, current_line)] <= current_time:
                continue

            visited[(current.idx, current_line)] = current_time

            for neighbor, travel_time in current.neighbors:
                new_time = current_time + travel_time
                counter += 1
                new_path = path.copy()

                if neighbor.line != current_line:
                    if neighbor.name != current.name:
                        new_path.append(neighbor)

                    heapq.heappush(
                        queue,
                        (new_time + heuristic(neighbor, target), counter, new_time,
                         neighbor, new_path, neighbor.line)
                    )
                else:
                    # Check if neighbor is already in path
                    in_path = False
                    for station in path:
                        if station.idx == neighbor.idx:
                            in_path = True
                            break

                    if not in_path:
                        new_path.append(neighbor)
                        heapq.heappush(
                            queue,
                            (new_time + heuristic(neighbor, target), counter, new_time,
                             neighbor, new_path, current_line)
                        )

        return None

    # Remove duplicate stations from path
    def _clean_path(self, path):
        result = []
        for i, station in enumerate(path):
            if i > 0 and station.name == path[i - 1].name:
                continue
            result.append(station)
        return result

# Example Usage
if __name__ == "__main__":
    metro = MetroNetwork()

    # Add stations
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

    # Add connections with travel times
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

    # Transfer connections
    metro.add_connection("K1", "M2", 2)  # Kızılay transfer
    metro.add_connection("K3", "T2", 3)  # Demetevler transfer
    metro.add_connection("M4", "T3", 2)  # Gar transfer

    # Test scenarios
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