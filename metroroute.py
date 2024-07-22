# Copyright (c) Eason Qin, 2024
# This source code form is licensed under the MIT license

from enum import Enum
from dataclasses import dataclass
from collections import deque

import colorama
import sys

class Line(Enum):
    CTL = "Central Line"
    CSL = "Coastal Line"
    APL = "Airport Line"
    HTL = "Hattakesh Line"
    RLR = "Redackistan Light Rail"

@dataclass
class Action:
    def __init__(self) -> None:
        pass   

@dataclass
class Transfer(Action):
    at: str
    from_line: Line
    to_line: Line

@dataclass
class GoTo(Action):
    to: str
    frm: str 
    on_line: Line
    stations: list[str]

@dataclass
class BeginAt(Action):
    station: str

@dataclass
class ArriveAt(Action):
    station: str

@dataclass
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

    def get_path(self, start: str, end: str) -> list[str] | None:
        if start not in self.graph or end not in self.graph:
            return None

        visited: set[str] = set()
        queue: deque[tuple[str, list[str]]] = deque([(start, [start])])

        while queue:
            current_station, path = queue.popleft()
            if current_station == end:
                return path
            if current_station not in visited:
                visited.add(current_station)
                for neighbor in self.graph[current_station]:
                    if neighbor not in visited:
                        queue.append((neighbor, path + [neighbor]))

        return None


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
        # "kadena",
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

STATION_LINES: dict[str, list[Line]] = {
    "akemane": [Line.CTL, Line.APL],
    "hasiph": [Line.CTL, Line.CSL, Line.HTL],
    "korihasiph": [Line.CTL, Line.CSL],
    "southbridge": [Line.CTL],
    "parliament": [Line.CTL, Line.APL],
    "kandami": [Line.CTL],
    "kutsimati": [Line.CTL],
    "kemigitech": [Line.CTL, Line.HTL],
    "azadimoph": [Line.CTL],
    "venice": [Line.CSL, Line.APL],
    # "kadena": [Line.CSL],
    "waisharkil": [Line.CSL],
    "dern": [Line.CSL, Line.APL],
    "detech": [Line.CSL],
    "amiri": [Line.CSL, Line.RLR],
    "snowbing": [Line.CSL],
    "airport": [Line.APL],
    "quramitu": [Line.APL],
    "hayalese": [Line.APL],
    "university": [Line.APL],
    "distaye": [Line.APL],
    "rasir piss": [Line.APL, Line.HTL],
    "marcosia": [Line.APL],
    "sanzaleka": [Line.APL],
    "damatsalan": [Line.HTL],
    "kanahide": [Line.HTL],
    "yelojaber": [Line.HTL],
    "amirkhan": [Line.RLR],
    "amiri south": [Line.RLR],
}

STATION_CODES: dict[str, list[str]] = {
    # Central Line
    "akemane": ["AP11", "CT13"],
    "hasiph": ["CT1", "CS5", "HT1"],
    "korihasiph": ["CT2", "CS4"],
    "southbridge": ["CT3"],
    "parliament": ["CT4", "AP6"],
    "kandami": ["CT5"],
    "kutsimati": ["CT6"],
    "kemigitech": ["CT7", "HT5"],
    "azadimoph": ["CT8"],

    # Airport Line
    "airport": ["AP1"],
    "venice": ["AP2", "CS1"],
    "quramitu": ["AP3"],
    "hayalese": ["AP4"],
    "university": ["AP5"],
    #parliament
    "distaye": ["AP7"],
    "rasir piss": ["AP8", "HT3"],
    "marcosia": ["AP9"],
    "sanzaleka": ["AP10"],
    # akemane
    "dern": ["AP12", "CS6"],

    # Coastal Line
    # venice
    "waisharkil": ["CS3"],
    # korihasiph, hasiph, dern
    "detech": ["CS7"],
    "amiri": ["CS8", "RL2"],
    "snowbing": ["CS9"],

    # Hattakesh Line
    # hasiph
    "damatsalan": ["HT2"],
    # rasir piss
    "kanahide": ["HT4"],
    # kemigitech
    "yelojaber": ["HT6"],

    # Redackistan Light Rail
    "amirkhan": ["RL1"],
    # amiri
    "amiri south": ["RL3"],
}

def has_common(list1: list, list2: list) -> bool:
    set1 = set(list1)
    set2 = set(list2)
    return not set1.isdisjoint(set2)

def common_line_between_stations(stations: list[str]) -> list[Line]:
    lines: list[set[Line]] = []

    if len(stations) == 0:
        raise ValueError("Not enough stations for calculaton")
     
    for station in stations:
        lines.append(set(STATION_LINES[station]))
    
    val: set[Line] = set(lines[0]).intersection(*lines[1:])
    return list(val)

