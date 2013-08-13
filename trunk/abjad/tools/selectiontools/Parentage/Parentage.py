# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools.selectiontools.SimultaneousSelection \
    import SimultaneousSelection


class Parentage(SimultaneousSelection):
    r'''Abjad model of component parentage:

    ::

        >>> score = Score()
        >>> score.append(Staff(r"""\new Voice = "Treble Voice" { c'4 }""",
        ...     name='Treble Staff'))
        >>> score.append(Staff(r"""\new Voice = "Bass Voice" { b,4 }""",
        ...     name='Bass Staff'))

    ..  doctest::

        >>> f(score)
        \new Score <<
            \context Staff = "Treble Staff" {
                \context Voice = "Treble Voice" {
                    c'4
                }
            }
            \context Staff = "Bass Staff" {
                \context Voice = "Bass Voice" {
                    b,4
                }
            }
        >>

    ::

        >>> for x in selectiontools.Parentage(score): x
        ...
        Score<<2>>

    ::

        >>> for x in selectiontools.Parentage(score['Bass Voice'][0]): x
        ...
        Note('b,4')
        Voice-"Bass Voice"{1}
        Staff-"Bass Staff"{1}
        Score<<2>>

    Parentage is treated as a selection of the component's improper parentage.

    Return parentage instance.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_component', 
        '_root',
        )

    ### INITIALIZER ###

    def __init__(self, component=None, include_self=True):
        from abjad.tools import componenttools
        assert isinstance(component, (componenttools.Component, type(None)))
        if component is None:
            music = ()
        else:
            music = []
            if include_self:
                parent = component
            else:
                parent = component._parent
            while parent is not None:
                music.append(parent)
                parent = parent._parent
            music = tuple(music)
        SimultaneousSelection.__init__(self, music)
        self._component = component

    ### PRIVATE PROPERTIES ###

    @property
    def _prolations(self):
        prolations = []
        default = durationtools.Multiplier(1)
        for parent in self:
            prolation = getattr(parent, 'implied_prolation', default)
            prolations.append(prolation)
        return prolations

    ### PRIVATE METHODS ###

    @staticmethod
    def _id_string(component):
        lhs = component._class_name
        rhs = getattr(component, 'name', None) or id(component)
        return '{}-{!r}'.format(lhs, rhs)

    def _get_governor(self):
        from abjad.tools import containertools
        from abjad.tools import componenttools
        for component in self:
            if isinstance(component, containertools.Container) and \
                not component.is_simultaneous:
                if component._parent is None:
                    return component
                if isinstance(component._parent, containertools.Container) and \
                    component._parent.is_simultaneous:
                    return component

    def _get_spanner(self, spanner_classes=None):
        spanners = self._get_spanners(spanner_classes=spanner_classes)
        if not spanners:
            raise MissingSpannerError
        elif len(spanners) == 1:
            return spanners.pop()
        else:
            raise ExtraSpannerError

    def _get_spanners(self, spanner_classes=None):
        spanners = set()
        for component in self:
            spanners.update(component._get_spanners(spanner_classes))
        return spanners

    ### PUBLIC PROPERTIES ###

    @property
    def component(self):
        r'''The component from which the selection was derived.
        '''
        return self._component

    @property
    def logical_voice_indicator(self):
        r'''Logical voice indicator of component.

        ::

            >>> score = Score(
            ... r"""\context Staff = "CustomStaff" { """
            ...     r"""\context Voice = "CustomVoice" { c' d' e' f' } }""")
            >>> score.name = 'CustomScore'


        ..  doctest::

            >>> f(score)
            \context Score = "CustomScore" <<
                \context Staff = "CustomStaff" {
                    \context Voice = "CustomVoice" {
                        c'4
                        d'4
                        e'4
                        f'4
                    }
                }
            >>

        ::

            >>> leaf = score.select_leaves()[0]
            >>> parentage = more(leaf).select_parentage()
            >>> print parentage.logical_voice_indicator
                score: Score-'CustomScore'
                staff: Staff-...
                voice: Voice-'CustomVoice'

        Return logical voice indicator.
        '''
        from abjad.tools import componenttools
        from abjad.tools import contexttools
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        from abjad.tools import stafftools
        from abjad.tools import voicetools
        signature = selectiontools.LogicalVoiceIndicator()
        for component in self:
            if isinstance(component, voicetools.Voice) and \
                signature._voice is None:
                signature._voice = self._id_string(component)
            elif isinstance(component, stafftools.Staff) and \
                signature._staff is None:
                signature._staff = '{}-{}'.format(
                    component._class_name, id(component))
            elif isinstance(component, scoretools.StaffGroup) and \
                signature._staff_group is None:
                signature._staff_group = self._id_string(component)
            elif isinstance(component, scoretools.Score) and \
                signature._score is None:
                signature._score = self._id_string(component)
        signature._root = id(component)
        return signature

    @property
    def depth(self):
        r'''Length of proper parentage of component.

        Return nonnegative integer.
        '''
        return len(self[1:])

    @property
    def is_orphan(self):
        r'''True when component has no parent.
        Otherwise false.

        Return boolean.
        '''
        return self.parent is None

    @property
    def parent(self):
        r'''Parent of component or none when component is orphan.

        Return component or none.
        '''
        if 1 < len(self):
            return self[1]

    @property
    def prolation(self):
        prolations = [durationtools.Multiplier(1)] + self._prolations
        products = mathtools.cumulative_products(prolations)
        return products[-1]

    @property
    def root(self):
        r'''Last element in parentage.
        '''
        return self[-1]

    @property
    def score_index(self):
        r'''Score index of component:

        ::

            >>> staff_1 = Staff(
            ...     r"\times 2/3 { c'8 d'8 e'8 } \times 2/3 { f'8 g'8 a'8 }")
            >>> staff_2 = Staff(r"\times 2/3 { b'8 c''8 d''8 }")
            >>> score = Score([staff_1, staff_2])

        ..  doctest::

            >>> f(score)
            \new Score <<
                \new Staff {
                    \times 2/3 {
                        c'8
                        d'8
                        e'8
                    }
                    \times 2/3 {
                        f'8
                        g'8
                        a'8
                    }
                }
                \new Staff {
                    \times 2/3 {
                        b'8
                        c''8
                        d''8
                    }
                }
            >>

        ::

            >>> for leaf in score.select_leaves(
            ...     allow_discontiguous_leaves=True):
            ...     leaf, more(leaf).select_parentage().score_index
            ...
            (Note("c'8"), (0, 0, 0))
            (Note("d'8"), (0, 0, 1))
            (Note("e'8"), (0, 0, 2))
            (Note("f'8"), (0, 1, 0))
            (Note("g'8"), (0, 1, 1))
            (Note("a'8"), (0, 1, 2))
            (Note("b'8"), (1, 0, 0))
            (Note("c''8"), (1, 0, 1))
            (Note("d''8"), (1, 0, 2))

        Return tuple of zero or more nonnegative integers.
        '''
        result = []
        cur = self[0]
        for parent in self[1:]:
            index = parent.index(cur)
            result.insert(0, index)
            cur = parent
        result = tuple(result)
        return result

    @property
    def tuplet_depth(self):
        r'''Tuplet-depth of component:

        ::

            >>> tuplet = tuplettools.FixedDurationTuplet(
            ...     Duration(2, 8), "c'8 d'8 e'8")
            >>> staff = Staff([tuplet])
            >>> note = staff.select_leaves()[0]

        ::

            >>> more(note).select_parentage().tuplet_depth
            1

        ::

            >>> more(tuplet).select_parentage().tuplet_depth
            0

        ::

            >>> more(staff).select_parentage().tuplet_depth
            0

        Return nonnegative integer.
        '''
        from abjad.tools import tuplettools
        from abjad.tools import componenttools
        result = 0
        # should probably interate up to only first simultaneous container 
        # in parentage.
        # note that we probably need a named idea for 'parentage 
        # up to first simultaneous container'.
        for parent in self[1:]:
            if isinstance(parent, tuplettools.Tuplet):
                result += 1
        return result

    ### PUBLIC METHODS ###

    def get_first(self, component_classes=None):
        r'''Get first instance of `component_classes` in parentage.

        Return component or none.
        '''
        from abjad.tools import componenttools
        if component_classes is None:
            component_classes = (componenttools.Component,)
        if not isinstance(component_classes, tuple):
            component_classes = (component_classes,)
        for component in self:
            if isinstance(component, component_classes):
                return component
