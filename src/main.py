from graph import *
from algorithms.utils import *
from algorithms.push_relable import solve_max_flow_pl, conclusion
from algorithms.ford_fulkerson import solve_max_flow_ff, conclusion
from algorithms.dinics import solve_dinic
import time
teams = ['MI', 'CSK', 'DC', 'KKR']
log = open('log.txt', 'w')

def read_ip(team):
    rem = 0
    L1 = []
    L2 = []
    wx = 0
    gx = 0
    mx = 0
    g = Graph()
    g.add_nodes(["MI", "CSK", "DC", "KKR", "MI-CSK", "MI-KKR", "MI-DC", "CSK-DC", "SRC", "SINK"])
    f_f = open('fixings.txt', 'r')
    f_s = open('scores.txt', 'r')
    standings = []
    for line in f_f:
        tokens = line.split(" ")
        if tokens[0] not in L1:
            L1.append(tokens[0])
        if team not in tokens[0]:
            rem = rem + int(tokens[1])
            g.add_edge('SRC',tokens[0], {"capacity": int(tokens[1])})
    for line in f_s:
        tokens = line.split(" ")
        if tokens[0] not in L2:
            L2.append(tokens[0])
        standings.append([tokens[0], int(tokens[1]), int(tokens[2]), int(tokens[3])])
    for stat in standings:
        if stat[0] == team:
            wx = stat[1]
            gx = stat[3]
    mx = wx+gx
    for stat in standings:
        if stat[0] != team:
            if mx>stat[1]:
                g.add_edge(stat[0], "SINK", {"capacity": mx-stat[1]})
            
    for pair in L1:
        teams = pair.split("-")
        g.add_edge(pair, teams[1], {"capacity": 10000})
        g.add_edge(pair, teams[0], {"capacity": 10000})
    return g, rem

def push_relable(team):
    g, rem = read_ip(team)
    solve_max_flow_pl(g, g.get_node("SRC"), g.get_node("SINK"))
    log.write('--------------------------------------------------------------------\n')
    log.write('Solving max flow for team {} using Push Relable Algorithm\n'.format(team))
    log.write(str(g))
    log.write('maxflow: {}\n'.format(conclusion(g)))
    print("Push Relable maxflow: " + str(conclusion(g)))
    if conclusion(g) >= rem:
        print("Push Relable Algorithm: " +team+" is not eliminated")
        return False
    else:
        print("Push Relable Algorithm: " +team+" is eliminated")
        return True

def ff(team):
    g, rem = read_ip(team)
    solve_max_flow_ff(g, g.get_node("SRC"), g.get_node("SINK"))
    log.write('--------------------------------------------------------------------\n')
    log.write('Solving max flow for team {} using Ford Fulkerson Algorithm\n'.format(team))
    log.write(str(g))
    concl= conclusion(g)
    log.write('maxflow: {}\n'.format(concl))
    print("Ford Fulkerson maxflow: "+ str(concl))
    if conclusion(g) >= rem:
        print("Ford Fulkerson Algorithm: " +team+" is not eliminated")
        return False
    else:
        print("Ford Fulkerson Algorithm: " +team+" is eliminated")
        return True


if __name__ == "__main__":
    for team in teams:
        print('--------------------------------------------------------------------')
        times={'Ford Fulkerson':time.perf_counter(),'Push Relable':time.perf_counter(),'Dinics':time.perf_counter()}
        a1=push_relable(team)
        times['Push Relable']=time.perf_counter()-times['Push Relable']
        a2=ff(team)
        times['Ford Fulkerson']=time.perf_counter()-times['Ford Fulkerson']
        a3=solve_dinic(team, log)
        times['Dinics']=time.perf_counter()-times['Dinics']
        
        if(a1==a2==a3):
            print("\nAll methods return same answer. Time to execute: ")
            times=dict(sorted(times.items(),key=lambda item: item[1]))
            for i in times.keys():
                print("{}: {}".format(i,round(times[i],5)))
log.close()

