from room import Room
from player import Player
from world import World
from util import Queue

# import random
from ast import literal_eval

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
graph = {}
reversed_cardinals = {
    's': 'n',
    'n': 's',
    'e': 'w',
    'w': 'e'
}


def bfs(graph, starting_vertex):
    queue = Queue()
    visited = set()
    queue.enqueue([starting_vertex])

    while queue.size():
        current_path = queue.dequeue()
        current_vertex = current_path[-1]
        if current_vertex not in visited:
            visited.add(current_vertex)
            for vertex in graph[current_vertex]:
                # print(vertex)
                if graph[current_vertex][vertex] == '?':
                    return current_path
            for neighbors in graph[current_vertex]:
                adjacent = graph[current_vertex][neighbors]
                new_path = list(current_path)
                new_path.append(adjacent)
                queue.enqueue(new_path)


while len(graph) < len(room_graph):
    current_room_id = player.current_room.id
    if current_room_id not in graph:
        graph[current_room_id] = {}
        for exits in player.current_room.get_exits():
            graph[current_room_id][exits] = '?'

    for path in graph[current_room_id]:
        if path not in graph[current_room_id]:
            break
        if graph[current_room_id][path] == '?':
            next_room = path
            if next_room is not None:
                traversal_path.append(next_room)
                player.travel(next_room)
                next_room_id = player.current_room.id
                if next_room_id not in graph:
                    graph[next_room_id] = {}
                    for exits in player.current_room.get_exits():
                        graph[next_room_id][exits] = '?'
            graph[current_room_id][next_room] = next_room_id
            graph[next_room_id][reversed_cardinals[next_room]] = current_room_id
            current_room_id = next_room_id

    room_traversal = bfs(graph, player.current_room.id)
    if room_traversal is not None:
        for room in room_traversal:
            for exits in graph[current_room_id]:
                if graph[current_room_id][exits] == room:
                    traversal_path.append(exits)
                    print(traversal_path)
                    player.travel(exits)
    current_room_id = player.current_room.id

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
