"""
Tests for the ga (genetic algorithm) module
"""
from foox.ga import genetic_algorithm
import unittest
from mock import MagicMock

class TestGeneticAlgorithm(unittest.TestCase):
    """
    Ensures the genetic_algorithm generator function works as expected.
    """

    def test_yields_starting_population(self):
        """
        Ensures that the first item yielded *is* the starting population.
        """
        start_pop = [3, 2, 1]
        ga = genetic_algorithm(start_pop, None, None, None)
        self.assertEqual(ga.next(), start_pop,
            "Starting population not yielded as first result.")

    def test_fitness_called_for_starting_population(self):
        """
        Ensures the fitness function is called before yielding the starting
        population.
        """
        start_pop = [1, 2, 3]
        mock_fitness = MagicMock(return_value=None)
        ga = genetic_algorithm(start_pop, mock_fitness, None, None)
        result = ga.next()
        self.assertEqual(len(start_pop), mock_fitness.call_count,
            "Fitness function not called for each genome.")

    def test_starting_population_fitness_ordered(self):
        """
        Ensures that the starting population as returned by the GA is ordered
        according to the fitness function.
        """
        start_pop = [1, 2, 3]

        def fitness(genome):
            """
            For illustrative purposes.
            """
            return genome * genome

        ga = genetic_algorithm(start_pop, fitness, None, None)
        expected = [3, 2, 1]
        actual = ga.next()
        self.assertEqual(actual, expected,
            "Actual: %r Expected: %r" % (actual, expected))

    def test_halt_function(self):
        """
        Ensures that the halt function is called for all subsequent yields after
        yielding the starting population.
        """
        start_pop = [1, 2, 3]

        def fitness(genome):
            """
            For illustrative purposes.
            """
            return genome

        def halt(population, generation_count):
            """
            Halts the algorithm after ten populations.
            """
            return generation_count == 10

        class Generate(object):
            """
            As simple as possible. See generate related test below.
            """
            def __init__(self, parents):
                pass

            def __iter__(self):
                return self

            def next(self):
                raise StopIteration()

        ga = genetic_algorithm(start_pop, fitness, Generate, halt)
        result = [p for p in ga]
        actual = len(result)
        expected = 10
        self.assertEqual(actual, expected,
            "Actual: %r Expected: %r" % (actual, expected))

    def test_generate(self):
        """
        Ensures that the generate iterable is used to create new generations.
        """
        start_pop = [1, 2, 3]

        def fitness(genome):
            """
            For illustrative purposes.
            """
            return genome

        def halt(population, generation_count):
            """
            Halts the algorithm after ten populations.
            """
            return generation_count == 10

        class Generate(object):
            """
            An iterable for producing new offspring.
            """

            def __init__(self, parent_population):
                """
                @param parent_population: the parent genomes.
                """
                self.counter = 0
                self.size = len(parent_population)
                self.parents = parent_population

            def __iter__(self):
                return self

            def next(self):
                """
                For testing purposes only.
                """
                if self.counter < self.size:
                    pos, self.counter = self.counter, self.counter + 1
                    return self.parents[pos] + 1
                else:
                    raise StopIteration()

        ga = genetic_algorithm(start_pop, fitness, Generate, halt)
        actual = [p for p in ga]
        expected = [[3+i, 2+i, 1+i] for i in range(10)]
        self.assertEqual(actual, expected,
            "Actual: %r Expected: %r" % (actual, expected))
