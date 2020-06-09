import sys
from math import sqrt
from GATsp import Population

f = open("n20w20.001.txt","r")
lines = f.readlines()
f.close()

def extractCrities(lines):
    vector = []
    for line in lines:
        data = line.replace("      ","\t").split("\t")
        vector.append((int(data[0].strip()),float(data[1].strip()), float(data[2].strip())))
    return vector

def costMatrix(cities):
    matrix=[]
    for i in range(0, len(cities)):
        matrix.append( [ sqrt( (cities[i][1]- cities[j][1])**2 + (cities[i][2]- cities[j][2])**2 ) for j in range (0, len(cities))] )
    return matrix


cities = extractCrities(lines[6:len(lines)-1]) #From 5 when 100, 6 when 20
costs = costMatrix(cities)

pop = Population(100, cities, costs, 0, 0.5, 0.05, 100)
pop.initPopulation()
print("-------------------------------------")
print("Generation #",pop.numGen)
print("Current Average cost=",1/pop.fitAve)
print("This generation best tour: ",[e[0] for e in pop.thisGenBest[0]])
print("This generation best cost: ",1/pop.thisGenBest[1])
print("Current global optimum tour: ", [e[0] for e in  pop.globalOpti[0]])
print("Current global optimum cost: ", 1/pop.globalOpti[1])

for i in range(100):
    pop.run()
    print("-------------------------------------")
    print("Generation #",pop.numGen)
    print("Current Average cost=",1/pop.fitAve)
    print("This generation best tour: ",[e[0] for e in pop.thisGenBest[0]])
    print("This generation best cost: ",1/pop.thisGenBest[1])
    print("Current global optimum tour: ", [e[0] for e in  pop.globalOpti[0]])
    print("Current global optimum cost: ", 1/pop.globalOpti[1])


