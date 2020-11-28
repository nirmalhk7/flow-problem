import sys
from collections import deque

S = 'SRC'
T = 'SINK'

def make_auxiliar_network(edges):
    """Create an auxiliar network from a edges list
    Returns an auxiliar network."""
    s = S;t = T;na = {}
    fl = deque([s]) # parent layer
    cl = deque([])  # children layer
    level = 0
    vl = {s:level} 
    while len(fl) > 0:
        key = fl.popleft()
        for e in edges:
            if e['used']: continue
            r = e['capacity'] - e['flow']
            if key == e['first'] and  r > 0:
                v = {'id':e['last'], 'direction':'F'}
            elif key == e['last'] and e['flow'] > 0:
                v = {'id':e['first'], 'direction':'B'}
            else: continue            
            if v['id'] not in cl: 
                cl.append(v['id'])
            if key not in na:
                na[key] = []

            if v['id'] not in vl:
                vl[v['id']] = level
            if vl[v['id']] == level:
                na[key].append(v)
                e['used'] = True      
        if len(fl) == 0: fl = cl; cl = deque([]); level += 1
        if len(fl) == 0 or t in fl: break
    complete = False
    for n in [k for k in vl if vl[k] == level-1]: 
        if n == t:
            complete = True
            continue
        for k in na:
            na[k] = [v for v in na[k] if v['id'] != n]                
    return {'na':na, 'complete':complete}


def get_path(na, edges): 
    s = S; t = T
    key = s
    path = [{'id':s}]
    minflow = sys.maxsize
    complete = False
    while True:
        if key in na and len(na[key]) > 0:
            n = na[key][0]
            path.append(n)
        elif key == s:
            break
        elif key == t:
            complete = True
            break
        else:
            path.pop()
            n = path.pop()
            path.append(n) 
            for k in na:
                na[k] = [v for v in na[k] if v['id'] != key]
            key = n['id']
            continue
        r = get_residual(n, key, edges)
        if r < minflow:
            minflow = r
        key = n['id']               
    return {'path':path, 'minflow':minflow, 'complete':complete}

def get_residual(n, key, edges):
    """ Return residual capacity of node."""
    if n['direction'] == 'F':
        e = [e for e in edges if e['first'] == key and e['last'] == n['id']][0]
        r = e['capacity'] - e['flow'] 
            
    if n['direction'] == 'B':
        e = [e for e in edges if e['last'] == key and e['first'] == n['id']][0]
        r = e['flow']
    return r


def augment(na, edges, path, mincost):
    """Augment the flow in each edge from path by mincost."""   
    s = S
    first = s
    path = deque(path)
    path.popleft()
    while len(path) > 0:
        v = path.popleft()
        last = v['id']
        augment_and_delete(v, first, last, mincost, edges, na)
        first = last

def augment_and_delete(v, first, last, mincost, edges, na):
    """ Update flow in edges list for vertex v and delete edges without capacity """
    if v['direction'] == 'F':
        e = [e for e in edges if e['first'] == first and e['last'] == last][0]
        e['flow'] += mincost
            
        if e['capacity'] - e['flow'] == 0:
            na[e['first']] = [v for v in na[e['first']] if v['id'] != e['last']]

    if v['direction'] == 'B':
        e = [e for e in edges if e['last'] == first and e['first'] == last][0]
        e['flow'] -= mincost
            
        if e['flow'] == 0:
            na[e['last']] = [v for v in na[e['last']] if v['id'] != e['first']]


def dinic(edges):
    s = S
    na_num = 0
    while True:
        for e in edges:
            e['used'] = False
        data = make_auxiliar_network(edges)
        na = data['na']
        na_num += 1
        complete = data['complete']
        if not complete:
            break
        while True:
            path = get_path(na, edges)
            if path['complete']:
                augment(na, edges, path['path'], path['minflow'])
            else:
                break
    corte = get_corte(na)
    return corte, sum([e['flow'] for e in edges if e['first'] == s])

def get_corte(na):
    corte = [1]
    for k in na:
        for v in na[k]:
            if v['id'] not in corte:
                corte.append(v['id'])
    return corte

def read_edges(team):
    rem = 0
    k = ['first', 'last', 'capacity', 'flow', 'used']
    edges = []
    L1 = []
    L2 = []
    f_f = open('fixings.txt', 'r')
    f_s = open('scores.txt', 'r')
    standings = []
    for line in f_f:
        tokens = line.split(" ")
        if tokens[0] not in L1:
            L1.append(tokens[0])
        if team not in tokens[0]:
            rem = rem + int(tokens[1])
            edges.append(dict(zip(k, ["SRC", tokens[0], int(tokens[1])] + [0, False])))
    for line in f_s:
        tokens = line.split(" ")
        if tokens[0] not in L2:
            L2.append(tokens[0])
        standings.append([tokens[0], int(tokens[1]), int(tokens[2]), int(tokens[3])])
    wx = 0
    gx = 0
    mx = 0
    for stat in standings:
        if stat[0] == team:
            wx = stat[1]
            gx = stat[3]
    mx = wx+gx
    for stat in standings:
        if stat[0] != team:
            if mx-stat[1] >0:
                edges.append(dict(zip(k, [stat[0], "SINK", mx-stat[1]] + [0, False])))
    for pair in L1:
        teams = pair.split("-")
        edges.append(dict(zip(k, [pair, teams[0], 10000] + [0, False])))
        edges.append(dict(zip(k, [pair, teams[1], 10000] + [0, False])))
    return edges, rem

def solve_dinic(team, log):
    edges, rem = read_edges(team)
    corte, maxflow = dinic(edges)
    print("Dinics maxflow: " + str(maxflow))
    log.write('--------------------------------------------------------------------\n')
    log.write('Solving max flow for team {} using Dinics Algorithm\n'.format(team))
    log.write('maxflow: {}\n'.format(maxflow))
    if maxflow>=rem:
        print("Dinics Algorithm: " +team+" is not eliminated")
    else:
        print("Dinics Algorithm: " +team+" is eliminated")
