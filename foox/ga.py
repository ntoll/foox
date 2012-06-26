"""
Contains code specific to the genetic algorithm.
"""
import random


def genetic_algorithm(population, fitness, generate, halt, reverse=True):
    """
    A generator that yields a list of genomes ordered by fitness (descending).
    Each yielded list represents a generation in the execution of the genetic
    algorithm.

    @param population: the starting population of genomes.
    @param fitness: a function which given a genome will return a fitness
    score.
    @param generate: an function that produces offspring genomes for the next
    generation.
    @param halt: a function to test if the genetic algorithm should stop.
    @reverse: a flag to indicate if fittest = highest score (True) or lowest
    (False)

    Applies the fitness function to each genome in a generation, uses the
    generate function create the next generation from the existing one.

    If the halt function returns True for a generation then the algorithm
    stops.
    """
    current_population = sorted(population, key=fitness, reverse=reverse)
    generation_count = 1
    yield current_population
    while not halt(current_population, generation_count):
        generation_count += 1
        new_generation = generate(current_population)
        current_population = sorted(new_generation, key=fitness, reverse=True)
        yield current_population


def roulette_wheel_selection(population):
    """
    A random number between 0 and the total fitness score of all the genomes in
    a population is chosen (a point with a slice of a roulette wheel). The code
    iterates through the genomes adding up the fitness scores. When the
    subtotal is greater than the randomly chosen point it returns the genome
    at that point "on the wheel".

    See: https://en.wikipedia.org/wiki/Fitness_proportionate_selection
    """
    total_fitness = 0.0
    for genome in population:
        total_fitness += genome.fitness

    # Ensures random selection if no solutions are "fit".
    if total_fitness == 0.0:
        return random.choice(population)

    random_point = random.uniform(0.0, total_fitness)

    fitness_tally = 0.0
    for genome in population:
        fitness_tally += genome.fitness
        if fitness_tally > random_point:
            return genome


def crossover(mum, dad, klass):
    """
    Given two parent genomes and a Genome class, randomly selects a midpoint
    and then swaps the ends of each genome's chromosome to create two new
    genomes that are returned in a tuple.
    """
    # Check if the parents are the same,
    if mum == dad:
        # and do nothing if they are.
        return (mum, dad)

    crossover_point = random.randint(0, len(mum))

    baby1 = klass(mum[:crossover_point] + dad[crossover_point:])
    baby2 = klass(dad[:crossover_point] + mum[crossover_point:])

    return (baby1, baby2)


class Genome(object):
    """
    A base class that all Genome's must use. Genomes represent candidate
    solutions in the genetic algorithm.
    """

    def __init__(self, chromosome):
        """
        The chromosome is a list of genes that encode specific characteristics
        of the candidate solution (genome). The different settings that a gene
        may possess are called alleles, and their location in the chromosome is
        called the locus. The state of the alleles in a particular chromosome
        is called the genotype. It is the genotype that provides information
        about the state of the actual candidate solution. The candidate
        solution itself is called a genome (hence the name of this class).
        """
        self.chromosome = chromosome
        # Denotes unknown. Set by the fitness function.
        self.fitness = None

    def breed(self, other):
        """
        Returns two new offspring bred from this and another instance. Uses the
        crossover function.
        """
        return crossover(self, other, self.__class__)

    def mutate(self, mutation_range, mutation_rate, context):
        """
        Mutates the genotypes no more than the mutation_range depending on the
        mutation_rate given a certain context (to ensure the mutation is
        valid).

        To be overridden as per requirements in the child classes.
        """
        return NotImplemented

    def __eq__(self, other):
        """
        Genomes are judged to be equal if they have the same genotype.
        """
        return self.chromosome == other.chromosome

    def __len__(self):
        """
        Returns the length of the chromosome for ease of use.
        """
        return len(self.chromosome)

    def __getitem__(self, key):
        """
        To allow slicing and getting a value for a specific allele.
        """
        return self.chromosome.__getitem__(key)

    def __repr__(self):
        """
        Return something meaningful (the chromosome's repr for example).
        """
        return self.chromosome.__repr__()
