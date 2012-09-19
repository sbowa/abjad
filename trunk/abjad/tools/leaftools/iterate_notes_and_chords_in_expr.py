from abjad.tools import componenttools


def iterate_notes_and_chords_in_expr(expr, reverse=False, start=0, stop=None):
    r'''.. versionadded:: 2.10

    Iterate notes and chords forward in `expr`::

        >>> staff = Staff("<e' g' c''>8 a'8 r8 <d' f' b'>8 r2")

    ::

        >>> f(staff)
        \new Staff {
            <e' g' c''>8
            a'8
            r8
            <d' f' b'>8
            r2
        }

    ::

        >>> for leaf in leaftools.iterate_notes_and_chords_in_expr(staff):
        ...   leaf
        Chord("<e' g' c''>8")
        Note("a'8")
        Chord("<d' f' b'>8")

    Iterate notes and chords backward in `expr`::

        >>> for leaf in leaftools.iterate_notes_and_chords_in_expr(staff, reverse=True):
        ...   leaf
        Chord("<d' f' b'>8")
        Note("a'8")
        Chord("<e' g' c''>8")

    Ignore threads.

    Return generator.
    '''
    from abjad.tools import chordtools
    from abjad.tools import notetools

    return componenttools.iterate_components_in_expr(
        expr, klass=(notetools.Note, chordtools.Chord), reverse=reverse,
        start=start, stop=stop)
