import unittest

from mochila import genetic_algorithm


class TestGeneticAlgorithmKnapsack(unittest.TestCase):

    def test_basic(self):
        values = [60, 100, 120]
        weights = [10, 20, 30]
        W = 50
        best_solution, best_value = genetic_algorithm(weights, values, W, population_size=50, generations=500, mutation_rate=0.01)
        self.assertEqual(best_value, 180)
    
    def test_small_knapsack(self):
        values = [60, 100, 120]
        weights = [10, 20, 30]
        W = 10
        best_solution, best_value = genetic_algorithm(weights, values, W, population_size=50, generations=500, mutation_rate=0.01)
        self.assertEqual(best_value, 60)

    def test_large_knapsack(self):
        values = [60, 100, 120]
        weights = [10, 20, 30]
        W = 60
        best_solution, best_value = genetic_algorithm(weights, values, W, population_size=50, generations=500, mutation_rate=0.01)
        self.assertEqual(best_value, 280)

    def test_same_weight_value(self):
        values = [10, 10, 10]
        weights = [10, 10, 10]
        W = 20
        best_solution, best_value = genetic_algorithm(weights, values, W, population_size=50, generations=500, mutation_rate=0.01)
        self.assertEqual(best_value, 20)

if __name__ == '__main__':
    unittest.main()