from math import ceil, floor
from random import choices, randint, randrange, random
from typing import Callable, List, Tuple

Genome = List[int]
Population = List[Genome]

FitnessFunc = Callable[[Genome], int]

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
# por ejemplo, un genoma de fitness 5 es mas apto que otro con 7
def fitnessFunction(genome : Genome) -> int :
    ft = 0

    #print("\nGenoma a evaluar:", genome)
    #print(genomeToStr(genome))

    for i in range(len(genome)):
        found_a = False
        found_b = False
        c = 1 
        for j in range(i+1, len(genome)):
            if genome[i] == genome[j]+c and found_a == False:
                ft += 1
                found_a = True
            if genome[i] == genome[j]-c and found_b == False:
                ft += 1 
                found_b = True
            c += 1
    #print ("valor de fitness: ", ft)
    return ft 

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

def sortPopulation(population: Population, fitnessFunc: FitnessFunc) -> Population:
    return sorted(population, key=fitnessFunc)

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
""" fitnessFunction([7,6,5,4,3,2,1,0])
fitnessFunction([4, 7, 3, 0, 6, 1, 5, 2])
fitnessFunction([0,1,2,3,6,5,4,7]) """

# test sortPopulation

pop = generatePopulation(5,8)
print("\nGenerada nueva poblacion\n")
for i in range(len(pop)):
    print("\n")
    print(pop[i], "Fitness:", fitnessFunction(pop[i]))
    print(genomeToStr(pop[i]))

pop = sortPopulation(pop, fitnessFunction)
print("##############################################")
for i in range(len(pop)):
    print("\n")
    print(pop[i], "Fitness:", fitnessFunction(pop[i]))
    print(genomeToStr(pop[i]))