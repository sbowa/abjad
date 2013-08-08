# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_lily_voice_resolution_01():
    r'''Anonymous voice with a sequence of leaves,
    in the middle of which there is a parallel,
    which in turn contains two anonymous voices.
    How does LilyPond resolve voices?
    '''

    voice = Voice(notetools.make_repeated_notes(4))
    voice.insert(2, Container(Voice(notetools.make_repeated_notes(2)) * 2))
    voice[2].is_simultaneous = True
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    voice.override.note_head.color = 'red'

    r'''
    \new Voice \with {
        \override NoteHead #'color = #red
    } {
        c'8
        d'8
        <<
            \new Voice {
                e'8
                f'8
            }
            \new Voice {
                g'8
                a'8
            }
        >>
        b'8
        c''8
    }'''

    r'''LilyPond identifies three separate voices.
    LilyPond colors the outer four notes (c'8 d'8 b'8 c''8) red.
    LilyPond colors the inner four notes black.
    LilyPond issues clashing note column warnings for the inner notes.
    How should Abjad resolve voices?
    '''


def test_lily_voice_resolution_02():
    r'''Named voice with  with a sequence of leaves,
    in the middle of which there is a parallel,
    which in turn contains one like-named and one differently named voice.
    How does LilyPond resolve voices?
    '''

    voice = Voice(notetools.make_repeated_notes(4))
    voice.name = 'foo'
    voice.insert(2, Container(Voice(notetools.make_repeated_notes(2)) * 2))
    voice[2].is_simultaneous = True
    voice[2][0].name = 'foo'
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    voice.override.note_head.color = 'red'

    r'''
    \context Voice = "foo" \with {
        \override NoteHead #'color = #red
    } {
        c'8
        d'8
        <<
            \context Voice = "foo" {
                e'8
                f'8
            }
            \new Voice {
                g'8
                a'8
            }
        >>
        b'8
        c''8
    }
    '''

    r'''LilyPond colors six notes red and two notes black.
    LilyPond identifies two voices.
    '''


def test_lily_voice_resolution_03():
    r'''Two like-named voices in two differently named staves.
    '''

    container = Container(Staff([Voice("c'8 d'8")]) * 2)
    container[0].name = 'staff1'
    container[1].name = 'staff2'
    container[0][0].name = 'voicefoo'
    container[1][0].name = 'voicefoo'
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(container)
    py.test.raises(AssertionError, 'spannertools.BeamSpanner(container.select_leaves())')

    r'''LilyPond gives unterminated beam warnings.
    LilyPond gives grob direction programming errors.
    We conclude that LilyPond identifies two separate voices.
    Good example for Abjad voice resolution.
    '''


def test_lily_voice_resolution_04():
    r'''Container containing a run of leaves.
    Two like-structured parallels in the middle of the run.
    '''

    container = Container(notetools.make_repeated_notes(2))
    container[1:1] = Container(Voice(notetools.make_repeated_notes(2)) * 2) * 2
    container[1].is_simultaneous = True
    container[1][0].name = 'alto'
    container[1][1].name = 'soprano'
    container[2][0].name = 'alto'
    container[2][1].name = 'soprano'
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(container)

    container[1][1].override.note_head.color = 'red'
    container[2][1].override.note_head.color = 'red'

    r'''
    {
        c'8
        <<
            \context Voice = "alto" {
                d'8
                e'8
            }
            \context Voice = "soprano" \with {
                \override NoteHead #'color = #red
            } {
                f'8
                g'8
            }
        >>
        <<
            \context Voice = "alto" {
                a'8
                b'8
            }
            \context Voice = "soprano" \with {
                \override NoteHead #'color = #red
            } {
                c''8
                d''8
            }
        >>
        e''8
    }
    '''

    r'''LilyPond handles this example perfectly.
    LilyPond colors the four note_heads of the soprano voice red.
    LilyPond colors all other note_heads black.
    '''
