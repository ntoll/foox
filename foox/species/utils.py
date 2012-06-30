"""
Contains common utility functions required by all species of counterpoint.
"""
from foox import ga


def is_parallel(last, current):
    """
    Returns True if the motion between last and current notes is parallel.
    """
    parallel = False
    if last[0] - current[0] < 0 and last[1] - current[1] < 0:
        parallel = True
    elif last[0] - current[0] > 0 and last[1] - current[1] > 0:
        parallel = True
    return parallel


def is_stepwise_motion(melody, position):
    """
    Returns true if the note at position in the melody is in the middle of a
    step-wise movement in a single direction.
    """
    pre_note = melody[position-1]
    note = melody[position]
    post_note = melody[position+1]
    step_to = abs(pre_note - note)
    step_from = abs(note - post_note)
    if step_to == 1 and step_from == 1:
        return pre_note != post_note
    return False


def make_generate_function(mutation_range, mutation_rate, cantus_firmus):
    """
    Given the cantus firmus, mutation range and mutation rate will return a
    function that takes a seed generation and returns a new population.
    """

    def generate(seed_generation):
        """
        Given a seed generation will return a new generation of candidate
        solutions assuming the cantus_firmus and other settings in the closure.
        """
        length = len(seed_generation)
        # Keep the fittest 50%
        new_generation = seed_generation[:length/2]

        # Breed the remaining 50% using roulette wheel selection
        offspring = []
        while len(offspring) < length/2:
            mum = ga.roulette_wheel_selection(seed_generation)
            dad = ga.roulette_wheel_selection(seed_generation)
            children = mum.breed(dad)
            offspring.extend(children)

        # Mutate
        for genome in offspring:
            genome.mutate(mutation_range, mutation_rate, cantus_firmus)

        # Ensure the new generation is the right length
        new_generation.extend(offspring)
        new_generation = new_generation[:length]

        return new_generation

    return generate


def is_suspension(melody, position, cantus_firmus):
    """
    Returns true if the note in the melody at the specified position is part of
    a correctly formed suspension (dissonance resolving by step onto a
    consonance)
    """
    current_note = melody[position]
    resolution_note = melody[position + 1]
    cantus_firmus_note = cantus_firmus[position + 1]
    suspension_interval = current_note - cantus_firmus_note
    resolution_interval = resolution_note - cantus_firmus_note
    if suspension_interval == 3 and resolution_interval == 2:
        return True
    if suspension_interval == 6 and resolution_interval == 5:
        return True
    return False
