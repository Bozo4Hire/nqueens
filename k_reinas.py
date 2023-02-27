from random import choices
from typing import List

Genome = List[int]
Population = List[Genome]

def generateGenome(length : int) -> Genome:
    genotypeList = list(range(0, length-1))
    return choices(genotypeList, k=length)

def generatePopulation(size : int, genomeLength : int) -> Population:
    return [generateGenome(genomeLength) for _ in range(size)]

def genomeToStr(genome : Genome) -> str:
    aux = ""
    for i in range(len(genome)):
        for j in range(len(genome)):
            if genome[i] == j :
                aux += "X"
            else:
                aux += "_"
        aux += "\n"
    return aux

newPop = generatePopulation(2, 8)
print(newPop)
#print(genomeToStr(newPop[0]))

for i in range(len(newPop)):
    print("\n")
    print(genomeToStr(newPop[i]))
