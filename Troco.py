import random

# Function to calculate the fitness of an individual
def fitness(individual, coin_values, target):
    total_value = sum(ind * coin for ind, coin in zip(individual, coin_values))
    if total_value == target:
        return sum(individual)  # Minimize the number of coins used
    elif total_value < target:
        return (target - total_value) ** 3  # Penalize for not reaching the target (cubic penalty)
    else:
        return (total_value - target) ** 3  # Penalize for exceeding the target (cubic penalty)

# Function to generate a random individual
def generate_individual(n):
    return [random.randint(0, 1) for _ in range(n)]

# Function to generate a population of individuals
def create_population(size, n):
    return [generate_individual(n) for _ in range(size)]

# Function to select the best individuals
def tournament_selection(population, coin_values, target, k=3):
    selected = random.sample(population, k)
    selected.sort(key=lambda ind: fitness(ind, coin_values, target))
    return selected[0]

# Function to perform a crossover of a point
def one_point_crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]

# Function to perform a mutation
def mutate(individual, mutation_rate):
    return [gene if random.random() > mutation_rate else 1 - gene for gene in individual]

# Function to perform a genetic algorithm
def genetic_algorithm(coin_values, target, population_size=200, generations=3000, mutation_rate=0.1, elite_size=2):
    n = len(coin_values)
    population = create_population(population_size, n)
    
    best_solution = None
    best_fitness = float('inf')
    
    for generation in range(generations):
        new_population = []
        
        # Elitism: Preserve the best individuals from the previous generation
        if elite_size > 0:
            elite = sorted(population, key=lambda ind: fitness(ind, coin_values, target))[:elite_size]
            new_population.extend(elite)
        
        # Generate offspring through crossover and mutation
        while len(new_population) < population_size:
            parent1 = tournament_selection(population, coin_values, target)
            parent2 = tournament_selection(population, coin_values, target)
            offspring1, offspring2 = one_point_crossover(parent1, parent2)
            offspring1 = mutate(offspring1, mutation_rate)
            offspring2 = mutate(offspring2, mutation_rate)
            new_population.extend([offspring1, offspring2])
        
        population = new_population
        
        # Find the best individual in the population
        current_best_individual = min(population, key=lambda ind: fitness(ind, coin_values, target))
        current_best_fitness = fitness(current_best_individual, coin_values, target)
        
        if current_best_fitness < best_fitness:
            best_fitness = current_best_fitness
            best_solution = current_best_individual
        
        # Output the best fitness found in the current generation
        total_value = sum(ind * coin for ind, coin in zip(best_solution, coin_values))
        # print(f"Generation {generation}: Best Value = {total_value}, Best Fitness = {best_fitness}")
        
        # Early stopping if exact solution is found
        if total_value == target:
            break
    
    return best_solution, best_fitness

# Verifying the solution
def verify_solution(coin_values, target, solution):
    total = sum(coin * val for coin, val in zip(solution, coin_values))
    if total == target:
        print(f"A solução é válida e atinge o valor alvo. Total obtido: {total}, Valor alvo: {target}")
    elif abs(total - target) <= 1:
        print(f"A solução é válida e atinge ou está dentro da faixa aceitável do valor alvo. Total obtido: {total}, Valor alvo: {target}") 
    else:
        print(f"A solução é inválida. Total obtido: {total}, Valor alvo: {target}")


# Example of use
coin_values = [1, 5, 10, 25, 50, 100]  # Values of the coins
targets = [10, 11, 15, 16, 20, 50, 75, 100, 120, 150, 200, 250, 300, 350]
                   

for target in targets:
        best_solution, _ = genetic_algorithm(coin_values, target)
        total_value = sum(coin * val for coin, val in zip(best_solution, coin_values))
        
        print(f"Target: {target}, Best Solution: {best_solution}, Total Value: {total_value}")
        verify_solution(coin_values, target, best_solution)
       
# best_solution, best_value = genetic_algorithm(coin_values, target)
# print("Melhor Solução: ", best_solution)
# print("Valor Total das Moedas: ", sum(coin * val for coin, val in zip(best_solution, coin_values)))
# print("Número de Moedas: ", sum(best_solution))

