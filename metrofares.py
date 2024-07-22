# Copyright (c) Eason Qin, 2024.
# This source code form is licensed under the MIT license.

import sys
from collections import deque

class MetroNetwork:
    def __init__(self):
        self.graph: dict[str, list[str]] = {}

    def add_station(self, station: str):
        if station not in self.graph:
            self.graph[station] = []

    def add_connections(self, conns: list[str]):
        for i in range(len(conns)):
            if i + 1 == len(conns):
                break

            self.add_connection(conns[i], conns[i + 1])

    def add_connection(self, station1: str, station2: str):
        self.add_station(station1)
        self.add_station(station2)
        self.graph[station1].append(station2)
        self.graph[station2].append(station1)

    def shortest_path(self, start: str, end: str) -> int | None:
        if start not in self.graph or end not in self.graph:
            return None

        visited: set[str] = set()
        queue: deque[tuple[str, int]] = deque([(start, 0)])

        while queue:
            current_station, distance = queue.popleft()
            if current_station == end:
                return distance
            if current_station not in visited:
                visited.add(current_station)
                for neighbor in self.graph[current_station]:
                    if neighbor not in visited:
                        queue.append((neighbor, distance + 1))
        return None

    def calculate_fare(self, start: str, end: str) -> int:
        distance = self.shortest_path(start, end)
        if distance is None:
            raise ValueError("invalid route")
        base_fare = 5
        additional_cost = 1 * (distance - 1)
        total_fare = base_fare + additional_cost
        return total_fare if total_fare >= 5 else -1


STATIONS: dict[str, list[str]] = {
    "central": [
        "hasiph",
        "korihasiph",
        "southbridge",
        "parliament",
        "kandami",
        "kutsimati",
        "kemigitech",
        "azadimoph",
    ],
    "coastal": [
        "venice",
        #"kadena",
        "waisharkil",
        "korihasiph",
        "hasiph",
        "dern",
        "detech",
        "amiri",
        "snowbing",
    ],
    "airport": [
        "airport",
        "venice",
        "quramitu",
        "hayalese",
        "university",
        "parliament",
        "distaye",
        "rasir piss",
        "marcosia",
        "sanzaleka",
        "akemane",
        "dern",
    ],
    "hattakesh": [
        "hasiph",
        "damatsalan",
        "rasir piss",
        "kanahide",
        "kemigitech",
        "yelojaber",
    ],
}


def main():
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    else:
        mode = input("print a [c]sv, print a [p]ython repr, or a [d]enizen map (default)? ").strip().lower()

    if mode not in "cpd":
        mode = 'd'

    metro = MetroNetwork()
    allstations_s: set[str] = set()
    [[allstations_s.add(s) for s in l] for l in STATIONS.values()]
    allstations = list(allstations_s)
    allstations.sort()

    for line in STATIONS.values():
        metro.add_connections(line)

    stations = {}

    # Calculate fare from A to E
    for start_station in allstations:
        stations[start_station] = {}

        for end_station in allstations:
            fare = metro.calculate_fare(start_station, end_station)

            if start_station == end_station:
                continue

            stations[start_station][end_station] = fare

    match mode:
        case 'c':
            from pandas import DataFrame
            from io import StringIO

            buf = StringIO()
            DataFrame(stations).write_csv(buf)
            print(buf.getvalue())
        case 'p':
            print(stations)
        case 'd':
            python_repr = str(stations)
            python_repr = python_repr.replace("{", "map<[")
            python_repr = python_repr.replace("}", "]>")
            python_repr = python_repr.replace("'", "")
            python_repr = python_repr.replace(", ",";")
            python_repr = python_repr.replace(": ", "=")
            print(python_repr)
        

if __name__ == "__main__":
    main()
