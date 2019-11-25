import random; import string; import math
def random_string(stringLength, stringGenes):
    """
        Description: 
            Return a random string chromosome.
        Input:
            stringLength : Length of Chromosome/String
            stringGenes : Ascii all letters gene pool including space 
            and exclamation mark
        Out:
            ran_string_chromosome: String Object of length stringLength.
    """
    ran_string_chromosome = "".join(random.choice(stringGenes) 
                                    for i in range(stringLength))
    return ran_string_chromosome

def eval_fun(test_string, target_string):
    """
        Description:
            Evaluate an individual. Fitness Function! Chose a Root Mean Square 
            Error (RMSE) difference motivated by the flowchart from the slides 
            in lecture 1. For each character in the test and target strings 
            the builtin python function 'ord()' is used for the difference, 
            which returns for a Unicode Character a Unicode Integer value.
            This is needed as Strings are *Immutable* Objects in Python!
        Input:
            test_string : Chromosome/String from population to be tested
            target_string : The goal/ground truth string
        Out: 
            fitness : Float, summed up RMSE for each char in Unicode integer value.
    """
    fitness = 0.0
    # Calculate the RMSE difference for each char in Unicode Integer form
    # for the test_string characters compared to target_string
    for test_char, target_char in zip(test_string, target_string):
        fitness += math.sqrt((ord(test_char)-ord(target_char))**2)
    return fitness

def initial_population_generation(pop_number, target_string, string_genes):
    """
        Description: 
            Generate an initial population of chromosomes/strings.
        Input:
            pop_number : The population number
            target_string : String to be tested
            string_genes : Gene pool of letters composed of ascii characters
        Output:
            population: List of Chromosomes/Individuals.
    """
    population = []
    for i in range(pop_number):
        population.append(random_string(len(target_string), string_genes))
    return population

def crossover_individuals(sel_population, gene_language):
    """
        Descriptions:
            Crossover the random selected individuals from sel_population.
        Input:
            sel_population : List of chromosomes from ranked selection
            gene_language : String of ascii letters/gene pool
        Output:
            cross_population: List of population with new offsprings.
    """

    cross_population = random.sample(sel_population, len(sel_population))

    for parent1, parent2 in zip(cross_population[::2], cross_population[1::2]):
        lst1 = list(parent1)
        lst2 = list(parent2)
        cross_index = random.randint(1,len(lst1)-2)
        lst1[:cross_index], lst2[:cross_index] = lst2[:cross_index], lst1[:cross_index]
        parent1 = ''.join(lst1)
        parent2 = ''.join(lst2)

    return cross_population

def mutate_individuals(population, gene_language):
    """
        Descriptions:
            Mutate a random char from population by incrementing or decrementing it by one.
        Input:
            population : List of chromoses to be checked for mutation
            gene_language = String of ascii letters/gene pool
        Output:
            The individuals of population list having random chars mutated.
    """

    for i in range(len(population)):
        index = random.randint(0, len(population[i]) - 1)
        lst = list(population[i])
        random_bit_like_change = random.randint(-1,1)
        lst[index] = chr(ord(lst[index]) + random_bit_like_change)
        population[i] = ''.join(lst)
    
def select_individuals(population, target_string, gene_language):
    """
        Description:
            Select  individuals from population to be breed in ranking order.
        Input: 
            population : List of Strings to be ranked selected
            target_string : Ground Truth String
            gene_language :  String of ascii letters/gene pool
        Output:
            new_pop : List of new population
            min_fit : Float, min fitness value from pop/new_pop
            min_word : String/Chromosome for min_fit.
    """
    # Create empty list for population
    new_pop = []
    # Create new empty list for fitness values of each individual in population
    fit_list = []
    # Populaton size
    pop_size = len(population)
    for individual in population:
        fitness = eval_fun(individual, target_string)
        fit_list.append(fitness)

    # Calculate average fitness values for fun
    fitness_sum = sum(fit_list)
    average_fitness = fitness_sum/pop_size
    
    # Find minimum value in fitness list,
    # corresponding word and check if you can exit
    # before proceeding with ranked selection
    min_fit = min(fit_list)
    index = fit_list.index(min_fit)
    min_word = population[index]
    if min_fit == 0:
        return population, min_fit, min_word

    # Sort for ranking selection, both fit_list and population in sync
    population = [x for _, x in sorted(zip(fit_list, population))]
    fit_list = sorted(fit_list)
    
    # For loop for same size as old population for new one to be 
    # created using ranked selection.
    for i in range(pop_size):
        # pick index by bigger likelihood to be in first indices
        probability_ranking_index = (pop_size-1) * (random.random())**2
        # convert by casting to int
        probability_ranking_index = int(probability_ranking_index)
        new_pop.append(population[probability_ranking_index])
    
    # Print for terminal
    print("min_fit_value :",min_fit,":", new_pop[index])  

    # Return chosen population, minimum value for fitness and the word
    # corresponding to it.
    return new_pop, min_fit, min_word

