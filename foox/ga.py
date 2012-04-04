"""
Contains code specific to the genetic algorithm.
"""

def genetic_algorithm(population, fitness, generate, halt):
    """
    A generator that yields a list of genomes ordered by fitness (descending).
    Each yielded list represents a generation in the execution of the genetic
    algorithm.

    @param population: the starting population of genomes.
    @param fitness: given a genome will return a fitness score.
    @param generate: encapsulates producing offspring genomes for the next
        generation.
    @param halt: tests if the genetic algorithm should stop.

    Applies the fitness function to each genome in a generation, uses the
    select function to choose genomes for crossover (offspring) and mutation.
    These become the next generation.

    If the halt function returns True for a generation then the algorithm stops.
    """
    current_population = sorted(population, key=fitness, reverse=True)
    generation_count = 1
    yield current_population
    while not halt(current_population, generation_count):
        generation_count += 1
        new_generation = [genome for genome in generate(current_population)]
        current_population = sorted(new_generation, key=fitness, reverse=True)
        yield current_population
