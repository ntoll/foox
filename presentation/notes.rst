FOOX - Music Theory, Genetic Algorithms and Python
==================================================

This talk describes a "fun" brain-break project I've been working on in my
own time. It encompasses three things I love:

* Music
* Programming
* Learning new stuff

Put simply, I've written a program that will solve musical problems used to
train composers. I'll start by describing some high level music theory (just
enough so you are able to understand the nature of the problem) followed by
an exploration of genetic algorithms (the technique I used to solve the
problems) and finish by comparing computer generated output with solutions
from the composers Johan Joseph Fux and Wolfgang Amadeus Mozart.

The only assumption I'm making is that you're familiar with Python. However, it
would be helpful to me if I could find out how "musical" you guys think you are.

Hands up if you're:

* Tone deaf, can't tell the difference between a lawn mower and saxophone.
* Someone who enjoys listening to music but doesn't know anything about what you're listening to.
* Someone with some sort of basic musical training - perhaps piano lessons when you were a kid.
* A serious amateur musician who knows music.
* The result of an extensive musical education perhaps culminating with time spent at a world class conservatoire such as the Royal College of Music.

----

First, let's explore the musical aspects of the problem. Here are two
contrasting melodies (tunes) that I've composed.

----

How are these melodies "contrasting"? What are the terms of reference for
making such a claim? One obvious way they contrast is in their "shape". Look
at how different the two lines are.

----

This is better illustrated if the notes are removed and the shape (contour)
remains. Notice how the top melody is jagged, starts low down and ends high
up. In contrast the bottom melody is rather flat with a bump in the middle
and ends in much the same place as it started.

----

One useful way to think of this contrast is that the top melody is jagged like
this picture of the French Alps whereas the bottom melody is undulating like
Shropshire's Long Mynd Hills.

----

Another way the two melodies contrast is in the number of notes they contain.

----

Once again, removing the notes makes this difference clear.

----

Just like the density of these two photographs of birds on telephone wires.

----

So given these two different melodies, what happens when we play them
together? In some way these very different melodies are related to each other
in such a way that they mysteriously work when played together. This is
called "counterpoint".

----

