"""
Tests for the silly word based example used to demonstrate the machinations of
genetic algorithms.
"""
import unittest
from foox.words import (Genome, create_population,
    make_fitness_function, make_generate_function, halt)


# Target word we're attempting to evolve.
TARGET_WORD = 'foo'


class TestCreatePopulation(unittest.TestCase):
    """
    Ensures the create_population function works as expected.
    """

    def test_returns_valid_genomes(self):
        """
        Checks the genomes returned by the create_population function are
        of the correct type.
        """
        result = create_population(1, TARGET_WORD)
        self.assertEqual(Genome, type(result[0]))

    def test_returns_correct_number_of_genomes(self):
        """
        Ensures the correct number of genomes are returned by the function.
        """
        result = create_population(100, TARGET_WORD)
        self.assertEqual(100, len(result))


class TestFitnessFunction(unittest.TestCase):
    """
    Ensures that the fitness function works as expected.
    """

    def test_make_fitness_function_returns_callable(self):
        """
        Ensures the make_fitness_function returns a callable.
        """
        result = make_fitness_function(TARGET_WORD)
        self.assertTrue(callable(result))

    def test_fitness_function_returns_float(self):
        """
        Makes sure the generated fitness function returns a fitness score as a
        float.
        """
        fitness_function = make_fitness_function(TARGET_WORD)
        genome = Genome(['c', 'a', 't'])
        result = fitness_function(genome)
        self.assertTrue(float, type(result))

    def test_fitness_function_sets_fitness_on_genome(self):
        """
        Ensures the fitness score is set in the genome's fitness attribute and
        is the same as the returned fitness score.
        """
        fitness_function = make_fitness_function(TARGET_WORD)
        genome = Genome(['c', 'a', 't'])
        self.assertEqual(None, genome.fitness)
        result = fitness_function(genome)
        self.assertNotEqual(None, genome.fitness)
        self.assertEqual(result, genome.fitness)

    def test_fitness_function_uses_cached_genome_fitness(self):
        """
        Ensures the fitness function bails if there is already a score set for
        the genome.
        """
        fitness_function = make_fitness_function(TARGET_WORD)
        genome = Genome(['c', 'a', 't'])
        genome.fitness = 12345
        result = fitness_function(genome)
        self.assertEqual(12345, result)


class TestGenerateFunction(unittest.TestCase):
    """
    Ensures that the generate function (used to generate new populations) works
    as expected.
    """

    def test_make_generate_function_returns_callable(self):
        """
        Ensures the make_generate_function returns a callable (the generate
        function to use in the GA).
        """
        result = make_generate_function(7, 0.2, TARGET_WORD)
        self.assertTrue(callable(result))

    def test_generate_function_returns_list(self):
        """
        Ensures the new population is a list.
        """
        generate_function = make_generate_function(7, 0.2, TARGET_WORD)
        g1 = Genome(['c', 'a', 't'])
        g1.fitness = 1
        g2 = Genome(['d', 'o', 'g'])
        g2.fitness = 2
        seed_population = [g1, g2]
        result = generate_function(seed_population)
        self.assertTrue(list, type(result))

    def test_generate_function_returns_list_of_correct_length(self):
        """
        Ensure the new population is the correct length.
        """
        generate_function = make_generate_function(7, 0.2, TARGET_WORD)
        g1 = Genome(['c', 'a', 't'])
        g1.fitness = 1
        g2 = Genome(['d', 'o', 'g'])
        g2.fitness = 2
        g3 = Genome(['f', 'o', 'o'])
        g3.fitness = 3
        seed_population = [g1, g2, g3]
        result = generate_function(seed_population)
        self.assertTrue(3, len(result))


class TestHalt(unittest.TestCase):
    """
    Ensure the halting function works as expected.
    """

    def test_halt_expected(self):
        """
        Ensure the function returns true if we're in a halting state.
        """
        g1 = Genome(['c', 'a', 't'])
        g1.fitness = len(TARGET_WORD)
        g2 = Genome(['d', 'o', 'g'])
        g2.fitness = 2
        g3 = Genome(['f', 'o', 'o'])
        g3.fitness = 3
        # Any fittest solution with fitness = length of the target word.
        population = [g1, g2, g3]
        result = halt(population, 1)
        self.assertTrue(result)

    def test_halt_not(self):
        """
        Ensures if the fittest genome has fitness < 4 then halt doesn't
        succeed.
        """
        g1 = Genome(['c', 'a', 't'])
        g1.fitness = len(TARGET_WORD) - 1
        g2 = Genome(['d', 'o', 'g'])
        g2.fitness = 2
        g3 = Genome(['f', 'o', 'o'])
        g3.fitness = 3
        # Any fittest solution with fitness < target word length means call a
        # halt.
        population = [g1, g2, g3]
        result = halt(population, 1)
        self.assertFalse(result)


class TestGenome(unittest.TestCase):
    """
    Ensures that the Genome class is overridden as expected.
    """

    def test_mutate_is_implemented(self):
        """
        Ensures that we have a mutate method implemented.
        """
        genome = Genome(['c', 'a', 't'])
        self.assertNotEqual(NotImplemented, genome.mutate(2, 0.2,
            ['d', 'o', 'g']))
