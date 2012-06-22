
\version "2.14.2"

\header {
    title = "Untitled"
    subtitle = "Created on: Sat Jun 23 00:16:14 2012"
    composer = "Anonymous and Foox"
}

result = {
    <<
    \new Staff
    {
        \time 4/4
        \clef treble
        {
            a' 2 f' c'' a' b' c'' b' b' d'' b' d'' d'' f'' c'' d'' e'' c'' a' b' cis'' d'' 1
        }
    }
    \new Staff
    {
        \time 4/4
        \clef treble
        {
            d' 1 f' e' d' g' f' a' g' f' e' d' \bar "|."
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
    \result
    \midi {
        \context {
            \Score
            tempoWholesPerMinute = #(ly:make-moment 160 4)
        }
    }
    \layout {}
}
