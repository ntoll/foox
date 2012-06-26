"""
Tests for the ga (genetic algorithm) module
"""
import unittest
import random
from mock import MagicMock, patch
from foox.ga import (genetic_algorithm, roulette_wheel_selection, crossover,
    Genome)


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
        Ensures the fitness function is called on each initial genome before
        yielding the starting population.
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
        Ensures that the halt function is called for all subsequent yields
        after yielding the starting population.
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
        expected = [[3 + i, 2 + i, 1 + i] for i in range(10)]
        self.assertEqual(actual, expected,
            "Actual: %r Expected: %r" % (actual, expected))


class TestRouletteWheelSelection(unittest.TestCase):
    """
    As much as is possible, ensures the roulette wheel selection function works
    in the expected fashion.
    """

    def setUp(self):
        # To make the results repeatable and predictable.
        random.seed(1)

    def test_returns_genome(self):
        """
        Ensures that the roulette wheel returns a selected genome.
        """

        class Genome(object):
            """
            A simple representation of a genome.
            """

            def __init__(self, fitness):
                self.fitness = fitness

        population = [Genome(random.uniform(0.1, 10.0)) for i in range(4)]
        result = roulette_wheel_selection(population)
        self.assertIsInstance(result, Genome,
            "Expected result of roulette_wheel_selection is not a Genome")

    def test_returns_genome_with_unfit_population(self):
        """
        Ensures that the roulette wheel returns a randomly selected genome if
        none of them have a positive fitness score.
        """

        class Genome(object):
            """
            A simple representation of a genome.
            """

            def __init__(self, fitness):
                self.fitness = fitness

        population = [Genome(0.0) for i in range(4)]
        result = roulette_wheel_selection(population)
        self.assertIsInstance(result, Genome,
            "Expected result of roulette_wheel_selection is not a Genome")


class TestCrossover(unittest.TestCase):
    """
    Ensures the crossover function used to "breed" two new offspring from two
    given parents works as expected.
    """

    def setUp(self):
        # To make the results repeatable and predictable.
        random.seed(9)

    def test_return_parents_if_same(self):
        """
        If both parents have the same chromosome then just return the parents.
        """
        mum = Genome([1, 2, 3])
        dad = Genome([1, 2, 3])
        result = crossover(mum, dad, Genome)
        self.assertEqual(mum, result[0],
            "Child expected to be the same as parent.")
        self.assertEqual(mum, result[0],
            "Child expected to be the same as parent.")

    def test_creates_two_babies(self):
        """
        If the parents are different ensures that the children are the result
        of an expected crossover.
        """
        mum = Genome([1, 2, 3, 4])
        dad = Genome(['a', 'b', 'c', 'd'])
        result = crossover(mum, dad, Genome)
        # There must be two children.
        self.assertEqual(2, len(result))
        # The randint call in crossover will choose 2 given random.seed(5).
        expected1 = Genome([1, 2, 'c', 'd'])
        expected2 = Genome(['a', 'b', 3, 4])
        self.assertEqual(expected1, result[0],
            "Expected: %r Got: %r" % (expected1, result[0]))
        self.assertEqual(expected2, result[1],
            "Expected: %r Got: %r" % (expected2, result[1]))


class TestGenome(unittest.TestCase):
    """
    Ensures the base Genome class behaves as expected.
    """

    def setUp(self):
        # To make the results repeatable and predictable.
        random.seed(9)

    def test_init(self):
        """
        Ensures the chromosome and fitness are initialised correctly.
        """
        x = Genome([1, 2, 3])
        self.assertEqual(None, x.fitness)
        self.assertEqual([1, 2, 3], x.chromosome)

    def test_breed(self):
        """
        Ensures that the crossover function is called as a result of calling
        the breed method.
        """
        x = Genome([1, 2, 3, 4])
        mate = Genome(['a', 'b', 'c', 'd'])
        mock_crossover = MagicMock(return_value=(Genome([1, 2, 'a', 'b']),
            Genome(['a', 'b', 3, 4])))

        with patch('foox.ga.crossover', mock_crossover):
            x.breed(mate)
        self.assertEqual(1, mock_crossover.call_count,
            "Breed does not call crossover function expected number of times.")
        mock_crossover.assert_called_with(x, mate, Genome)

    def test_mutate(self):
        """
        Ensurs the mutate method returns NotImplemented.
        """
        x = Genome([1, 2, 3])
        self.assertEqual(NotImplemented, x.mutate(1, 2, [1, 2, 3]))

    def test_eq(self):
        """
        Ensures that only the chromosome is used for equality.
        """
        x = Genome([1, 2, 3])
        y = Genome([1, 2, 3])
        z = Genome([3, 2, 1])
        self.assertEqual(x, y)
        self.assertNotEqual(x, z)

    def test_len(self):
        """
        The __len__ function returns the length of the chromosome.
        """
        x = Genome([1, 2, 3])
        self.assertEqual(3, len(x))

    def test_getitem(self):
        """
        The __getitem__ function returns the corresponding result from the
        chromosome.
        """
        x = Genome([1, 2, 3])
        self.assertEqual(1, x[0])
        self.assertEqual(2, x[1])
        self.assertEqual(3, x[2])

    def test_repr(self):
        """
        The __repr__ of the Genome is that of the chromosome.
        """
        x = Genome([1, 2, 3])
        self.assertEqual(repr([1, 2, 3]), repr(x))
