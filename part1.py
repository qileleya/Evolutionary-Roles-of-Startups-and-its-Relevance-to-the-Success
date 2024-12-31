# static network uses unimproved algorithms

import igraph as ig
import xlrd
from random import choice
from collections import Counter
import pandas as pd
import xlwt


class randNetwk(ig.Graph):
    def __init__(self):
        ig.Graph.__init__(self)
        self.network = ig.Graph(1)

    def ad_vertices(self, v_list):
        for i in range(len(v_list)):
            self.network.add_vertex(v_list[i])

    def ad_edges(self, e_list):
        for i in range(len(e_list)):
            self.network.add_edge(source=e_list[i][0], target=e_list[i][1])

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
        workbook.save("jing_bet.xls")

    def randomWalk(self, vlist, stop,time):
        startNode = choice(vlist)
        t_list = []
        t_list.append(startNode)
        for i in range(time):
            t = 1
            while (t <= stop):
                neighbors = self.network.neighbors(startNode)
                while (neighbors.__len__() == 0):
                    startNode2 = choice(vlist)
                    neighbors = self.network.neighbors(startNode2)
                    t_list = t_list[0:-1]
                    t_list.append(startNode2)
                currentNode = choice(neighbors)
                t_list.append(vlist[currentNode-1])
                startNode = currentNode
                t = t + 1

        lista = dict(Counter(t_list))
        print(lista)

        key = list(lista.keys())
        value = list(lista.values())

        result_excel = pd.DataFrame()
        result_excel["company"] = key
        result_excel["times"] = value

        result_excel.to_excel('1.xlsx')



