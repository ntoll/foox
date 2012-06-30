"""
Ensures that the lilypond module is producing expected output.
"""
import unittest
import datetime

from foox.lilypond import (get_cantus_firmus, get_simple_contrapunctus,
    get_fourth_species, render)


class TestLilypond(unittest.TestCase):
    """
    Ensures the foox.lilypond module works as expected.
    """

    def test_empty_get_cantus_firmus(self):
        """
        An empty list should produce an empty string.
        """
        result = get_cantus_firmus([])
        self.assertEqual('', result)

    def test_good_get_cantus_firmus(self):
        """
        The known good case.
        """
        raw = [5, 7, 6, 5, 8, 7, 9, 8, 7, 6, 5]
        result = get_cantus_firmus(raw)
        expected = "d' 1 f' e' d' g' f' a' g' f' e' d' \\bar \"|.\""
        self.assertEqual(expected, result)

    def test_get_cantus_firmus_range_too_low(self):
        """
        Notes less than 1 are ignored.
        """
        raw = [0, 1]
        result = get_cantus_firmus(raw)
        expected = "g 1 \\bar \"|.\""
        self.assertEqual(expected, result)

    def test_get_cantus_firmus_range_too_high(self):
        """
        Notes greater than 17 are ignored.
        """
        raw = [18, 1]
        result = get_cantus_firmus(raw)
        expected = "g 1 \\bar \"|.\""
        self.assertEqual(expected, result)

    def test_empty_get_simple_contrapunctus(self):
        """
        An empty list should return an empty string.
        """
        result = get_simple_contrapunctus([], 1)
        self.assertEqual('', result)

    def test_good_get_simple_contrapunctus(self):
        """
        The known good case.
        """
        raw = [5, 7, 6, 5, 8, 7, 9, 8, 7, 6, 5]
        result = get_simple_contrapunctus(raw, 4)
        expected = "d' 4 f' e' d' g' f' a' g' f' e' d' 1"
        self.assertEqual(expected, result)

    def test_get_simple_contrapunctus_rising_final_cadence(self):
        """
        Ensures that the final two notes are only a semitone apart if the
        melody is rising.
        """
        # check for if the diatonic notes are a tone apart
        raw = [5, 7, 6, 5, 8, 7, 9, 8, 7, 4, 5]
        result = get_simple_contrapunctus(raw, 4)
        expected = "d' 4 f' e' d' g' f' a' g' f' cis' d' 1"
        self.assertEqual(expected, result)

        # and again if the diatonic notes are only a semitone apart
        raw = [5, 7, 6, 5, 8, 7, 9, 8, 7, 6, 7]
        result = get_simple_contrapunctus(raw, 4)
        expected = "d' 4 f' e' d' g' f' a' g' f' e' f' 1"
        self.assertEqual(expected, result)

    def test_get_simple_contrapunctus_duration_set(self):
        """
        Ensures that the duration indication is correctly set.
        """
        raw = [5, 7, 6, 5, 8, 7, 9, 8, 7, 6, 5]
        result = get_simple_contrapunctus(raw, 4)
        expected = "d' 4 f' e' d' g' f' a' g' f' e' d' 1"
        self.assertEqual(expected, result)
        # do it again with a different duration
        result = get_simple_contrapunctus(raw, 2)
        expected = "d' 2 f' e' d' g' f' a' g' f' e' d' 1"
        self.assertEqual(expected, result)
        # do it again with a semibreve duration (so final not need not be set).
        result = get_simple_contrapunctus(raw, 1)
        expected = "d' 1 f' e' d' g' f' a' g' f' e' d'"
        self.assertEqual(expected, result)

    def test_empty_get_fourth_species(self):
        """
        An empty list should return an empty string.
        """
        result = get_fourth_species([])
        self.assertEqual('', result)

    def test_good_get_fourth_species(self):
        """
        The good case for fourth species counterpoint.
        """
        raw = [5, 12, 11, 10, 13, 12, 14, 13, 12, 11, 12]
        result = get_fourth_species(raw)
        expected = "r2 d'~ d' d''~ d'' c''~ c'' b'~ b' e''~ e'' d''~ d'' f''~ f'' e''~ e'' d''~ d'' cis'' d'' 1"
        self.assertEqual(expected, result)

    def test_get_fourth_species_rising_final_cadence(self):
        """
        Ensures that the final two notes are only a semitone apart if the
        melody is rising.
        """
        # check for if the diatonic notes are a tone apart
        raw = [5, 12, 11, 10, 13, 12, 14, 13, 12, 11, 12]
        result = get_fourth_species(raw)
        expected = "r2 d'~ d' d''~ d'' c''~ c'' b'~ b' e''~ e'' d''~ d'' f''~ f'' e''~ e'' d''~ d'' cis'' d'' 1"
        self.assertEqual(expected, result)

        # and again if the diatonic notes are only a semitone apart
        raw = [5, 12, 11, 10, 13, 12, 14, 13, 12, 6, 7]
        result = get_fourth_species(raw)
        expected = "r2 d'~ d' d''~ d'' c''~ c'' b'~ b' e''~ e'' d''~ d'' f''~ f'' e''~ e'' d''~ d'' e' f' 1"
        self.assertEqual(expected, result)

    def test_render_with_problems(self):
        """
        If render encounters problems with the passed in music it should just
        return an empty string (falsey).
        """
        result = render(1, [], [])
        self.assertEqual('', result)

    def test_render_with_default_args(self):
        """
        Checks the arguments appear as expected in the resulting lilypond code.
        """
        result = render(1, [5, 6, 5], [10, 11, 12])
        self.assertIn('Untitled', result)
        self.assertIn('Anonymous', result)
        self.assertIn("b' 1 cis'' d''", result)
        self.assertIn("d' 1 e' d' \\bar \"|.\"", result)

    def test_render_with_title(self):
        """
        Ensures the title is used in the lilypond code.
        """
        result = render(1, [5, 6, 5], [10, 11, 12], title='foo')
        self.assertIn('foo', result)

    def test_render_with_created_on(self):
        """
        Ensures the title is used in the lilypond code.
        """
        created_on = datetime.datetime.today()
        result = render(1, [5, 6, 5], [10, 11, 12], created_on=created_on)
        self.assertIn(created_on.strftime('%c'), result)

    def test_render_with_composer(self):
        """
        Ensures the title is used in the lilypond code.
        """
        result = render(1, [5, 6, 5], [10, 11, 12], composer='unittest')
        self.assertIn('unittest', result)
