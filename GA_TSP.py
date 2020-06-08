"""

author @jdconrado

"""
from random import random, randint

class Population:
    def __init__(self, popSize, cities, cost, start, pc, pm):
        self.pSize = popSize
        self.cities = cities
        self.costs = cost
        self.start = start
        self.pc = pc
        self.pm = pm
        self.numGen = 0
        self.individuals = []
        self.thisGenBest = None
        self.globalOpti = None
        self.fitsum = 0
        self.fitAve = 0
    
    def randomIndividual(self):
        cities = self.cities[:]
        init = 0
        if self.start is not None:
            temp = cities[0]
            cities[0] = cities[self.start]
            cities[self.start] = temp
            init = 1
        for i in range(init,len(self.cities)-1):
            j = randint(i, len(cities)-1)
            temp = cities[i]
            cities[i] = cities[j]
            cities[j] = temp
        return cities
    
    def calcInfivFitness(self, tour):
        cost = 0
        for i in range(len(tour)):
            if i == len(tour) - 1:
                cost+= self.costs[tour[i][0]-1][tour[0][0]-1]
            else:
                cost+= self.costs[tour[i][0]-1][tour[i+1][0]-1]
        return 1/cost
    
    def calcFintness(self, individuals):
        fitave = 0
        fitsum = 0
        best = None
        for i in individuals:
            fitness =  self.calcInfivFitness(i[0])
            i[1] = fitness
            if best is None:
                best = i
            elif best[1]<i[1]:
                best = i
            fitsum+= fitness
            fitave+= fitness/self.pSize
        return best, fitsum, fitave
    
    def initPopulation(self):
        for i in range(self.pSize):
            self.individuals.append([self.randomIndividual(),0,0])
        self.thisGenBest, self.fitsum, self.fitAve = self.calcFintness(self.individuals)
        self.globalOpti = self.thisGenBest
    
    def execSelection(self):
        fineIndivs = []
        for i in self.individuals:
            i[2] =  i[1]/self.fitsum
        self.individuals.sort(key= lambda e: e[2], reverse=True)
        fineIndivs.append(self.individuals[0])
        for i in range(self.pSize-1):
            probExtraction = random()
            j = 0
            sumP = self.individuals[j][2]
            while j<len(self.individuals)-1 and probExtraction > sumP:
                j+=1
                sumP+=self.individuals[j][2]
            fineIndivs.append(self.individuals[j])
        fineIndivs.sort(key= lambda e: e[2], reverse=True)
        return fineIndivs
    
    def execCrossover(self, individuals):
        parents= []
        for i in individuals:
            if random() < self.pc:
                parents.append(i)
        numPairs = len(parents)
        if numPairs % 2 != 0:
            numPairs +=1
        numPairs = round(numPairs/2)
        pairs = []
        for i in range(numPairs):
            a = randint(0, len(parents)-1)
            b = randint(0, len(parents)-1)
            pairs.append([[parents[a][0][:]], [parents[b][0][:]]])
        newGen = []
        for i in pairs:
            childx = []
            childy = []
            if self.start is not None:
                c = self.cities[self.start]
                childx.append(c)
            else:
                c = self.cities[randint(0,len(self.cities)-1)]
                childx.append(c)
            
            icopy = [[i[0][0][:]],[i[1][0][:]]]

            while len(childx) < len(self.cities):
                indexX = i[0][0].index(c)
                indexY = i[1][0].index(c)
                dx = None
                dy = None
                if indexX == len(i[0][0]) -1:
                    dx = self.costs[c[0]-1][i[0][0][0][0]-1]
                    indexX = 0
                else:
                    dx = self.costs[c[0]-1][i[0][0][indexX+1][0]-1]
                    indexX = indexX+1
                if indexY == len(i[1][0]) -1:
                    dy = self.costs[c[0]-1][i[1][0][0][0]-1]
                    indexY = 0
                else:
                    dy = self.costs[c[0]-1][i[1][0][indexY+1][0]-1]
                    indexY = indexY+1
                
                if dx <= dy:
                    cx = i[0][0][indexX]
                    i[0][0].remove(c)
                    i[1][0].remove(c)
                    childx.append(cx)
                    c = cx
                else:
                    cy = i[1][0][indexY]
                    i[0][0].remove(c)
                    i[1][0].remove(c)
                    childx.append(cy)
                    c = cy
            
            if self.start is not None:
                c = self.cities[self.start]
                childy.append(c)
            else:
                c = self.cities[randint(0,len(self.cities)-1)]
                childy.append(c)
            while len(childy) < len(self.cities):
                indexX = icopy[0][0].index(c)
                indexY = icopy[1][0].index(c)
                dx = None
                dy = None
                if indexX == 0:
                    dx = self.costs[c[0]-1][icopy[0][0][len(icopy[0][0])-1][0]-1]
                    indexX = len(icopy[0][0])-1
                else:
                    dx = self.costs[c[0]-1][icopy[0][0][indexX-1][0]-1]
                    indexX = indexX -1
                if indexY == 0:
                    dy = self.costs[c[0]-1][icopy[1][0][len(icopy[1][0])-1][0]-1]
                    indexY = len(icopy[1][0])-1
                else:
                    dy = self.costs[c[0]-1][icopy[1][0][indexY-1][0]-1]
                    indexY = indexY-1
                
                if dx <= dy:
                    cx = icopy[0][0][indexX]
                    icopy[0][0].remove(c)
                    icopy[1][0].remove(c)
                    childy.append(cx)
                    c = cx
                else:
                    cy = icopy[1][0][indexY]
                    icopy[0][0].remove(c)
                    icopy[1][0].remove(c)
                    childy.append(cy)
                    c = cy
            newGen.append([childx,0,0])
            newGen.append([childy,0,0])
        for i in range (0, self.pSize - len(newGen)):
            newGen.append([individuals[i][0][:],0,0])
        return newGen
    
    def execMutation(self, individuals):
        newGen = []
        for i in individuals:
            if random() < self.pm:
                a = randint(0, len(self.cities) -1)
                b = randint(0, len(self.cities) -1)
                if b < a:
                    temp = a
                    a = b
                    b = temp
                tour = i[0][0:a]
                rev =  i[0][a:b+1]
                rev.reverse()
                tour.extend(rev)
                tour.extend(i[0][b+1:])
                i[0] = tour
            newGen.append(i)
        return newGen
    
    def run(self):
        fineIndivs = self.execSelection()
        newGen = self.execCrossover(fineIndivs)
        newGen = self.execMutation(newGen)
        self.thisGenBest, self.fitsum, self.fitAve = self.calcFintness(newGen)
        self.individuals = newGen
        if self.globalOpti[1] < self.thisGenBest[1]:
            self.globalOpti = self.thisGenBest
        self.numGen+= 1


