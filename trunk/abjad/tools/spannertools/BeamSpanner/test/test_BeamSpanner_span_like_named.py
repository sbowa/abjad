# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_BeamSpanner_span_like_named_01():
    r'''Abjad lets you span liked named voices.
    '''

    staff = Staff(Voice(notetools.make_repeated_notes(4)) * 2)
    staff[0].name = 'foo'
    staff[1].name = 'foo'
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(staff)

    beam = spannertools.BeamSpanner(staff)
    assert len(beam.components) == 1
    assert isinstance(beam.components[0], Staff)
    assert len(beam.leaves) == 8

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \context Voice = "foo" {
                c'8 [
                cs'8
                d'8
                ef'8
            }
            \context Voice = "foo" {
                e'8
                f'8
                fs'8
                g'8 ]
            }
        }
        '''
        )
    beam.detach()

    beam = spannertools.BeamSpanner(staff[:])
    assert len(beam.components) == 2
    for x in beam.components:
        assert isinstance(x, Voice)
    assert len(beam.leaves) == 8

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \context Voice = "foo" {
                c'8 [
                cs'8
                d'8
                ef'8
            }
            \context Voice = "foo" {
                e'8
                f'8
                fs'8
                g'8 ]
            }
        }
        '''
        )


# TODO: move to slur spanner test file
def test_BeamSpanner_span_like_named_02():
    '''Abjad lets you span over liked named staves
    so long as the voices nested in the staves are named the same.
    '''

    container = Container(
        Staff([Voice(notetools.make_repeated_notes(4))]) * 2)
    container[0].name, container[1].name = 'foo', 'foo'
    container[0][0].name, container[1][0].name = 'bar', 'bar'
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(
        container)
    slur = spannertools.SlurSpanner(container)


    assert testtools.compare(
        container,
        r'''
        {
            \context Staff = "foo" {
                \context Voice = "bar" {
                    c'8 (
                    cs'8
                    d'8
                    ef'8
                }
            }
            \context Staff = "foo" {
                \context Voice = "bar" {
                    e'8
                    f'8
                    fs'8
                    g'8 )
                }
            }
        }
        '''
        )

    assert select(container).is_well_formed()


def test_BeamSpanner_span_like_named_03():
    '''Like-named containers need not be lexically contiguous.
    '''

    container = Container(Container(Voice(notetools.make_repeated_notes(4)) * 2) * 2)
    container[0].is_simultaneous = True
    container[1].is_simultaneous = True
    container[0][0].name, container[1][1].name = 'first', 'first'
    container[0][1].name, container[1][0].name = 'second', 'second'
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(container)

    beam = spannertools.BeamSpanner([container[0][0], container[1][1]])
    assert len(beam.components) == 2
    assert isinstance(beam.components[0], Voice)
    assert isinstance(beam.components[1], Voice)
    assert len(beam.leaves) == 8
    beam.detach()

    r'''
    {
        <<
            \context Voice = "first" {
                c'8 [
                cs'8
                d'8
                ef'8
            }
            \context Voice = "second" {
                e'8
                f'8
                fs'8
                g'8
            }
        >>
        <<
            \context Voice = "second" {
                af'8
                a'8
                bf'8
                b'8
            }
            \context Voice = "first" {
                c''8
                cs''8
                d''8
                ef''8 ]
            }
        >>
    }
    '''


def test_BeamSpanner_span_like_named_04():
    '''
    Asymmetric structures are no problem.
    '''

    container = Container(Container(Voice(notetools.make_repeated_notes(4)) * 2) * 2)
    container[0].is_simultaneous = True
    container[1].is_simultaneous = True
    container[0][0].name, container[1][0].name = 'first', 'first'
    container[0][1].name, container[1][1].name = 'second', 'second'
    del(container[1][1])
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(container)
    beam = spannertools.BeamSpanner([container[0][0], container[1][0]])

    assert len(beam.components) == 2
    assert len(beam.leaves) == 8

    assert testtools.compare(
        container,
        r'''
        {
            <<
                \context Voice = "first" {
                    c'8 [
                    cs'8
                    d'8
                    ef'8
                }
                \context Voice = "second" {
                    e'8
                    f'8
                    fs'8
                    g'8
                }
            >>
            <<
                \context Voice = "first" {
                    af'8
                    a'8
                    bf'8
                    b'8 ]
                }
            >>
        }
        '''
        )

    r'''
    {
        <<
            \context Voice = "first" {
                c'8 [
                cs'8
                d'8
                ef'8
            }
            \context Voice = "second" {
                e'8
                f'8
                fs'8
                g'8
            }
        >>
        <<
            \context Voice = "first" {
                af'8
                a'8
                bf'8
                b'8 ]
            }
        >>
    }
    '''