def random_benchmark(target):
    """
        Description: 
            Random sampling as relative test with ga function. In this case the likelihood
            of finding it immedietely is very small. Thus we compare each char till it find randomly
            the right char and then compare total number of gens.
        Input:
            target : String to be checked.
    """
    gene_language = string.ascii_letters + ' ' + '!'
    target_list = list(target)
    test = ''.join(random.choice(gene_language) for _ in range(len(target_list)))
    test_list = list(test)
    gen = 0
    i = 0
    print(target_list)
    while i < len(target_list):
        if test_list[i] == target_list[i]:
            i += 1
            gen += 1
        else:
            test_list[i] = ''.join(random.choice(gene_language))
            gen += 1
        if gen >= 3000:
            print("Too many loops, stopping now")
            break
    # https://codegolf.stackexchange.com/questions/4707/outputting-ordinal-numbers-1st-2nd-3rd#answer-4712
    ending = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4]) # so it prints 1st, 2nd, 3rd, 4th etc correctly for generation
    print(10*"=", "RANDOM CHECK", 30*"=")
    print("Number of trials/generation comparion with ga: {}".format(ending(gen)))
    print("Target: {}".format(target_list))
    print("Test: {}".format(test_list))
    return(gen)

def genetic_algorithm_string_evolution(val_string="Welcome to CS547!", pop_number=10, gen_number=2000):
    """
        Description:
            Genetic Algorithm for String Evolution.
        Input:
            val_string : String for ground truth/target to be reached
            gen_number : Generation/Iteration number
        Output:
            Prints on terminal values for min_fit and min_word till it finds the value.
            So far inside a for loop, might change it to while so it finds the value 
            always when stopping. Relative index is for comparison along with with iter-number
            so the difference can be found for the word, or best combination of words
            through the random function check.
    """

    # Genes - consisting of all letters (e.g. a,b..A,B, etc) given by ascii + ' ' + '!'
    gene_language = string.ascii_letters + ' ' + '!'
    # Target/Ground Truth
    target_string = val_string
    # Generate population of strings
    pop_number = pop_number
    iter_number = gen_number
    string_population = initial_population_generation(pop_number, 
                                                    target_string, gene_language)

    relative_index = 0
    # Iterate for a number of Generations. Break early if fitness functions is minimizes to 0.
    for i in range(iter_number):
        # SELECTION
        string_population[:], min_fit, min_word = select_individuals(string_population, 
                                                                    target_string, gene_language)

        # Checking if fitness value is 0 so we can break out earlier
        if min_fit == 0:
            print(10*"=", "GENETIC ALGORITHM CHEK", 30*"=")
            print("Minimum fitness value : {}\nWord : {}".format(min_fit, min_word)) 
            # https://codegolf.stackexchange.com/questions/4707/outputting-ordinal-numbers-1st-2nd-3rd#answer-4712
            ending = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4]) # so it prints 1st, 2nd, 3rd, 4th etc correctly for generation
            print("FOUND AT: {} Generation/Run".format(ending(i)))
            relative_index = i
            print("Original number of runs/generations: {} \nPopulation number: {}".format(iter_number, pop_number))
            break

        # CROSSOVER
        string_population[:] = crossover_individuals(string_population, gene_language)
        
        # MUTATION
        mutate_individuals(string_population, gene_language)
    
    if relative_index !=0:
        return relative_index
    # If not found, print the best values so far:
    if min_fit != 0:
        print(10*"=", "GENETIC ALGORITHM CHEK", 30*"")
        print("Not found!\nBest min value so far: {}\nBest Word so Far: {}".format(min_fit, min_word))
        print("Iterations/Generations number: {} \nPopulation number: {}".format(iter_number,pop_number))
        return iter_number

# Here we call the ga algol, but can also tweak its values directly. Try for example pop_number=100 and gen_number = 1000
# Defaults by just calling: genetic_algorithm_string_evolution(), has the "Welcome to CS547!" as a default target string.
ga_gen_num = genetic_algorithm_string_evolution(val_string="Welcome to CS547!", pop_number=100, gen_number=1000)
random_iter_num = random_benchmark("Welcome to CS547!")
print("DIFFERENCE (Random iter number - GA generation number): {}".format(random_iter_num-ga_gen_num))