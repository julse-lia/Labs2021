import itertools
from itertools import product
import math

G = {1: {2, 3},   # Введіть граф представлення зв'язків системи
     2: {4, 5},
     3: {4, 6, 8},
     4: {5, 6, 8},
     5: {6, 7},
     6: {7, 8},
     7: {7},
     8: {8}
    }

p = {1: 0.5,       # Введіть Йймовірності безвідмовної роботи елементів системи
     2: 0.6,
     3: 0.7,
     4: 0.8,
     5: 0.85,
     6: 0.9,
     7: 0.92,
     8: 0.94
     }

sources = [1]     # Введіть початкову(початкові) вершину для знаходження шляхів
ends = [7, 8]     # Введіть кінцеву(кінцеві) вершину для знаходження шляхів

def main():

    #-----------General reservation---------
    linkway = 'general'            # загальне
    reservation_mode = 'unloaded'  # ненавантажене
    time = 1000                    # час
    k = 1                          # кратність
    print(linkway, reservation_mode, "reservation:")
    general_distributed(linkway, reservation_mode, time, k)

    print()
    reservation_mode = 'loaded'    # загальне навантажене
    print(linkway, reservation_mode, "reservation:")
    general_distributed(linkway, reservation_mode, time, k)
    print()
    #----------Distributed reservation--------
    linkway = 'distributed'        # роздільне
    reservation_mode = 'unloaded'  # ненавантажене
    time = 1000                    # час
    k = 1                          # кратність
    print(linkway, reservation_mode, "reservation:")
    general_distributed(linkway, reservation_mode, time, k)

    print()
    reservation_mode = 'loaded'    # роздільне навантажене
    print(linkway, reservation_mode, "reservation:")
    general_distributed(linkway, reservation_mode, time, k)


def P_0(G, p, sources, ends):
    # DFS algorithm
    def dfs_paths(graph, start, goal, path=None):
        if path is None:
            path = [start]
        if start == goal:
            yield path
        for next in graph[start] - set(path):
            yield from dfs_paths(graph, next, goal, path + [next])

    elements = range(1, len(p) + 1)  # system objects list
    pos_states = []
    for i in range(1, len(elements)+1):
        pos_states += list(itertools.combinations(elements, i))


    if len(G) == 0:
        print("P_системи = 0")
    elif len(G) == 1:
        print("P_системи = ", + p[list(p.keys())[0]])
    else:
        paths = []

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
        return round(p_system, 6)

def P_system(G, p, sources, ends):
    return P_0(G, p, sources, ends)

# def Q_system(G, p, sources, ends):
#     return 1 - P_0(G, p, sources, ends)

def P_reserved_system(linkway, mode, K, Q_system):
    if linkway == 'general':
        if mode == 'unloaded':
            return 1 - (1 / math.factorial(K + 1)) * Q_system
        elif mode == 'loaded':
            return 1 - pow(Q_system, K + 1)
    elif linkway == 'distributed':
        P_reserved_i = {}
        if mode == 'unloaded':
            for k in p.keys():
                P_reserved_i[k] = 1 - (1 / math.factorial(K + 1)) * (1 - p[k])
            return P_0(G, P_reserved_i, sources, ends)
        elif mode == 'loaded':
            for k in p.keys():
                P_reserved_i[k] = 1 - pow(1 - p[k], K + 1)
            return P_0(G, P_reserved_i, sources, ends)
def T_system(time, P_system):
    return round((- time) / math.log(P_system))

def T_reserved_system(time, P_reserved_system):
    return round((- time) / math.log(P_reserved_system))

def G_q(Q_reserved_system, Q_system):
    return Q_reserved_system / Q_system

def G_p(P_reserved_system, P_system):
    return P_reserved_system / P_system

def G_t(T_reserved_system, T_system):
    return T_reserved_system / T_system



def general_distributed(linkway, mode, time, K):
    p_system = P_system(G, p, sources, ends)
    print("P_system =", p_system)
    q_system = 1 - p_system
    print("Q_system = ", q_system)
    p_reserved_system = P_reserved_system(linkway, mode, K, q_system)
    print("P_reserved_system =", p_reserved_system)
    q_reserved_system = 1 - p_reserved_system
    print("Q_reserved_system =", q_reserved_system)
    t_system = T_system(time, p_system)
    print("T_system =", round(t_system))
    t_reserved_system = T_reserved_system(time, p_reserved_system)
    print("T_reserved_system =", round(t_reserved_system))
    g_q = G_q(q_reserved_system, q_system)
    print("G_q =", round(g_q, 2))
    g_p = G_p(p_reserved_system, p_system)
    print("G_p =", round(g_p, 2))
    g_t = G_t(t_reserved_system, t_system)
    print("G_t =", round(g_t, 2))
    return

if __name__ == '__main__':
    main()
