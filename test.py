
import temporal as tn
import numpy as np
import matplotlib.pyplot as plt


t = tn.TemporalNetwork()
t.addEdge("cins", "a", 1)
t.addEdge("e", "fed", 2)

t.addEdge("e", "a", 3)
t.addEdge("ety", "g", 4)

t.addEdge("c", "e", 5)
t.addEdge("e", "f", 6)

t.addEdge("a", "e", 7)
t.addEdge("e", "g", 8)

t.addEdge("c", "e", 9)
t.addEdge("e", "f", 10)
t.addEdge("f", "e", 11)
t.addEdge("e", "b", 12)
t.addEdge("e", "b", 13)
t.addEdge("c", "e", 14)
t.addEdge("e", "f", 15)

t.addEdge("b", "e", 16)
t.addEdge("e", "g", 17)

t.addEdge("c", "e", 18)
t.addEdge("e", "f", 19)

t.addEdge("c", "e", 20)
t.addEdge("e", "f", 21)

# print(t.Summary())
# print(t.getObservationLength())
# print(t.getInterEventTimes())
