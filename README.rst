Foox
====

A fun brain break.

Creates species counterpoint with genetic algorithms (in Python). Produces
output for the music typesetter Lilypond (http://lilypond.org).

A presentation about this project given at the Europython 2012 conference can
be found in the presentation directory, just load the index.html file in a
browser.

See AUTHORS for contact information and LICENSE for the license (MIT).

To install type::

    $ python setup.py install

Once installed try::

    $ foox --help

for more information, or, to evolve some counterpoint try::

    $ foox -s 1 -cf 5 7 6 5 8 7 9 8 7 6 5 -o first_species
    $ lilypond first_species.ly

This will produce two files: first_species.pdf (the musical score) and
first_species.midi (a midi file to listen to with you media player). More
information can be gleaned from the presentation.

Feedback and questions most welcome.
