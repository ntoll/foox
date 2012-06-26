"""
This module encapsulates the behaviour of evolving words.
"""
import random
import string

import foox.ga as ga


# Valid values for letters in a word.
LETTERS = string.ascii_lowercase


def create_population(number, word):
    """
    Will create a new list of random candidate solutions of the specified
    number given the candidate word that is the evolutionary target.
    """
    result = []
    word_length = len(word)
    for i in range(number):
        new_chromosome = []
        for j in range(word_length):
            letter = random.choice(LETTERS)
            new_chromosome.append(letter)
        genome = Genome(new_chromosome)
        result.append(genome)
    return result


def levenshtein(s1, s2):
    """
    Calculates the Levenshtein distance between two strings. Based upon the
    function found here:

    http://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
    """
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if not s1:
        return len(s2)
    previous_row = xrange(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # j+1 instead of j since previous_row and current_row are one
            # character longer than s2
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]


def make_fitness_function(word):
    """
    Given the target word, will return a function that takes a single Genome
    instance and returns a fitness score (based upon its Levenshtein distance).
    """

    word_len = len(word)

    def fitness_function(genome):
        """
        Returns the fitness score of the genome.
        """
        if genome.fitness:
            return genome.fitness

        genome.fitness = abs(word_len -
            levenshtein(word, ''.join(genome.chromosome)))
        return genome.fitness

    return fitness_function


def make_generate_function(mutation_range, mutation_rate, word):
    """
    Given a target word, mutation range and mutation rate will use return a
    function that takes a seed generation and returns a new generation.
    """

    def generate(seed_generation):
        """
        Given a seed generation will return a new generation of candidates.
        """
        length = len(seed_generation)
        # Keep the fittest 50%
        new_generation = seed_generation[:length / 2]

        # Breed the remaining 50% using roulette wheel selection
        offspring = []
        while len(offspring) < length / 2:
            mum = ga.roulette_wheel_selection(seed_generation)
            dad = ga.roulette_wheel_selection(seed_generation)
            children = mum.breed(dad)
            offspring.extend(children)

        # Mutate
        for genome in offspring:
            genome.mutate(mutation_range, mutation_rate, word)

        # Ensure the new generation is the right length
        new_generation.extend(offspring)
        new_generation = new_generation[:length]

        return new_generation

    return generate


def halt(population, generation_count):
    """
    Given a population of candidate solutions and generation count (the number
    of epochs the algorithm has run) will return a boolean to indicate if an
    acceptable solution has been found within the referenced population.
    """
    word_length = len(population[0].chromosome)
    return population[0].fitness == word_length or generation_count > 100


class Genome(ga.Genome):
    """
    A class to represent a candidate solution for a target word.
    """

    def mutate(self, mutation_rate, mutation_range, context):
        """
        Mutates the genotypes. Only the mutation_rate is used in this simple
        example.
        """
        for locus in range(len(self.chromosome)):
            if mutation_rate >= random.random():
                # Verbose, but correctly named for clarity.
                new_allele = random.choice(LETTERS)
                self.chromosome[locus] = new_allele
                # force recalculation of fitness
                self.fitness = None
