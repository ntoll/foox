"""
Contains code that takes a representation of a Genome and cantus firmus and
turns them into a .ly file so GNU Lilypond (http://lilypond.org/) can turn it
into printed sheet music and a midi file.

For duration, given counterpoint of species < 5, it is possible to work out the
number of notes and their durations from the number of notes in the cantus
firmus.
"""
import datetime
from string import Template

SPECIES_DURATION = {
    1: 1,
    2: 2,
    3: 4,
}

TEMPLATE = """
\\version "2.14.2"

\header {
    title = "$title"
    subtitle = "Created on: $created_on"
    composer = "$composer and Foox"
}

result = {
    <<
    \\new Staff
    {
        \\time 4/4
        \clef treble
        {
            $contrapunctus
        }
    }
    \\new Staff
    {
        \\time 4/4
        \clef treble
        {
            $cantus_firmus
        }
    }
    >>
}

\paper {
    raggedbottom = ##t
    indent = 7. \mm
    linewidth = 183.5 \mm
    betweensystemspace = 25\mm
    betweensystempadding = 0\mm
}

\score{
    \\result
    \midi {
        \context {
            \Score
            tempoWholesPerMinute = #(ly:make-moment 160 4)
        }
    }
    \layout {}
}
"""

# A dictionary that maps numbers to lilypond notes.
NOTES = {
    1: "g",
    2: "a",
    3: "b",
    4: "c'",
    5: "d'",
    6: "e'",
    7: "f'",
    8: "g'",
    9: "a'",
    10: "b'",
    11: "c''",
    12: "d''",
    13: "e''",
    14: "f''",
    15: "g''",
    16: "a''",
    17: "r",
}


def get_cantus_firmus(notes):
    """
    Given a list of notes as integers, will return the lilypond notes
    for the cantus firmus.
    """
    result = ''
    # Ensure the notes are in range
    normalised = [note for note in notes if note > 0 and note < 18]
    if not normalised:
        return result
    # Set the duration against the first note.
    result = NOTES[normalised[0]] + ' 1 '
    # Translate all the others.
    result += ' '.join([NOTES[note] for note in normalised[1:]])
    # End with a double bar.
    result += ' \\bar "|."'
    # Tidy up double spaces.
    result = result.replace('  ', ' ')
    return result


def get_simple_contrapunctus(notes, duration):
    """
    Given a list of notes as integers and the duration to use, will return the
    lilypond notes for the contrapunctus.

    Durations: 1-semibreve, 2-minim, 4-crotchet
    """
    result = ''
    # Ensure the notes are in range
    normalised = [note for note in notes if note > 0 and note < 18]
    if not normalised:
        return result
    # Set the duration against the first note.
    result = NOTES[normalised[0]] + ' %d ' % duration
    # Translate all the others except the final two.
    result += ' '.join([NOTES[note] for note in normalised[1:-2]])

    # Ensure the penultimate note is a semitone away IFF moving up to the final
    # note. (Kinda hacky - would be easier in Lisp)
    final_note = normalised.pop()
    penultimate_note = normalised.pop()
    next_note = NOTES[penultimate_note]
    if final_note == penultimate_note + 1:
        # Check if the note isn't a C or an F
        if final_note not in [4, 7, 11, 14]:
            # insert 'is' to sharpen the pitch of the note by a semitone.
            next_note = next_note[0] + 'is' + next_note[1:]
    result += ' ' + next_note

    # Ensure the final note is a semibreve.
    result += ' ' + NOTES[final_note]
    if duration != 1:
        result += ' 1'

    # Tidy up double spaces.
    result = result.replace('  ', ' ')
    return result


def get_fourth_species(notes):
    """
    Given a representation of the contrapunctus part of fourth species
    counterpoint in numeric (foox) form, turns it into correct Lilypond
    notation.
    """
    result = ''
    # Ensure the notes are in range
    normalised = [note for note in notes if note > 0 and note < 18]
    if not normalised:
        return result

    # Fourth species starts with two beats rest.
    result = 'r2 '

    # Translate all the others except the final two.
    body = [NOTES[note] for note in normalised[:-2]]
    for pitch in body:
        result += '%s~ %s ' % (pitch, pitch)

    # Ensure the penultimate note is a semitone away IFF moving up to the final
    # note. (Kinda hacky - would be easier in Lisp)
    final_note = normalised.pop()
    penultimate_note = normalised.pop()
    next_note = NOTES[penultimate_note]
    if final_note == penultimate_note + 1:
        # Check if the note isn't a C or an F
        if final_note not in [4, 7, 11, 14]:
            # insert 'is' to sharpen the pitch of the note by a semitone.
            next_note = next_note[0] + 'is' + next_note[1:]
    result += ' ' + next_note

    # Ensure the final note is a semibreve.
    result += ' %s 1' % (NOTES[final_note])

    # Tidy up double spaces.
    result = result.replace('  ', ' ')
    return result


def render(species, cantus_firmus, contrapunctus, title='Untitled',
    created_on=None, composer='Anonymous'):
    """
    Given an indication of the species (1-3), a list of notes for the
    cantus_firmus and contrapunctus returns a string containing lilypond code
    to render the musical information as PDF and MIDI files.
    """
    if not created_on:
        created_on = datetime.datetime.today()

    contrapunctus_notes = ''
    if species < 4:
        duration = SPECIES_DURATION[species]
        contrapunctus_notes = get_simple_contrapunctus(contrapunctus, duration)
    elif species == 4:
        contrapunctus_notes = get_fourth_species(contrapunctus)

    context = {}
    context['title'] = title
    context['created_on'] = created_on.strftime('%c')
    context['composer'] = composer
    context['contrapunctus'] = contrapunctus_notes
    context['cantus_firmus'] = get_cantus_firmus(cantus_firmus)
    # Sanity check...
    if context['contrapunctus'] and context['cantus_firmus']:
        score = Template(TEMPLATE)
        return score.substitute(context)
    else:
        return ''
