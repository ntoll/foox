"""
Contains code specific to the genetic algorithm.
"""
import random

def genetic_algorithm(population, fitness, generate, halt):
    """
    A generator that yields a list of genomes ordered by fitness (descending).
    Each yielded list represents a generation in the execution of the genetic
    algorithm.

    @param population: the starting population of genomes.
    @param fitness: a function which given a genome will return a fitness score.
    @param generate: an iterator that encapsulates producing offspring genomes
    for the next generation.
    @param halt: a function to test if the genetic algorithm should stop.

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

def rouletteWheelSelection(population):
    """
    A random number between 0 and the total fitness score of all the genomes in
    a population is chosen (a point with a slice of a roulette wheel). The code
    iterates through the genomes adding up the fitness scores. When the subtotal
    is greater than the randomly chosen point it returns the genome at that
    point "on the wheel".

    See: https://en.wikipedia.org/wiki/Fitness_proportionate_selection
    """
    total_fitness = 0.0
    for genome in population:
        total_fitness += genome.fitness

    random_point = random.uniform(0.0, total_fitness)

    fitness_tally = 0.0
    for genome in population:
        fitness_tally += genome.fitness
        if fitness_tally > random_point:
            return genome
