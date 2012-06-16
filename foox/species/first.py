"""
This module encapsulates the behaviour of first species counterpoint.
"""
import random

import foox.ga as ga


VALID_INTERVALS = [2, 4, 5, 7, 9, 11]


def create_population(size, cantus_firmus):
    """
    Will create a new list of random candidate solutions of the specified size.
    """
    result = []
    for i in range(size):
        new_chromosome = []
        for note in cantus_firmus:
            interval = random.choice(VALID_INTERVALS)
            new_chromosome.append(note+interval)
        genome = Genome(new_chromosome)
        result.append(genome)
    return result


def is_parallel(last, current):
    """
    Returns True if the motion between last and current is parallel.
    """
    parallel = False
    if last[0] - current[0] < 0 and last[1] - current[1] < 0:
        parallel = True
    elif last[0] - current[0] > 0 and last[1] - current[1] > 0:
        parallel = True
    return parallel


def make_fitness_function(cantus_firmus):
    """
    Given the cantus firmus, will use it in a closure and return a function
    that takes a single Genome instance and returns a fitness score.
    """

    def fitness_function(genome):
        """
        Given a candidate solution will return a fitness score assuming
        the cantus_firmus in this closure. Caches the fitness score in the
        genome.
        """
        """
        if genome.fitness != None:
            return genome.fitness
        """

        # The fitness score to be returned.
        fitness_score = 0.0
        # Counts the number of repeated notes in the contrapunctus.
        repeats = 0
        # Counts consecutive parallel thirds.
        thirds = 0
        # Counts consecutive parallel sixths.
        sixths = 0
        # Counts the amount of parallel motion.
        parallel_motion = 0

        contrapunctus = genome.chromosome

        # Make sure the solution starts correctly (at a 5th or octave).
        first_interval = contrapunctus[0] - cantus_firmus[0]
        if first_interval == 7 or first_interval == 4:
            fitness_score += 1
        else:
            fitness_score -= 0.1

        # Make sure the solution finishes correctly (at an octave).
        if contrapunctus[-1] - cantus_firmus[-1] == 7:
            fitness_score += 1
        else:
            fitness_score -= 0.1

        # Reward contrary motion onto the final note.
        cantus_firmus_motion = cantus_firmus[-1] - cantus_firmus[-2]
        contrapunctus_motion = contrapunctus[-1] - contrapunctus[-2]

        if ((cantus_firmus_motion < 0 and contrapunctus_motion > 0) or
            (cantus_firmus_motion > 0 and contrapunctus_motion < 0)):
            fitness_score += 1
        else:
            fitness_score -= 0.1

        # Make sure the penultimate note isn't a repeated note.
        penultimate_preparation = abs(contrapunctus[-2] - contrapunctus[-3])
        if penultimate_preparation == 0:
            fitness_score -= 0.1
        else:
            # Make sure the movement to the penultimate note isn't from too
            # far away (not greater than a fifth).
            if penultimate_preparation < 5:
                fitness_score += 1
            else:
                fitness_score -= 0.1

        # Check the fitness of the body of the solution.
        solution = zip(contrapunctus, cantus_firmus)
        last_notes = solution.pop()
        last_interval = last_notes[0] - last_notes[1]
        for contrapunctus_note, cantus_firmus_note in solution:
            current_notes = (contrapunctus_note, cantus_firmus_note)
            current_interval = contrapunctus_note - cantus_firmus_note

            # Punish parallel fifths or octaves.
            if ((current_interval == 4 or current_interval == 7) and
                (last_interval == 4 or last_interval == 7)):
                fitness_score -= 0.1

            # Check if the melody is a repeating note.
            if contrapunctus_note == last_notes[0]:
                repeats += 1

            # Check for parallel thirds.
            if current_interval == 2 and last_interval == 2:
                thirds += 1

            # Check for parallel sixths.
            if current_interval == 4 and last_interval == 4:
                sixths += 1

            # Check for parallel motion.
            if is_parallel(last_notes, current_notes):
                parallel_motion += 1

            last_notes = current_notes
            last_interval = current_interval

        # Melody wide attributes to be punished.
        one_third = len(contrapunctus) % 0.33

        # Punish too many (> 1/3) repeated notes.
        if repeats > one_third:
            fitness_score -= 0.1

        # Punish too many (> 1/3) parallel thirds
        if thirds > one_third:
            fitness_score -= 0.1

        # Punish too many (> 1/3) parallel sixths.
        if sixths > one_third:
            fitness_score -= 0.1

        # Punish too many (> 1/3) parallel movements.
        if parallel_motion > one_third:
            fitness_score -= 0.1

        genome.fitness = fitness_score

        return fitness_score

    return fitness_function


def make_generate_function(mutation_range, mutation_rate, cantus_firmus):
    """
    Given the cantus firmus, mutation range and mutation rate will use them in
    a closure and return a function that takes a seed generation and returns a
    new population.
    """

    def generate(seed_generation):
        """
        Given a seed generation will return a new generation of candidate
        solutions assuming the cantus_firmus in the closure.
        """
        length = len(seed_generation)
        # Keep the fittest 50%
        new_generation = seed_generation[:length/2]

        # Breed the remaining 50% using roulette wheel selection
        while len(new_generation) < length:
            mum = ga.roulette_wheel_selection(seed_generation)
            dad = ga.roulette_wheel_selection(seed_generation)
            children = mum.breed(dad)
            new_generation.extend(children)
        # Ensure the new generation is the right length
        new_generation = new_generation[:length]

        # Mutate
        for genome in new_generation:
            genome.mutate(mutation_range, mutation_rate, cantus_firmus)

        return new_generation

    return generate


def halt(population, generation_count):
    """
    Given a population of candidate solutions and generation count (the number
    of epochs the algorithm has run) will return a boolean to indicate if an
    acceptable solution has been found within the referenced population.
    """
    # All four required fingerprints exist in a solution that has not been
    # punished by for over-use of thirds, sixths, parallel motion etc.
    return population[0].fitness >= 4 or generation_count > 100


class Genome(ga.Genome):
    """
    A class to represent a candidate solution for first species counterpoint.
    """

    def mutate(self, mutation_rate, mutation_range, context):
        """
        Mutates the genotypes no more than the mutation_range depending on the
        mutation_rate given the cantus_firmus passed in as the context (to
        ensure the mutation is valid).
        """
        valid_mutation_intervals = [interval for interval in VALID_INTERVALS
            if interval <= mutation_range]
        for locus in range(len(self.chromosome)):
            cantus_firmus_note = context[locus]
            if mutation_rate >= random.random():
                mutation = random.choice(valid_mutation_intervals)
                new_allele = cantus_firmus_note + mutation
                self.chromosome[locus] = new_allele
