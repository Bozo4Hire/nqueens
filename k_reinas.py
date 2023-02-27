from math import ceil, floor
from random import choices, randint, randrange, random
from typing import List, Tuple

Genome = List[int]
Population = List[Genome]

# implementacion de algoritmo de Fisher-Yates para generar lista aleatoria
def fisher_yates_shuffle(list : List[int]) -> List[int]:
    auxList = range(0, len(list))
    for i in list:
        j = randint(auxList[0], auxList[-1])
        list[i], list[j] = list[j], list[i]
    return list 

# generar un genoma de longitud n, donde cada elemento corresponde
# a la fila que ocupa la reina de cada columna. Utilizamos el algoritmo
# de Yates-fisher para acomodar el genotipo de forma aleatoria de tal 
# manera que ninguna reina comparta la misma fila
def generateGenome(length : int) -> Genome:
    return fisher_yates_shuffle( list(range(0, length)))

# generar a una poblacion de  (size) n individuos
def generatePopulation(size : int, genomeLength : int) -> Population:
    return [generateGenome(genomeLength) for _ in range(size)]

# funcion para evaluar fitness de un genoma
# 0 es el valor optimo de fitness y se aleja de el al aumentar el valor
def fitnessFunction(genome : Genome) -> int :
    f1 = 0; f2 =0
    abv = [None]*len(genome)
    blw = [None]*len(genome)

    for i in range(len(genome)):
        abv[i] = genome[i]-1
        blw[i] = genome[i]+1
    
    print("\nGenoma a evaluar:", genome)
    print(genomeToStr(genome))
    print ("Diagonales: ", abv,blw)

    for i in range(1, len(genome)):
        if genome[i] == abv[i-1]: f1 += 1
        if genome[i] == blw[i-1]: f2 += 1

    print ("valor de fitness: ", f1 + f2)
    return f1 + f2
    
# funcion de cruzamiento
def singlePointCrossover(p1: Genome, p2: Genome) -> Genome:
    i = randrange(floor(len(p1)/2)+1)
    p1 = p1[i:(i+ceil(len(p1)/2))]
    p2 = [k for k in p2 if k not in p1]
    p2[i:i] = p1
    
    return p2

# funcion de mutacion
def mutation1(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:
    i = randrange(len(genome))
    j = randrange(len(genome))
    if random() <= probability:
        genome[i], genome [j] = genome[j], genome[i]
        print("Mutation took place. Swapped pos", i, "&", j)
        print(genome)
        print(genomeToStr(genome))
    else:
        print("Mutation did not took place")
    return genome

# funcion conveniente para imprimir un tablero con n reinas 
def genomeToStr(genome : Genome) -> str:
    aux = ""
    for i in range(len(genome)):
        for j in range(len(genome)):
            if genome[j] == i:
                aux += "|X|"
            else:
                aux += "|_|"
        aux += "\n"
    return aux

##################################################################################

# test de generacion de poblacion
newPop = generatePopulation(2, 8)

for i in range(len(newPop)):
    print("\n")
    print(newPop[i])
    print(genomeToStr(newPop[i]))

# test de mutacion
mutation1(newPop[0])

# test crossover
print("Padres:",newPop[0], newPop[1])
print("Hijo:", singlePointCrossover(newPop[0], newPop[1]))

# test fitnessFunction
fitnessFunction(newPop[0])