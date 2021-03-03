import itertools
from itertools import product

# DFS algorithm
def dfs_paths(graph, start, goal, path=None):
    if path is None:
        path = [start]
    if start == goal:
        yield path
    for next in graph[start] - set(path):
        yield from dfs_paths(graph, next, goal, path + [next])


p = {1: 0.59,  # input system objects list probabilities
     2: 0.89,
     3: 0.55,
     4: 0.22,
     5: 0.70
     }
elements = range(1, len(p)+1) # system objects list

G = {1: {2, 3},   # input graph
     2: {4},
     3: {4, 5},
     4: {5},
     5: {5}
    }

pos_states = []
for i in range(1,len(elements)+1):
    pos_states += list(itertools.combinations(elements, i))

if len(G) == 0:
    print("P_системи = 0")
elif len(G) == 1:
    print("P_системи = ", + p[list(p.keys())[0]])
else:
    paths = []  # список усіх знайдених шляхів

    sources = [1]  # input your source nodes
    ends = [5]     # input your end nodes

    for i in list(product(sources, ends)):
        for j in list(dfs_paths(G, i[0], i[1])):
            paths.append(j)

    d_list = []

    for state, path in itertools.product(pos_states, paths):
        if set(path).issubset(state):
            d_list.append(list(state))

    d_list.sort()
    work_states = list(d_list for d_list,_ in itertools.groupby(d_list))
    p_states = []

    for e in work_states:
        ps = 1
        for i in e:
            ps = ps * p[i]
        for j in set(elements) - set(e):
            ps = ps * (1 - p[j])
        p_states.append(ps)
    # ймовірність безвідмовної роботи системи
    p_system = sum(p_states)
    print('P_системи =',round(p_system, 6))



