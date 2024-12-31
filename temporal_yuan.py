# temporal network uses unimproved algorithms

import igraph as ig
import xlrd
import xlwt
import numpy as np
from collections import defaultdict
from random import choice
import pandas as pd
from collections import Counter
import random
from bisect import bisect_right
# from sets import Set
import sys  as _sys
import collections as _co
import openpyxl
import networkx as nx


class TemporalNetwork(ig.Graph):

    def __init__(self):
        ig.Graph.__init__(self)
        self.network = ig.Graph(1)
        self.tedges = []
        self.nodes = []
        self.time = defaultdict(lambda: list())
        self.targets = defaultdict(lambda: dict())
        self.sources = defaultdict(lambda: dict())
        self.activities = defaultdict(lambda: list())
        self.activities_sets = defaultdict(lambda: set())
        self.paths = _co.defaultdict(lambda: _co.defaultdict(lambda: np.array([0, 0])))
        self.ordered_times = []

        for e in self.tedges:
            self.time[e[2]].append(e)
            self.targets[e[2]].setdefault(e[1], []).append(e)
            self.sources[e[2]].setdefault(e[0], []).append(e)
            if e[0] not in self.nodes:
                self.nodes.append(e[0])
            if e[1] not in self.nodes:
                self.nodes.append(e[1])
        self.ordered_times = sorted(self.time.keys())

    def ad_vertices(self, v_list):
        for i in range(len(v_list)):
            self.network.add_vertex(v_list[i])

    def ad_edges(self, e_list):
        for i in range(len(e_list)):
            self.network.add_edge(source=e_list[i][0], target=e_list[i][1])

    def addEdge(self, source, target, start_time, end_time):
        e = (source, target, start_time, end_time)
        self.tedges.append(e)
        if source not in self.nodes:
            self.nodes.append(source)
        if target not in self.nodes:
            self.nodes.append(target)

        self.time[start_time].append(e)

        self.ordered_times = sorted(self.time.keys())

    def times_nodes(self, start_time, end_time):
        time_nodes = []
        for x in self.tedges:
            if start_time <= x[2] <= end_time:
                if x[1] not in time_nodes:
                    time_nodes.append(x[1])
                if x[0] not in time_nodes:
                    time_nodes.append(x[0])
        return time_nodes

    def time_edges(self, start_time, end_time):
        time_edges = 0
        for t in self.ordered_times:
            if start_time <= t <= end_time:
                time_edges += 1
        return time_edges

    def neighbors(self,node,vlist):
        neighbors = []
        for i in range(len(vlist)):
            if vlist[i][0] == node:
                neighbors.append(vlist[i][1])
        return neighbors

    def getObservationLength(self):
        return max(self.ordered_times) - min(self.ordered_times)

    def getInterEventTimes(self):
        timediffs = []
        for i in range(1, len(self.ordered_times)):
            timediffs += [self.ordered_times[i] - self.ordered_times[i - 1]]
        return np.array(timediffs)

    def Summary(self):
        summary = ''
        summary += 'Nodes number:\t' + str(len(self.nodes)) + '\n'
        summary += 'Edges number:\t' + str(len(self.tedges)) + '\n'
        if len(self.ordered_times) > 0:

            summary += 'Observation period:[' + str(min(self.ordered_times)) + ', ' + str(
                max(self.ordered_times)) + ']\n'
            summary += 'Time stamps:\t\t' + str(len(self.ordered_times)) + '\n'

        return summary


    def bet(self):
        btvs = []
        for p in zip(self.network.vs, self.network.betweenness()):
            btvs.append([p[0]["name"], p[1]])
        print(btvs)

        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet("Sheet")
        for i in range(len(btvs)):
            for j in range(len(btvs[i])):
                sheet.write(i, j, btvs[i][j])
        workbook.save("temporal_yuan_bet.xls")

    def randomWalk(self, vlist, stop,time):
        l1 = self.times_nodes(0,50000)
        startNode = choice(l1)
        t_list = []
        t_list.append(startNode)

        for i in range(time):
            t = 1
            while (t <= stop):
                while (len(self.neighbors(startNode,vlist))== 0):
                    startNode = choice(l1)
                    t_list = t_list[0:-1]
                    t_list.append(startNode)
                currentNode = choice(self.neighbors(startNode,vlist))
                t_list.append(currentNode)
                startNode = currentNode
                t = t + 1
                print(t)

        lista = dict(Counter(t_list))
        print(lista)

        key = list(lista.keys())
        value = list(lista.values())

        result_excel = pd.DataFrame()
        result_excel["company"] = key
        result_excel["times"] = value

        result_excel.to_excel('temporal_un.xlsx')

    def expandSubPaths(self,vlist):
        for l in range(len(vlist)):
            path = (vlist[l][0],vlist[l][1])
            frequency = 1
            self.paths[1][path] += (0,frequency)
        for pathLength in range(0,100):
            for path in self.paths[pathLength]:
                frequency = self.paths[pathLength][path][1]
                for k in range(0, pathLength):
                    for s in range(0, pathLength - k + 1):
                        self.paths[k][path[s:s + k + 1]] += (frequency, 0)

    def getShortestPaths(self):
        shortest_paths = _co.defaultdict(lambda: _co.defaultdict(lambda: set()))
        shortest_path_lengths = _co.defaultdict(lambda: _co.defaultdict(lambda: np.inf))

        for l in self.paths:
            for p in self.paths[l]:
                s = p[0]
                d = p[-1]
                if l < shortest_path_lengths[s][d]:
                    shortest_path_lengths[s][d] = l
                    shortest_paths[s][d] = set()
                    shortest_paths[s][d].add(p)
                elif l == shortest_path_lengths[s][d]:
                    shortest_paths[s][d].add(p)
        return shortest_paths
