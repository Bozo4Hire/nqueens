from math import ceil, floor
from random import choices, randint, randrange, random
from typing import Callable, List

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
# 1 es el valor optimo de fitness, y 0 el peor valor posible
def fitnessFunction(genome : Genome) -> float :
    ft = len(genome) - 1

    #print("\nGenoma a evaluar:", genome)
    #print(genomeToStr(genome))

    for i in range(len(genome)):
        found_a = False
        found_b = False
        c = 1 
        for j in range(i+1, len(genome)):
            if genome[i] == genome[j]+c and found_a == False:
                ft -= 1
                found_a = True
            if genome[i] == genome[j]-c and found_b == False:
                ft -= 1 
                found_b = True
            c += 1
    #print ("valor de fitness: ", ft)
    return round(ft/(len(genome)-1), 2)

# funcion de cruzamiento
def singlePointCrossover(p1: Genome, p2: Genome) -> Genome:
    i = randrange(floor(len(p1)/2)+1)
    p1 = p1[i:(i+ceil(len(p1)/2))]
    p2 = [k for k in p2 if k not in p1]
    p2[i:i] = p1
    return p2

# funcion de cruzamiento alternativa
def altCrossover(p1: Genome, p2: Genome, p3: Genome) -> Genome:
    i = randrange(floor(len(p1)/2)+1)
    p1 = p1[i:(i+ceil(len(p1)/2))]
    p3 = [k for k in p3 if k not in p1]
    p3[i:i] = p1

    i = randrange(floor(len(p2)/2)+1)
    p2 = p2[i:(i+ceil(len(p2)/2))]
    p3 = [k for k in p3 if k not in p2]
    p3[i:i] = p2

    return p3

# funcion de mutacion
def swappingMutation(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:
    i = randrange(len(genome))
    j = randrange(len(genome))
    if random() <= probability:
        genome[i], genome [j] = genome[j], genome[i]
        #print("Mutation took place. Swapped pos", i, "&", j)
        #print(genome)
        #print(genomeToStr(genome))
    #else:
        #print("Mutation did not took place")
    return genome

# funcion de mutacion alternativa 
def eliminativeMutation(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:
    i = randrange(len(genome))
    if random() <= probability:
        aux = genome[i]
        genome.pop(i)
        genome.extend([aux])
    return genome

# funcion para seleccionar un numero n de padres de acuerdo a su fitness
def parentSelection(population: Population, fitnessFunc: FitnessFunc, n: int) -> Population:
    return choices(
        population = population,
        weights = [fitnessFunc(genome) for genome in population],
        k = n
    )

def sortPopulation(population: Population, fitnessFunc: FitnessFunc) -> Population:
    return sorted(population, key=fitnessFunc, reverse = True)

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


# funcion principal del algoritmo genetico 
def genAlgorithm(popsize : int, genome_len : int, ngenerations : int, selCrossover : int, selMutation : int) -> Population:
    population = generatePopulation(popsize, genome_len)

    for i in range(ngenerations):
        if fitnessFunction(population[0]) == 1:
            break
        newGeneration = population[0:2]

        for j in range(0, len(population)-2):

            match selCrossover:
                case 0:
                    parents = parentSelection(population, fitnessFunction, 2)
                    offspring = singlePointCrossover(parents[0], parents[1])
                case 1:
                    parents = parentSelection(population, fitnessFunction, 3)
                    offspring = altCrossover(parents[0], parents[1], parents[2])
                case _:
                    print("Error: invalid crossover function id")
                    return

            match selMutation:
                case 0:
                    offspring = swappingMutation(offspring)
                case 1:
                    offspring = eliminativeMutation(offspring)
                case _:
                    print("Error: invalid mutation function id")
                    return

            newGeneration += [offspring]

        population = newGeneration
        population = sortPopulation(population, fitnessFunction)
    

    print("\nK - Reinas | K =", genome_len)
    print("- Tamaño de Genotipo:\t\t", genome_len)
    print("- Tamaño de Población:\t\t", popsize)
    print("- Máximo de Generaciones:\t", ngenerations)
    match selCrossover:
        case 0: 
            print("- Función de Crossover:\t\t Single Point Crossover")
        case 1:
            print("- Función de Crossover:\t\t Three-parent Crossover")
    match selCrossover:
        case 0: 
            print("- Función de Mutación:\t\t Swapping Mutation")
        case 1:
            print("- Función de Mutación:\t\t Eliminative Mutation")

    print("\n================Resultados================")
    if fitnessFunction(population[0]) == 1:
        print("Se encontró un óptimo en la generación", i+1)
    else:
        print("No se encontró un óptimo")

    print("\nMejor Resultado")
    print("Genotipo:", population[0], "\nFenotipo:")
    print(genomeToStr(population[0]))
    print("Fitness:", fitnessFunction(population[0]), "\n")

    return population

##################################################################################

newPop = genAlgorithm(16, 10, 100, 1, 1)