I want you to get a flavour of the intricacies of counterpoint so I'm going to
play the music two more times. On this occasion I want you to pick a part (it
doesn't matter which) and try to follow it while also attempting to listen to
the piece as a whole. Concentrate on the contour of the melody. Try to get a
feel of where it moves (higher or lower) and how it moves (by step or by jump).

----

Now, listen again but concentrate on the other melody while still attempting to
listen to the piece as a whole. Concentrate on the density of the melody while
trying to be aware of what the other melody is doing.

I'm trying to get you used to the different ways to listen to counterpoint so
you know what to listen out for with the computer generated examples I'll play
later.

----

This Escher print is a visual analogy that may also help you understand the
concept further.

----

Not only is counterpoint interesting because two (or more) contrasting melodies
are played together, but it's ingenious because composers will play around
with the melodies so that they are combined and re-combined in unexpected,
clever and interesting ways.

Perhaps the most talented composer of this sort of contrapuntal trickery is
J.S.Bach and these portraits of him help illustrate the most common
transformations composers use.

The original melody is represented by the portrait on the left.

Inversion means turning the melody upside down. When the original may go up
two steps, its inversion will go down two steps.

Retrograde is simply playing the melody backwards.

Retrograde inversion is a combination of the above two techniques to create a
mirror image of the melody.

----

Voicing concerns "where" each melody is played. For example, one melody may
first be heard on a high instrument at the start of the piece but ends up as
the bass line elsewhere.

Whereas all the previous transformations concern pitch, the following two
affect time:

Augmentation is uniformly extending the duration of the notes in a melody (for
example, doubling them). Diminution is the opposite, squeezing the duration of
the notes in a uniform way.

----

Here's a test: can you work out the transformations I use in the second half
of this example.

Retrograde, inversion and voicing.

----

Here's the mystery, how do composers know that two seemingly unrelated
melodies will fit together in these interesting ways? This use to fascinate me
when I was a teenager and I often used to wish there was a book the
explained it all.

----

I wanted a "Counterpoint for Dummies".

----

Actually, 300 years ago, someone had the same idea.

----

Its author, Johan Joseph Fux is an interesting character. At a time when
your position in life was determined by who your parents were Fux was a rare
exception. Nothing is known of his early years because he was the son of
peasants. However, his talent obviously shone because he ended up being the
court composer for three holy Roman emperors. At the time this was one of the
top musical jobs in Europe.

----

Gradus ad Parnassum is a set of dialogues between "Josephus" (Fux himself, as
student) and "Aloysius" (the master, said to be an idolisation of the great
Italian master, Palestrina).

They concern how two, three and four part counterpoint works by introducing
sets of rules, of increasing complexity in groups called "species". This method
is therefore called "species counterpoint".

Once the rules have been discussed the student is given a melody, called the
cantus firmus, over which they are supposed to write a new melody using the
rules of a certain species of counterpoint for however many voices.

In our case we're only interested in two part counterpoint.

Once the student demonstrates mastery of the species they "level up" and
proceed to the next species.

First species contains few but very specific rules whereas the fifth species
allows the student to compose counterpoint much like the "free" counterpoint
I played at the start of this presentation.

----

The cantus firmus is basically a medieval hymn tune based on plain chant. This
is the cantus firmus that Fux uses throughout Gradus ad Parnassum.

----

The rules concern the valid intervals between the pitches of the two melodies
(shown in grey). Intervals are classified into two sets: consonances (which
sound "nice") and dissonances (which don't) marked with an asterisk.

----

The rules also concern how the contours of each melody relate to each other -
the so-called "motion".

Similar motion is when the melodies are moving in the same direction but by
different steps.

Parallel motion is when the melodies are moving in the same direction by the
same degree (distance).

Contrary motion is when the melodies are moving in different directions (for
example, one may be moving up in pitch whereas the other may be moving down).

Oblique motion is when one part is moving more often than the other.

----

The question I asked myself is how I might use Fux's heuristics to make
computer generated counterpoint.

----

Unfortunately, it's quite a tricky problem for the reasons given on the
slide. Furthermore, any solution that the computer generates should meet
these requirements.

----

However, there is an interesting programming technique that appeared to meet
these criteria: a genetic algorithm.

This type of solution will find good solutions (although not necessarily the
best ones) to problems that may have impossibly huge potential result sets.

Furthermore, they use evolutionary processes to find such results (hence their
name).

Finally, they're damn interesting and I wanted to learn more.

----

A genetic algorithm basically starts with an initial population of potential
solutions then iterates through a scoring (with a fitness function), breeding
and mutation process to produce new generations of candidates. Each generation
is assessed to find out if an acceptable solution has been "evolved": if so
the process stops, otherwise the iteration continues.

----

You can see this process encapsulated in this Python generator function. It
keeps producing new populations until the halt function discerns a solution
is found (or enough generations have gone by).

----

To make this more concrete I'll describe a very simple instance of the genetic
algorithm. I originally wanted to do this with some musical examples but it
ended up being too confusing. Instead, I've written a play example that
evolves words (called Wordolution).

The example shows the output of the program evolving the word "cat" using
generations of ten possible solutions.

The program stops, when the word "cat" has evolved in a population.

----

The fitness of each possible solution in a generation is based upon its
Levenshtein distance (number of characters different from a target word - in
this case "cat").

----

Every candidate solution is an instance of the Genome class. This encapsulates
two important pieces of information: the chromosome (that describes the
solution itself) and its fitness score. The chromosome is simply a list of
values (e.g. ['c', 'a', 't']).

The class has two important methods: breed and mutate (which is provided by
the sub class).

----

The breed function uses a technique called crossover to produce two children
from two parents.

----

The mutate function (in the child class) has a mutation_rate's chance of
assigning a new randomly selected character to a position in the solution's
chromosome (thus changing the spelling of the word).

----

The generate function describes how each new generation is created (so
allowing the genetic algorithm to explore new parts of the solution space).

It saves the fittest 50% of the prior generation then breeds the remaining
solutions by using something called roulette wheel selection (described in a
moment). These child solutions are then mutated as described earlier.

The final list of the combined top 50% of the old generation and the new
candidate solutions is combined to form the next generation.

----

Roulette wheel selection (shown as Python code) is so called because it's best
to imagine the process as a spin of a wheel at a casino.

----

Each solution gets an area of the wheel in proportion to its relative fitness
score. As a result, the fittest solutions get more of the wheel and are thus
more likely to be selected for breeding.

A random point is chosen on the wheel and the solution at that point is
returned.

----

Finally, the halt function tests the fittest solution of each generation to
see if it's acceptable. In this case, if the score is 3 (the length of the word
"cat") then every letter in the fittest solution is the same as "cat".

----

Foox works more or less in the same way but with the following differences:

The chromosome isn't a list of letters, rather, it is a list of numbers
representing pitches. This also means it's relatively easy to discover
intervals between notes.

----

The fitness functions for each species attempt to codify the heuristic rules.

The examples you see here ensure that, for first species counterpoint, the
solution starts and ends in the correct way.

----

Each species has a group of reward / punishment values that are used by the
fitness function to ensure the right sort of features evolve.

----

Simply run the foox command with arguments to define the species to use and
cantus firmus to set.

The result is a Lilypond file describing the musical result. Lilypond is a free
music typesetter which is then used to produce a PDF of the score and midi file
to listen to.

----

I mentioned that I wanted the solutions to fool most of the people most of the
time. This is where I find out if I've succeeded.

----

Since species counterpoint has been around for almost 300 years we have the
notebooks containing solutions for various famous composers: Mozart, Beethoven,
Brahms and Bruckner for example.

I'd like to see if you can tell the computer-generated solution from the
solution created by a human.

----

Species 1.

----

Species 2.

----

Species 3.

----

Species 4.

----

Unfortunately, this is as far as I've got. Fifth species is quite a way off.

----

In the end, it's been fun. Questions..!
