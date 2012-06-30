"""
Tests the common utility functions found in the utils module.
"""
import unittest

from foox.species.utils import (is_parallel, make_generate_function,
    is_stepwise_motion, is_suspension)
from foox.ga import Genome


# The cantus firmus to use in the test suite.
CANTUS_FIRMUS = [5, 7, 6, 5, 8, 7, 9, 8, 7, 6, 5]


class TestIsParallel(unittest.TestCase):
    """
    Ensures parallel motion is correctly identified.
    """

    def test_is_parallel_rising(self):
        """
        Detects rising parallel motion.
        """
        last = (1, 3)
        current = (2, 4)
        result = is_parallel(last, current)
        self.assertEqual(True, result)

    def test_is_parallel_falling(self):
        """
        Detects falling parallel motion.
        """
        last = (2, 4)
        current = (1, 3)
        result = is_parallel(last, current)
        self.assertEqual(True, result)

    def test_is_parallel_contrary(self):
        """
        Check the function doesn't mis-identify contrary motion.
        """
        last = (2, 4)
        current = (1, 5)
        result = is_parallel(last, current)
        self.assertEqual(False, result)

    def test_is_parallel_repeating(self):
        """
        Check the function doesn't mis-identify repeating notes (no motion).
        """
        last = (2, 4)
        current = (2, 4)
        result = is_parallel(last, current)
        self.assertEqual(False, result)


class TestIsStepwiseMotion(unittest.TestCase):
    """
    Ensures that a note is correctly identified as being part of some step-wise
    movement in a single direction.
    """

    def test_ascending(self):
        """
        Ascending stepwise movement.
        """
        melody = [5, 6, 7]
        position = 1
        self.assertTrue(is_stepwise_motion(melody, position))

    def test_descending(self):
        """
        Descending stepwise movement.
        """
        melody = [7, 6, 5]
        position = 1
        self.assertTrue(is_stepwise_motion(melody, position))

    def test_non_uniform_motion_down_up(self):
        """
        Stepwise motion but descending then ascending.
        """
        melody = [7, 6, 7]
        position = 1
        self.assertFalse(is_stepwise_motion(melody, position))

    def test_non_uniform_motion_up_down(self):
        """
        Stepwise motion but ascending then descending.
        """
        melody = [5, 6, 5]
        position = 1
        self.assertFalse(is_stepwise_motion(melody, position))

    def test_non_stepwise_motion_from(self):
        """
        Non-stepwise motion from preceeding note.
        """
        melody = [8, 6, 5]
        position = 1
        self.assertFalse(is_stepwise_motion(melody, position))

    def test_non_stepwise_motion_to(self):
        """
        Non-stepwise motion to the following note.
        """
        melody = [5, 6, 8]
        position = 1
        self.assertFalse(is_stepwise_motion(melody, position))


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
        result = make_generate_function(7, 0.2, CANTUS_FIRMUS)
        self.assertTrue(callable(result))

    def test_generate_function_returns_list(self):
        """
        Ensures the new population is a list.
        """
        generate_function = make_generate_function(7, 0.2, CANTUS_FIRMUS)
        g1 = Genome([1, 2, 3])
        g1.fitness = 1
        g2 = Genome([1, 2, 3])
        g2.fitness = 2
        seed_population = [g1, g2]
        result = generate_function(seed_population)
        self.assertTrue(list, type(result))

    def test_generate_function_returns_list_of_correct_length(self):
        """
        Ensure the new population is the correct length.
        """
        generate_function = make_generate_function(7, 0.2, CANTUS_FIRMUS)
        g1 = Genome([1, 2, 3])
        g1.fitness = 1
        g2 = Genome([1, 2, 3])
        g2.fitness = 2
        g3 = Genome([1, 2, 3])
        g3.fitness = 3
        seed_population = [g1, g2, g3]
        result = generate_function(seed_population)
        self.assertTrue(3, len(result))

class TestIsSuspension(unittest.TestCase):
    """
    Ensures that a note is correctly identified as being part of a valid
    suspension (dissonance resolving onto a consonance).
    """

    def test_four_three_suspension(self):
        """
        Test a 4/3 suspension is correction identified.
        """
        cantus_firmus = [7, 6, 5]
        melody = [9, 8, 7]
        position = 0
        self.assertTrue(is_suspension(melody, position, cantus_firmus))

    def test_seven_six_suspension(self):
        """
        Test a 7/6 suspension is correction identified.
        """
        cantus_firmus = [7, 6, 5]
        melody = [12, 11, 10]
        position = 0
        self.assertTrue(is_suspension(melody, position, cantus_firmus))

    def test_suspension_with_no_suspension(self):
        """
        If the note isn't part of a suspension the function should return
        false.
        """
        cantus_firmus = [7, 6, 5]
        melody = [11, 11, 10]
        position = 0
        self.assertFalse(is_suspension(melody, position, cantus_firmus))
