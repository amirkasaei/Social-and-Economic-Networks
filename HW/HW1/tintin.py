import heapq

def dijkstra(n, adj, sources):
    dist = [float('inf')] * n
    heap = []
    for src, d in sources:
        dist[src] = d
        heapq.heappush(heap, (d, src))
    while heap:
        current_dist, u = heapq.heappop(heap)
        if current_dist > dist[u]:
            continue
        for v, t in adj[u]:
            if dist[v] > dist[u] + t:
                dist[v] = dist[u] + t
                heapq.heappush(heap, (dist[v], v))
    return dist

# Input reading
n, m = map(int, input().split())
adj = [[] for _ in range(n)]
for _ in range(m):
    u, v, t = map(int, input().split())
    adj[u].append((v, t))
    adj[v].append((u, t))

k = int(input())
mafia_positions = [int(input()) for _ in range(k)]

c = int(input())
car_positions = set(int(input()) for _ in range(c))

v, s = map(int, input().split())

# Calculate Tintin's shortest paths
tintin_dist = dijkstra(n, adj, [(s, 0)])

# Mafia calculation without car
mafia_initial_sources = [(pos, 0) for pos in mafia_positions]
mafia_dist_no_car = dijkstra(n, adj, mafia_initial_sources)

# Calculate mafia distances with car (half speed edges)
if car_positions:
    car_sources = []
    for car_pos in car_positions:
        if mafia_dist_no_car[car_pos] != float('inf'):
            car_sources.append((car_pos, mafia_dist_no_car[car_pos]))
    mafia_dist_with_car = dijkstra(n, [[(v, t/2) for v, t in adj[u]] for u in range(n)], car_sources)
else:
    mafia_dist_with_car = [float('inf')] * n

# Final mafia arrival times
mafia_final_dist = [min(mafia_dist_no_car[i], mafia_dist_with_car[i]) for i in range(n)]

# Check if Tintin ever encounters mafia (must arrive strictly earlier than mafia everywhere)
safe = True
for i in range(n):
    if tintin_dist[i] >= mafia_final_dist[i]:
        safe = False
        break

# Special check at destination vertex
if tintin_dist[v] >= mafia_final_dist[v]:
    can_win = False
else:
    can_win = True

print("tintin" if can_win else "mafia")
