import random

# Função para calcular a fitness de um indivíduo
def fitness(individual, coin_values, target):
    total_value = sum(ind * coin for ind, coin in zip(individual, coin_values))
    total_coins = sum(individual)
    
    # Penaliza mais fortemente o uso de moedas de valores mais baixos
    penalty = sum(ind * (len(coin_values) - i) ** 2 for i, ind in enumerate(individual))
    
    if total_value == target:
        return total_coins + penalty  # Minimiza o número de moedas usadas e a penalidade
    elif total_value < target:
        return (target - total_value) ** 2 + (total_coins + penalty) * 10  # Penaliza por não atingir o alvo
    else:
        return (total_value - target) ** 2 + (total_coins + penalty) * 10  # Penaliza por exceder o alvo

# Função para gerar um indivíduo aleatório priorizando moedas de maior valor
def generate_individual(coin_values, target):
    individual = [0] * len(coin_values)
    remaining = target
    for i in reversed(range(len(coin_values))):  # Prioriza moedas de maior valor
        individual[i] = remaining // coin_values[i]
        remaining %= coin_values[i]
    return individual

# Função para gerar uma população de indivíduos
def create_population(size, coin_values, target):
    return [generate_individual(coin_values, target) for _ in range(size)]

# Função para selecionar os melhores indivíduos
def tournament_selection(population, coin_values, target, k=3):
    selected = random.sample(population, k)
    selected.sort(key=lambda ind: fitness(ind, coin_values, target))
    return selected[0]

# Função para realizar crossover de um ponto
def one_point_crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]

# Função para realizar mutação favorecendo moedas de maior valor
def mutate(individual, coin_values, mutation_rate):
    for i in reversed(range(len(individual))):  # Prioriza mutação nas moedas de maior valor
        if random.random() < mutation_rate:
            if individual[i] > 0:
                individual[i] -= 1
            else:
                individual[i] += 1
    return individual

# Função para realizar um algoritmo genético
def genetic_algorithm(coin_values, target, population_size=100, generations=1000, mutation_rate=0.1, elite_size=2):
    population = create_population(population_size, coin_values, target)
    
    best_solution = None
    best_fitness = float('inf')
    
    for generation in range(generations):
        new_population = []
        
        # Elitismo: Preserva os melhores indivíduos da geração anterior
        if elite_size > 0:
            elite = sorted(population, key=lambda ind: fitness(ind, coin_values, target))[:elite_size]
            new_population.extend(elite)
        
        # Gerar descendentes por meio de crossover e mutação
        while len(new_population) < population_size:
            parent1 = tournament_selection(population, coin_values, target)
            parent2 = tournament_selection(population, coin_values, target)
            offspring1, offspring2 = one_point_crossover(parent1, parent2)
            offspring1 = mutate(offspring1, coin_values, mutation_rate)
            offspring2 = mutate(offspring2, coin_values, mutation_rate)
            new_population.extend([offspring1, offspring2])
        
        population = new_population
        
        # Encontrar o melhor indivíduo na população
        current_best_individual = min(population, key=lambda ind: fitness(ind, coin_values, target))
        current_best_fitness = fitness(current_best_individual, coin_values, target)
        
        if current_best_fitness < best_fitness:
            best_fitness = current_best_fitness
            best_solution = current_best_individual
        
        # Output the best fitness found in the current generation
        total_value = sum(ind * coin for ind, coin in zip(best_solution, coin_values))
        
        # Early stopping if exact solution is found
        if total_value == target and best_fitness == sum(best_solution):
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
targets = [10, 11, 15, 16, 20, 50, 75, 100, 120, 150, 200, 10000]

for target in targets:
    best_solution, _ = genetic_algorithm(coin_values, target)
    total_value = sum(coin * val for coin, val in zip(best_solution, coin_values))
    
    print(f"Target: {target}, Best Solution: {best_solution}, Total Value: {total_value}")
    verify_solution(coin_values, target, best_solution)
