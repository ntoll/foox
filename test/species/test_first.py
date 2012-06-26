"""
Tests for the module that encompasses first species counterpoint.
"""
import unittest
from foox.species.first import (Genome, create_population, is_parallel,
    make_fitness_function, make_generate_function, halt, MAX_REWARD)


# The cantus firmus to use in the test suite.
CANTUS_FIRMUS = [5, 7, 6, 5, 8, 7, 9, 8, 7, 6, 5]


class TestCreatePopulation(unittest.TestCase):
    """
    Ensures the create_population function works as expected.
    """

    def test_returns_valid_genomes(self):
        """
        Checks the genomes returned by the create_population function are
        of the correct type.
        """
        result = create_population(1, CANTUS_FIRMUS)
        self.assertEqual(Genome, type(result[0]))

    def test_returns_correct_number_of_genomes(self):
        """
        Ensures the correct number of genomes are returned by the function.
        """
        result = create_population(100, CANTUS_FIRMUS)
        self.assertEqual(100, len(result))

    def test_uses_only_valid_intervals(self):
        """
        Tests that only valid consonant intervals are used.
        """
        valid_intervals = [2, 4, 5, 7, 9, 11]
        result = create_population(20, CANTUS_FIRMUS)
        for genome in result:
            for i in range(len(genome.chromosome)):
                contrapunctus_note = genome.chromosome[i]
                cantus_firmus_note = CANTUS_FIRMUS[i]
                interval = contrapunctus_note - cantus_firmus_note
                self.assertIn(interval, valid_intervals)


class TestFitnessFunction(unittest.TestCase):
    """
    Ensures that the fitness function works as expected.
    """

    def test_make_fitness_function_returns_callable(self):
        """
        Ensures the make_fitness_function returns a callable.
        """
        result = make_fitness_function(CANTUS_FIRMUS)
        self.assertTrue(callable(result))

    def test_fitness_function_returns_float(self):
        """
        Makes sure the generated fitness function returns a fitness score as a
        float.
        """
        fitness_function = make_fitness_function(CANTUS_FIRMUS)
        genome = Genome([1, 2, 3])
        result = fitness_function(genome)
        self.assertTrue(float, type(result))

    def test_fitness_function_sets_fitness_on_genome(self):
        """
        Ensures the fitness score is set in the genome's fitness attribute and
        is the same as the returned fitness score.
        """
        fitness_function = make_fitness_function(CANTUS_FIRMUS)
        genome = Genome([1, 2, 3])
        self.assertEqual(None, genome.fitness)
        result = fitness_function(genome)
        self.assertNotEqual(None, genome.fitness)
        self.assertEqual(result, genome.fitness)

    def test_fitness_function_uses_cached_genome_fitness(self):
        """
        Ensures the fitness function bails if there is already a score set for
        the genome.
        """
        fitness_function = make_fitness_function(CANTUS_FIRMUS)
        genome = Genome([1, 2, 3])
        genome.fitness = 12345
        result = fitness_function(genome)
        self.assertEqual(12345, result)


class TestHalt(unittest.TestCase):
    """
    Ensure the halting function works as expected.
    """

    def test_halt_expected(self):
        """
        Ensure the function returns true if we're in a halting state.
        """
        g1 = Genome([1, 2, 3])
        g1.fitness = MAX_REWARD
        g2 = Genome([1, 2, 3])
        g2.fitness = 3
        g3 = Genome([1, 2, 3])
        g3.fitness = 2
        # Any fittest solution with fitness >= MAX_REWARD means call a halt.
        population = [g1, g2, g3]
        result = halt(population, 1)
        self.assertTrue(result)

    def test_halt_not(self):
        """
        Ensures if the fittest genome has fitness < 4 then halt doesn't
        succeed.
        """
        g1 = Genome([1, 2, 3])
        g1.fitness = MAX_REWARD - 0.1
        g2 = Genome([1, 2, 3])
        g2.fitness = 3
        g3 = Genome([1, 2, 3])
        g3.fitness = 2
        # Any fittest solution with fitness >= 4 means call a halt.
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
        genome = Genome([1, 2, 3])
        self.assertNotEqual(NotImplemented, genome.mutate(2, 0.2, [1, 2, 3]))

    def test_mutate_bounded_by_arg_values(self):
        """
        A rather contrived test but it proves that both the mutation_range and
        mutation_rate are used correctly given the context given by a cantus
        firmus.
        """
        cantus_firmus = [1, 1, 1, 1, 1]
        mutation_rate = 1 # mutate every time.
        mutation_range = 2 # will always mutate to thirds above the cf note.
        genome = Genome([5, 6, 7, 8, 9])
        genome.mutate(mutation_range, mutation_rate, cantus_firmus)
        self.assertEqual([3, 3, 3, 3, 3], genome.chromosome)
