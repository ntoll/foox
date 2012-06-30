#!/usr/bin/env python
"""
A simple command line wrapper around the genetic algorithm used for finding
valid solutions to species counterpoint problems.
"""

import argparse
import logging

from foox import ga, version, lilypond, words
from foox.species import first, second, third, fourth


parser = argparse.ArgumentParser(
    description='Evolves valid solutions to species counterpoint problems.')
parser.add_argument('--version', action='version',
    version=version.get_version())
parser.add_argument('-v', '--verbose', help='increased amount of verbosity',
    action='store_true')
parser.add_argument('-s', '--species', help='indicated species to use (1-5)',
    required=True, type=int)
parser.add_argument('-cf', '--cantus-firmus', help='specify the cantus firmus',
    nargs='*', required=True)
parser.add_argument('-o', '--out', help='name the output file')


if __name__ == '__main__':
    args = parser.parse_args()
    cf = [int(x) for x in args.cantus_firmus]
    species = args.species
    output = 'out'
    if args.out:
        output = args.out

    population_size = 1000
    mutation_range = 7
    mutation_rate = 0.4
    if species == 1:
        population_size = first.DEFAULT_POPULATION_SIZE
        mutation_range = first.DEFAULT_MUTATION_RANGE
        mutation_rate = first.DEFAULT_MUTATION_RATE
        start_population = first.create_population(population_size, cf)
        fitness_function = first.make_fitness_function(cf)
        generate_function = first.make_generate_function(mutation_range,
            mutation_rate, cf)
        halt_function = first.halt
    elif species == 2:
        population_size = second.DEFAULT_POPULATION_SIZE
        mutation_range = second.DEFAULT_MUTATION_RANGE
        mutation_rate = second.DEFAULT_MUTATION_RATE
        start_population = second.create_population(population_size, cf)
        fitness_function = second.make_fitness_function(cf)
        generate_function = first.make_generate_function(mutation_range,
            mutation_rate, cf)
        halt_function = second.make_halt_function(cf)
    elif species == 3:
        population_size = third.DEFAULT_POPULATION_SIZE
        mutation_range = third.DEFAULT_MUTATION_RANGE
        mutation_rate = third.DEFAULT_MUTATION_RATE
        start_population = third.create_population(population_size, cf)
        fitness_function = third.make_fitness_function(cf)
        generate_function = third.make_generate_function(mutation_range,
            mutation_rate, cf)
        halt_function = third.make_halt_function(cf)
    elif species == 4:
        population_size = fourth.DEFAULT_POPULATION_SIZE
        mutation_range = fourth.DEFAULT_MUTATION_RANGE
        mutation_rate = fourth.DEFAULT_MUTATION_RATE
        start_population = fourth.create_population(population_size, cf)
        fitness_function = fourth.make_fitness_function(cf)
        generate_function = fourth.make_generate_function(mutation_range,
            mutation_rate, cf)
        halt_function = fourth.make_halt_function(cf)

    ga = ga.genetic_algorithm(start_population, fitness_function,
        generate_function, halt_function)
    fitness = 0.0

    counter = 0
    for generation in ga:
        counter += 1
        fitness = generation[0].fitness
        print "--- Generation %d ---" % counter
        print generation[0]
        print fitness
    with open('%s.ly' % output, 'w') as output:
        output.write(lilypond.render(species, cf, generation[0].chromosome))