def get_route_from_path(path: list[str]) -> list[Action]:
    route: list[Action] = []
    begin = ""
    buf = []
    i = 0

    while i < len(path):
        if i == 0:
            route.append(BeginAt(path[i]))
            begin = path[i]
            curline = STATION_LINES[path[i]][0]

        try:
            cond = lambda: has_common(STATION_LINES[path[i]], STATION_LINES[path[i+1]]) and curline in set(STATION_LINES[path[i]]) | set(STATION_LINES[path[i+1]])
            while cond():
                buf.append(path[i])
                i += 1
            i -= 1
        except IndexError:
            if i == len(path) - 1:
                #i -= 1
                if not isinstance(route[len(route)-1], GoTo):
                    common_lines = common_line_between_stations(buf)
                    common_line = common_lines[0] # FIXME: later
                    buf.append(path[i])

                    if isinstance(route[len(route)-1], Transfer):
                        action: Transfer = route[len(route)-1] #type: ignore
                        action.to_line = common_line
                        route[len(route)-1] = action

                    route.append(GoTo(path[i], begin, common_line, buf))
                    route.append(ArriveAt(path[i]))
                    break

        if len(STATION_LINES[path[i]]) > 1:
            curline = STATION_LINES[path[i]][0]
            route.append(GoTo(path[i], begin, curline, buf))
            nextstation = path[i+1]
            buf = [path[i], nextstation]
            route.append(Transfer(path[i], STATION_LINES[nextstation][0], STATION_LINES[path[i]][0]))
            begin = path[i]
            i+=1

    for i, actn in enumerate(route):
        if isinstance(actn, GoTo):
            buf = actn.stations
            line = common_line_between_stations(buf)[0]
            actn.on_line = line

            if isinstance(route[i+1], Transfer):
                actn.to_line = route[i+1].to_line # type: ignore
        elif isinstance(actn, Transfer):
            try:
                if isinstance(route[i-1], GoTo):
                    actn.from_line = route[i-1].on_line # type: ignore 
                
            except IndexError:
                pass

    return route

def line_to_color(line: Line) -> str:
    match line:
        case Line.CTL:
            return colorama.Fore.GREEN
        case Line.CSL:
            return colorama.Fore.RED
        case Line.APL:
            return colorama.Fore.BLUE
        case Line.HTL:
            return colorama.Fore.MAGENTA
        case Line.RLR:
            return colorama.Fore.CYAN
        case _:
            return ""

def station_code_to_line(code: str) -> Line:
    match code[:2]:
        case 'CS':
            return Line.CSL
        case 'CT':
            return Line.CTL
        case 'AP':
            return Line.APL
        case 'HT':
            return Line.HTL
        case 'RL':
            return Line.RLR
        case _:
            raise ValueError()

def display_line(line: Line):
    return f"{colorama.Style.BRIGHT}{line_to_color(line)}{line.value}{colorama.Style.RESET_ALL}"

def display_station_code(station_code: list[str]):
    res = "("
    for i, code in enumerate(station_code):
        line = station_code_to_line(code)
        color = line_to_color(line)
        txt = f"{colorama.Style.BRIGHT}{color}{code}{colorama.Style.RESET_ALL}" 
        
        if i < len(station_code) - 1:
            txt += '|'
        res += txt
    return res + ")"

def display_station(station: str):
    return f"{display_station_code(STATION_CODES[station])} {colorama.Style.BRIGHT}{station.title()}{colorama.Style.RESET_ALL}"

def display_station_list(stations: list[str]):
    txt = ""

    for i, station in enumerate(stations):
        txt += f"{display_station(station)}"

        if i == len(stations)-2:
            txt += " and "
        elif i == len(stations)-1:
            pass
        else:
            txt += ", "

    return txt


def display_route(route: list[Action]) -> str:
    txt = ""

    for action in route:
        if isinstance(action, BeginAt):
            txt += f"{colorama.Style.BRIGHT}Begin{colorama.Style.RESET_ALL} at {display_station(action.station)}"
        elif isinstance(action, GoTo):
            txt += f"{colorama.Style.BRIGHT}Go to{colorama.Style.RESET_ALL} {display_station(action.to)} from {display_station(action.frm)} on the {display_line(action.on_line)} ({len(action.stations)-1} stops)"# via {display_station_list(action.stations)}"
        elif isinstance(action, Transfer):
            txt += f"{colorama.Style.BRIGHT}Transfer from{colorama.Style.RESET_ALL} {display_station(action.at)} from the {display_line(action.from_line)} to the {display_line(action.to_line)}"
        elif isinstance(action, ArriveAt):
            txt += f"{colorama.Style.BRIGHT}Arrive at{colorama.Style.RESET_ALL} {display_station(action.station)}"
        
        txt += "\n"

    return txt

def main():
    colorama.init()

    metro = MetroNetwork()
    allstations_s: set[str] = set()
    [[allstations_s.add(s) for s in l] for l in STATIONS.values()]
    allstations = list(allstations_s)
    allstations.sort()

    for line in STATIONS.values():
        metro.add_connections(line)

    frm = input("Which station to go from? ").lower().strip()
    to = input("Which station to go to? ").lower().strip()

    if frm not in allstations_s:
        print(f"{colorama.Fore.RED}{colorama.Style.BRIGHT}!!! Station {frm} not found{colorama.Style.RESET_ALL}")

    if to not in allstations_s:
        print(f"{colorama.Fore.RED}{colorama.Style.BRIGHT}!!! Station {to} not found{colorama.Style.RESET_ALL}")

    path = metro.get_path(frm, to)

    if path == None:
        print("invalid path entered", file=sys.stderr)
        exit(1)

    route = get_route_from_path(path)
    pretty_route = display_route(route)
    cost = metro.calculate_fare(frm, to)

    print("\n" + pretty_route) 
    print(f"\nIt will cost {colorama.Style.BRIGHT}{cost} Siyyats.{colorama.Style.RESET_ALL}")

if __name__ == "__main__":
    main()
