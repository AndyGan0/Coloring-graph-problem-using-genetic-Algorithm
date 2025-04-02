import random
from random import choice

color = ["blue",
         "red",
         "green",
         "yellow"]


solution_template = {
  1: None,
  2: None,
  3: None,
  4: None,
  5: None,
  6: None,
  7: None,
  8: None,
  9: None,
  10: None,
  11: None,
  12: None,
  13: None
}


neighbors = [
    [1,2], [1,3], [1,12],
    [2,3], [2,4], [2,11], [2,12],
    [3,4], [3,5], [3,6], [3,7],
    [4,7], [4,9],
    [5,6],
    [6,7],
    [7,8], [7,9],
    [8,9], [8,10],
    [9,10], [9,11],
    [10,11], [10,13],
    [11,12], [11,13],
    [12,13]
]

def printSolution(solution):

    print("score ", rate_Solution(solution), "[", end =" ")

    for key, value in solution.items():
            print(key, ':', end =" ")
            
            if(value == "blue"):
                print("\u001b[36m", end ="")
            elif (value == "red"):
                print("\033[1;31;40m", end ="")
            elif (value == "green"):
                print("\033[1;32;40m", end ="")
            elif (value == "yellow"):
                print("\u001b[33m", end ="")    

            print(value, "\033[0m, ", end ="")

    print("]\n")


def create_Random_solution():
    # make new solution with the template
    RandomSolution = solution_template.copy()

    # put values
    for i in RandomSolution.keys():
        RandomSolution[i] = color[random.randint(0, 3)]        

    return RandomSolution


def rate_Solution(solution):
    score = 0

    for i in neighbors:
        if (solution[i[0]] != solution[i[1]]):
            score = score + 1

    return score
  

def giveOffsprings(parent1, parent2):    
    
    offspring1 = solution_template.copy()
    offspring2 = solution_template.copy()

    cuttingSpot = random.randint(2, 11)

    for i in range(1,cuttingSpot):
        offspring1[i] = parent1[i]
        offspring2[i] = parent2[i]

    for i in range(cuttingSpot, len(solution_template) + 1):
        offspring1[i] = parent2[i]
        offspring2[i] = parent1[i]


    return offspring1,offspring2
    

def roulette_Selection(population):
    # getting the sum and the weights
    sum = 0
    weights = []
    for i in range(len(population)):
        score_i = rate_Solution(population[i])
        sum += score_i
        weights.append(sum)


    # choosing 1st parent
    j = random.randint(0, sum) # the chosen solution base on weights
    k = 0 # chosen solution based on index
    
    while (weights[k] <= j and weights[k] != weights[-1]):
        k += 1
    parent1 = k

    parent2 = parent1
    while(parent2 == parent1):  # making sure we won't pick a solution to mate with itself
        # choosing 2nd parent
        j = random.randint(0, sum) # the chosen solution base on weights
        k = 0 # chosen solution based on index
        while (weights[k] <= j and weights[k] != weights[-1]):
            k += 1
        parent2 = k
    

    return parent1,parent2 


def createNextGeneration(old_generation):
    new_generation = []
    # adding already existing population to the new generation
    for i in old_generation:
        new_generation.append(i.copy())


    # mating process will be done 5 times (this gives 10 new offsprings)
    for i in range(10):
        # pick 2 parents
        parent1, parent2 = roulette_Selection(old_generation)
        parent1 = old_generation[parent1]
        parent2 = old_generation[parent2]

        # giving offsprings
        offspring1, offspring2 = giveOffsprings(parent1, parent2)        

        new_generation.append(offspring1)
        new_generation.append(offspring2)


    return new_generation
    
        
def Kill_Population():
    amount_of_wanted_deletes = int(len(old_generation)/10) # the amount of population we want to delete is 10%
    
    # getting the min score
    scores = []
    items_to_delete = []

    while(amount_of_wanted_deletes != 0):
        for i in old_generation:
            scores.append(rate_Solution(i))
        mininum_score = min(scores)

        # deleting the minimum score
        for i in range(len(old_generation)):
                if(scores[i] == mininum_score):
                    items_to_delete.append(i)
        
        # if amount to delete is more than the wanted one then delete only those that we need
        while(len(items_to_delete) > amount_of_wanted_deletes):
            items_to_delete.pop(int(amount_of_wanted_deletes))

        # now we know the solutions that we want to delete (items to delete)
        items_to_delete.sort()
        for i in range(len(items_to_delete)):
            temp = items_to_delete[i] - i # once the item is deleted from old_generation, old generation population will be reduced by 1
            old_generation.pop(temp)
            amount_of_wanted_deletes -= 1

        items_to_delete.clear()
        scores.clear()
        
        
def mutate():
    amount_of_population_to_mutate = int(len(old_generation)/10) # we want to mutate only 10%
    
    # choosing solutions to mutate
    solutions_to_mutate = []
    for i in range(int(amount_of_population_to_mutate)):
        temp = random.randint(0, len(old_generation)-1)
        while (temp in solutions_to_mutate):
            temp = random.randint(0, len(old_generation)-1)
        
        solutions_to_mutate.append(temp)

    # mutating
    for i in solutions_to_mutate:
        temp = random.randint(1,13)
        value = color.index(old_generation[i][temp])
        new_value = choice([i for i in range(4) if i != value])

        old_generation[i][temp] = color[new_value]

  
def find_best_score_solution():
    maxScore = 0
    index_of_max = -1
    for i in range(len(old_generation)):
        temp = rate_Solution(old_generation[i])
        if (temp > maxScore):
            maxScore = temp
            index_of_max = i

    return old_generation[index_of_max]





old_generation = []
#creating 4 random solutions and adding them in the lists with the methods
for i in range(10):
    old_generation.append(create_Random_solution())
    printSolution(old_generation[i])

for i in range(100):
    old_generation = createNextGeneration(old_generation)
    Kill_Population()
    mutate()



print("index of max: ")
printSolution(find_best_score_solution())


