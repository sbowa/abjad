# -*- coding: utf-8 -*-
import operator
from abjad.tools.rhythmmakertools.Expression import Expression
from abjad.tools.topleveltools.new import new


class CompoundPattern(Expression):
    r'''Compound pattern.

    ..  container:: example

        **Example 1.** Matches every index that is (one of the first three
        indices) OR (one of the last three indices):

        ::

            >>> pattern = rhythmmakertools.CompoundPattern(
            ...     [
            ...         rhythmmakertools.BooleanPattern(
            ...             indices=[0, 1, 2],
            ...             ),
            ...         rhythmmakertools.BooleanPattern(
            ...             indices=[-3, -2, -1],
            ...             ),
            ...         ],
            ...     )

        ::

            >>> print(format(pattern))
            rhythmmakertools.CompoundPattern(
                (
                    rhythmmakertools.BooleanPattern(
                        indices=(0, 1, 2),
                        ),
                    rhythmmakertools.BooleanPattern(
                        indices=(-3, -2, -1),
                        ),
                    ),
                operator='or',
                )

        ..  container:: example

            **Example 2.** Matches every index that is (equal to 0 % 2) AND
            (not one of the last three indices):

            ::

                >>> pattern = rhythmmakertools.CompoundPattern(
                ...     [
                ...         rhythmmakertools.BooleanPattern(
                ...             indices=[0],
                ...             period=2,
                ...             ),
                ...         rhythmmakertools.BooleanPattern(
                ...             indices=[-3, -2, -1],
                ...             invert=True,
                ...             ),
                ...         ],
                ...     operator='and',
                ...     )

            ::

                >>> print(format(pattern))
                rhythmmakertools.CompoundPattern(
                    (
                        rhythmmakertools.BooleanPattern(
                            indices=(0,),
                            period=2,
                            ),
                        rhythmmakertools.BooleanPattern(
                            indices=(-3, -2, -1),
                            invert=True,
                            ),
                        ),
                    operator='and',
                    )

        ..  container:: example

            **Example 3.** Sieve from opening of Xenakis's **Psappha**:

            ::

                >>> sieve_1a = rhythmmakertools.select_every([0, 1, 7], period=8)
                >>> sieve_1b = rhythmmakertools.select_every([1, 3], period=5)
                >>> sieve_1 = rhythmmakertools.CompoundPattern(
                ...     [sieve_1a, sieve_1b],
                ...     operator='and',
                ...     )
                >>> sieve_2a = rhythmmakertools.select_every([0, 1, 2], period=8)
                >>> sieve_2b = rhythmmakertools.select_every([0], period=5)
                >>> sieve_2 = rhythmmakertools.CompoundPattern(
                ...     [sieve_2a, sieve_2b],
                ...     operator='and',
                ...     )
                >>> sieve_3 = rhythmmakertools.select_every([3], period=8)
                >>> sieve_4 = rhythmmakertools.select_every([4], period=8)
                >>> sieve_5a = rhythmmakertools.select_every([5, 6], period=8)
                >>> sieve_5b = rhythmmakertools.select_every([2, 3, 4], period=5)
                >>> sieve_5 = rhythmmakertools.CompoundPattern(
                ...     [sieve_5a, sieve_5b],
                ...     operator='and',
                ...     )
                >>> sieve_6 = rhythmmakertools.CompoundPattern(
                ...     [
                ...         rhythmmakertools.select_every([1], period=8),
                ...         rhythmmakertools.select_every([2], period=5),
                ...         ],
                ...     operator='and',
                ...     )
                >>> sieve_7 = rhythmmakertools.CompoundPattern(
                ...     [
                ...         rhythmmakertools.select_every([6], period=8),
                ...         rhythmmakertools.select_every([1], period=5),
                ...         ],
                ...     operator='and',
                ...     )
                >>> sieve = rhythmmakertools.CompoundPattern(
                ...     [
                ...         sieve_1,
                ...         sieve_2,
                ...         sieve_3,
                ...         sieve_4,
                ...         sieve_5,
                ...         sieve_6,
                ...         sieve_7,
                ...         ],
                ...     operator='or',
                ...     )

            ::

                >>> print(format(sieve))
                rhythmmakertools.CompoundPattern(
                    (
                        rhythmmakertools.CompoundPattern(
                            (
                                rhythmmakertools.BooleanPattern(
                                    indices=(0, 1, 7),
                                    period=8,
                                    ),
                                rhythmmakertools.BooleanPattern(
                                    indices=(1, 3),
                                    period=5,
                                    ),
                                ),
                            operator='and',
                            ),
                        rhythmmakertools.CompoundPattern(
                            (
                                rhythmmakertools.BooleanPattern(
                                    indices=(0, 1, 2),
                                    period=8,
                                    ),
                                rhythmmakertools.BooleanPattern(
                                    indices=(0,),
                                    period=5,
                                    ),
                                ),
                            operator='and',
                            ),
                        rhythmmakertools.BooleanPattern(
                            indices=(3,),
                            period=8,
                            ),
                        rhythmmakertools.BooleanPattern(
                            indices=(4,),
                            period=8,
                            ),
                        rhythmmakertools.CompoundPattern(
                            (
                                rhythmmakertools.BooleanPattern(
                                    indices=(5, 6),
                                    period=8,
                                    ),
                                rhythmmakertools.BooleanPattern(
                                    indices=(2, 3, 4),
                                    period=5,
                                    ),
                                ),
                            operator='and',
                            ),
                        rhythmmakertools.CompoundPattern(
                            (
                                rhythmmakertools.BooleanPattern(
                                    indices=(1,),
                                    period=8,
                                    ),
                                rhythmmakertools.BooleanPattern(
                                    indices=(2,),
                                    period=5,
                                    ),
                                ),
                            operator='and',
                            ),
                        rhythmmakertools.CompoundPattern(
                            (
                                rhythmmakertools.BooleanPattern(
                                    indices=(6,),
                                    period=8,
                                    ),
                                rhythmmakertools.BooleanPattern(
                                    indices=(1,),
                                    period=5,
                                    ),
                                ),
                            operator='and',
                            ),
                        ),
                    operator='or',
                    )

            ::

                >>> sieve.get_boolean_vector(total_length=40)
                [1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1,
                1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0]

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Masks'

    __slots__ = (
        '_invert',
        )

    _name_to_operator = {
        'and': operator.and_,
        'or': operator.or_,
        'xor': operator.xor,
        }

    ### INITIALIZER ###

    def __init__(self, items=None, invert=None, operator='or'):
        from abjad.tools import rhythmmakertools
        items = items or ()
        prototype = (rhythmmakertools.BooleanPattern, type(self))
        for item in items:
            assert isinstance(item, prototype), repr(item)
        assert operator in self._name_to_operator, repr(operator)
        Expression.__init__(
            self,
            items=items,
            operator=operator,
            )
        self._invert = invert

    ### SPECIAL METHODS ###

    def __and__(self, pattern):
        r'''Logical AND of two patterns.

        ..  container:: example

            **Example 1.** Flat grouping:

            ::

                >>> pattern_1 = rhythmmakertools.select_first(3)
                >>> pattern_2 = rhythmmakertools.select_last(3)
                >>> pattern_3 = rhythmmakertools.select_every([0], period=2)
                >>> pattern = pattern_1 & pattern_2 & pattern_3

            ::

                >>> print(format(pattern))
                rhythmmakertools.CompoundPattern(
                    (
                        rhythmmakertools.BooleanPattern(
                            indices=(0, 1, 2),
                            ),
                        rhythmmakertools.BooleanPattern(
                            indices=(-3, -2, -1),
                            ),
                        rhythmmakertools.BooleanPattern(
                            indices=(0,),
                            period=2,
                            ),
                        ),
                    operator='and',
                    )

            ::

                >>> pattern.get_boolean_vector(total_length=16)
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        ..  container:: example

            **Example 2.** Nested grouping:

            ::

                >>> pattern_1 = rhythmmakertools.select_first(3)
                >>> pattern_2 = rhythmmakertools.select_last(3)
                >>> pattern_3 = rhythmmakertools.select_every([0], period=2)
                >>> pattern = pattern_1 & pattern_2 | pattern_3

            ::

                >>> print(format(pattern))
                rhythmmakertools.CompoundPattern(
                    (
                        rhythmmakertools.CompoundPattern(
                            (
                                rhythmmakertools.BooleanPattern(
                                    indices=(0, 1, 2),
                                    ),
                                rhythmmakertools.BooleanPattern(
                                    indices=(-3, -2, -1),
                                    ),
                                ),
                            operator='and',
                            ),
                        rhythmmakertools.BooleanPattern(
                            indices=(0,),
                            period=2,
                            ),
                        ),
                    operator='or',
                    )

            ::

                >>> pattern.get_boolean_vector(total_length=16)
                [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]

        Returns new compound pattern.
        '''
        if self._can_append_to_self(pattern, 'and'):
            patterns = self.items + [pattern]
            result = type(self)(patterns, operator='and')
        else:
            result = type(self)([self, pattern], operator='and')
        return result

    def __neg__(self):
        r'''Logical NOT of pattern.

        ..  container:: example

            **Example 1.** Matches every index that is (one of the first three
            indices) or (one of the last three indices):

            ::

                >>> pattern_1 = rhythmmakertools.select_first(3)
                >>> pattern_2 = rhythmmakertools.select_last(3)
                >>> pattern = pattern_1 | pattern_2

            ::

                >>> print(format(pattern))
                rhythmmakertools.CompoundPattern(
                    (
                        rhythmmakertools.BooleanPattern(
                            indices=(0, 1, 2),
                            ),
                        rhythmmakertools.BooleanPattern(
                            indices=(-3, -2, -1),
                            ),
                        ),
                    operator='or',
                    )

            ::

                >>> pattern.get_boolean_vector(total_length=16)
                [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]

        ..  container:: example

            **Example 2.** Matches every index that is NOT (one of the first
            three indices) or (one of the last three indices):

            ::

                >>> pattern = -pattern
                >>> print(format(pattern))
                rhythmmakertools.CompoundPattern(
                    (
                        rhythmmakertools.BooleanPattern(
                            indices=(0, 1, 2),
                            ),
                        rhythmmakertools.BooleanPattern(
                            indices=(-3, -2, -1),
                            ),
                        ),
                    invert=True,
                    operator='or',
                    )

            ::

                >>> pattern.get_boolean_vector(total_length=16)
                [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]

        Returns new compound pattern.
        '''
        invert = not self.invert
        pattern = new(self, invert=invert)
        return pattern

    def __or__(self, pattern):
        r'''Logical OR of two patterns.

        ..  container:: example

            **Example 1.** Flat grouping:

            ::

                >>> pattern_1 = rhythmmakertools.select_first(3)
                >>> pattern_2 = rhythmmakertools.select_last(3)
                >>> pattern_3 = rhythmmakertools.select_every([0], period=2)
                >>> pattern = pattern_1 | pattern_2 | pattern_3

            ::

                >>> print(format(pattern))
                rhythmmakertools.CompoundPattern(
                    (
                        rhythmmakertools.BooleanPattern(
                            indices=(0, 1, 2),
                            ),
                        rhythmmakertools.BooleanPattern(
                            indices=(-3, -2, -1),
                            ),
                        rhythmmakertools.BooleanPattern(
                            indices=(0,),
                            period=2,
                            ),
                        ),
                    operator='or',
                    )

            ::

                >>> pattern.get_boolean_vector(total_length=16)
                [1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1]

        ..  container:: example

            **Example 2.** Nested grouping:

            ::

                >>> pattern_1 = rhythmmakertools.select_first(3)
                >>> pattern_2 = rhythmmakertools.select_last(3)
                >>> pattern_3 = rhythmmakertools.select_every([0], period=2)
                >>> pattern = pattern_1 | pattern_2 & pattern_3

            ::

                >>> print(format(pattern))
                rhythmmakertools.CompoundPattern(
                    (
                        rhythmmakertools.BooleanPattern(
                            indices=(0, 1, 2),
                            ),
                        rhythmmakertools.CompoundPattern(
                            (
                                rhythmmakertools.BooleanPattern(
                                    indices=(-3, -2, -1),
                                    ),
                                rhythmmakertools.BooleanPattern(
                                    indices=(0,),
                                    period=2,
                                    ),
                                ),
                            operator='and',
                            ),
                        ),
                    operator='or',
                    )

            ::

                >>> pattern.get_boolean_vector(total_length=16)
                [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]

        Returns new compound pattern.
        '''
        if self._can_append_to_self(pattern, 'or'):
            patterns = self.items + [pattern]
            result = type(self)(patterns, operator='or')
        else:
            result = type(self)([self, pattern], operator='or')
        return result

    def __xor__(self, pattern):
        r'''Logical XOR of two patterns.

        ..  container:: example

            **Example 1.** Flat grouping:

            ::

                >>> pattern_1 = rhythmmakertools.select_first(3)
                >>> pattern_2 = rhythmmakertools.select_last(3)
                >>> pattern_3 = rhythmmakertools.select_every([0], period=2)
                >>> pattern = pattern_1 ^ pattern_2 ^ pattern_3

            ::

                >>> print(format(pattern))
                rhythmmakertools.CompoundPattern(
                    (
                        rhythmmakertools.BooleanPattern(
                            indices=(0, 1, 2),
                            ),
                        rhythmmakertools.BooleanPattern(
                            indices=(-3, -2, -1),
                            ),
                        rhythmmakertools.BooleanPattern(
                            indices=(0,),
                            period=2,
                            ),
                        ),
                    operator='xor',
                    )

            ::

                >>> pattern.get_boolean_vector(total_length=16)
                [0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1]

        ..  container:: example

            **Example 2.** Nested grouping:

            ::

                >>> pattern_1 = rhythmmakertools.select_first(3)
                >>> pattern_2 = rhythmmakertools.select_last(3)
                >>> pattern_3 = rhythmmakertools.select_every([0], period=2)
                >>> pattern = pattern_1 ^ pattern_2 & pattern_3

            ::

                >>> print(format(pattern))
                rhythmmakertools.CompoundPattern(
                    (
                        rhythmmakertools.BooleanPattern(
                            indices=(0, 1, 2),
                            ),
                        rhythmmakertools.CompoundPattern(
                            (
                                rhythmmakertools.BooleanPattern(
                                    indices=(-3, -2, -1),
                                    ),
                                rhythmmakertools.BooleanPattern(
                                    indices=(0,),
                                    period=2,
                                    ),
                                ),
                            operator='and',
                            ),
                        ),
                    operator='xor',
                    )

            ::

                >>> pattern.get_boolean_vector(total_length=16)
                [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]

        Returns new compound pattern.
        '''
        if self._can_append_to_self(pattern, 'xor'):
            patterns = self.items + [pattern]
            result = type(self)(patterns, operator='xor')
        else:
            result = type(self)([self, pattern], operator='xor')
        return result

    ### PRIVATE METHODS ###

    def _can_append_to_self(self, pattern, operator_):
        from abjad.tools import rhythmmakertools
        if operator_ == self.operator:
            if isinstance(pattern, rhythmmakertools.BooleanPattern):
                return True
            if (isinstance(pattern, type(self)) and 
                pattern.operator == self.operator):
                return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def invert(self):
        '''Gets inversion flag of pattern.

        ..  container:: example

            **Example 1.** Matches every index that is (one of the first three
            indices) OR (one of the last three indices):

            ::

                >>> pattern_1 = rhythmmakertools.select_first(3)
                >>> pattern_2 = rhythmmakertools.select_last(3)
                >>> pattern = pattern_1 | pattern_2
                >>> pattern.invert is None
                True

            ::

                >>> pattern.get_boolean_vector(total_length=16)
                [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]


        ..  container:: example

            **Example 2.** Matches every index that is NOT (one of the first
            three indices) OR (one of the last three indices):

            ::

                >>> pattern = new(pattern, invert=True)
                >>> pattern.invert
                True

            ::

                >>> pattern.get_boolean_vector(total_length=16)
                [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._invert

    ### PUBLIC METHODS ###

    def get_boolean_vector(self, total_length, rotation=None):
        r'''Gets boolean vector of pattern applied to input sequence with
        `total_length`.

        ..  container:: example

            **Example 1.** Two-part pattern with logical OR:

            ::

                >>> pattern = rhythmmakertools.CompoundPattern(
                ...     [
                ...         rhythmmakertools.BooleanPattern(
                ...             indices=[0, 1, 2],
                ...             ),
                ...         rhythmmakertools.BooleanPattern(
                ...             indices=[-3, -2, -1],
                ...             ),
                ...         ],
                ...     operator='or',
                ...     )

            ::

                >>> pattern.get_boolean_vector(4)
                [1, 1, 1, 1]

            ::

                >>> pattern.get_boolean_vector(8)
                [1, 1, 1, 0, 0, 1, 1, 1]


            ::

                >>> pattern.get_boolean_vector(16)
                [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]

            Matches every index that is (one of the first three indices) OR
            (one of the last three indices).

        ..  container:: example

            **Example 2.** Two-part pattern with mixed periodic and inverted
            parts:

            ::

                >>> pattern = rhythmmakertools.CompoundPattern(
                ...     [
                ...         rhythmmakertools.BooleanPattern(
                ...             indices=[0],
                ...             period=2,
                ...             ),
                ...         rhythmmakertools.BooleanPattern(
                ...             indices=[-3, -2, -1],
                ...             invert=True,
                ...             ),
                ...         ],
                ...     operator='and',
                ...     )

            ::

                >>> pattern.get_boolean_vector(4)
                [1, 0, 0, 0]

            ::

                >>> pattern.get_boolean_vector(8)
                [1, 0, 1, 0, 1, 0, 0, 0]

            ::

                >>> pattern.get_boolean_vector(16)
                [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0]

            Matches every index that is (equal to 0 % 2) AND (not one of the
            last three indices).

        Returns list of ones and zeroes.
        '''
        boolean_vector = []
        for index in range(total_length):
            result = self.matches_index(index, total_length, rotation=rotation)
            boolean_vector.append(int(result))
        return boolean_vector

    def matches_index(self, index, total_length, rotation=None):
        r'''Is true when compound pattern matches `index` under
        `total_length`. Otherwise false.

        ..  container:: example

            **Example 1.** Empty pattern:

            ::

                >>> pattern = rhythmmakertools.CompoundPattern()

            Total length 16:

            ::

                >>> total_length = 16
                >>> for index in range(total_length):
                ...     match = pattern.matches_index(index, total_length)
                ...     match = match or ''
                ...     print(index, match)
                0 
                1 
                2 
                3 
                4 
                5 
                6 
                7 
                8 
                9 
                10 
                11 
                12 
                13 
                14 
                15 

            Total length 8:

            ::

                >>> total_length = 8
                >>> for index in range(total_length):
                ...     match = pattern.matches_index(index, total_length)
                ...     match = match or ''
                ...     print(index, match)
                0 
                1 
                2 
                3 
                4 
                5 
                6 
                7 

            Total length 4:

            ::

                >>> total_length = 4
                >>> for index in range(total_length):
                ...     match = pattern.matches_index(index, total_length)
                ...     match = match or ''
                ...     print(index, match)
                0 
                1 
                2 
                3 

            Matches nothing.

        ..  container:: example

            **Example 2.** Simple pattern:

            Logical OR:

            ::

                >>> pattern = rhythmmakertools.CompoundPattern(
                ...     [
                ...         rhythmmakertools.BooleanPattern(
                ...             indices=[0, 1, 2],
                ...             ),
                ...         ],
                ...     operator='or',
                ...     )
                >>> total_length = 16
                >>> for index in range(total_length):
                ...     match = pattern.matches_index(index, total_length)
                ...     match = match or ''
                ...     print(index, match)
                0 True
                1 True
                2 True
                3 
                4 
                5 
                6 
                7 
                8 
                9 
                10 
                11 
                12 
                13 
                14 
                15 

            Logical AND:

            ::

                >>> pattern = rhythmmakertools.CompoundPattern(
                ...     [
                ...         rhythmmakertools.BooleanPattern(
                ...             indices=[0, 1, 2],
                ...             ),
                ...         ],
                ...     operator='and',
                ...     )
                >>> total_length = 16
                >>> for index in range(total_length):
                ...     match = pattern.matches_index(index, total_length)
                ...     match = match or ''
                ...     print(index, match)
                0 True
                1 True
                2 True
                3 
                4 
                5 
                6 
                7 
                8 
                9 
                10 
                11 
                12 
                13 
                14 
                15 

            Logical XOR:

            ::

                >>> pattern = rhythmmakertools.CompoundPattern(
                ...     [
                ...         rhythmmakertools.BooleanPattern(
                ...             indices=[0, 1, 2],
                ...             ),
                ...         ],
                ...     operator='xor',
                ...     )
                >>> total_length = 16
                >>> for index in range(total_length):
                ...     match = pattern.matches_index(index, total_length)
                ...     match = match or ''
                ...     print(index, match)
                0 True
                1 True
                2 True
                3 
                4 
                5 
                6 
                7 
                8 
                9 
                10 
                11 
                12 
                13 
                14 
                15 

            Matches every index that is (one of the first three indices).

            Ignores `operator`.

        ..  container:: example

            **Example 3.** Two-part pattern with logical OR:

            ::

                >>> pattern = rhythmmakertools.CompoundPattern(
                ...     [
                ...         rhythmmakertools.BooleanPattern(
                ...             indices=[0, 1, 2],
                ...             ),
                ...         rhythmmakertools.BooleanPattern(
                ...             indices=[-3, -2, -1],
                ...             ),
                ...         ],
                ...     operator='or',
                ...     )

            Total length 16:

            ::

                >>> total_length = 16
                >>> for index in range(total_length):
                ...     match = pattern.matches_index(index, total_length)
                ...     match = match or ''
                ...     print(index, match)
                0 True
                1 True
                2 True
                3 
                4 
                5 
                6 
                7 
                8 
                9 
                10 
                11 
                12 
                13 True
                14 True
                15 True

            Total length 8:

            ::

                >>> total_length = 8
                >>> for index in range(total_length):
                ...     match = pattern.matches_index(index, total_length)
                ...     match = match or ''
                ...     print(index, match)
                0 True
                1 True
                2 True
                3 
                4 
                5 True
                6 True
                7 True

            Total length 4:

            ::

                >>> total_length = 4
                >>> for index in range(total_length):
                ...     match = pattern.matches_index(index, total_length)
                ...     match = match or ''
                ...     print(index, match)
                0 True
                1 True
                2 True
                3 True

            Matches every index that is (one of the first three indices) OR
            (one of the last three indices).

        ..  container:: example

            **Example 4.** Two-part pattern with logical AND:

            ::

                >>> pattern = rhythmmakertools.CompoundPattern(
                ...     [
                ...         rhythmmakertools.BooleanPattern(
                ...             indices=[0, 1, 2],
                ...             ),
                ...         rhythmmakertools.BooleanPattern(
                ...             indices=[-3, -2, -1],
                ...             ),
                ...         ],
                ...     operator='and',
                ...     )

            Total length 16:

            ::

                >>> total_length = 16
                >>> for index in range(total_length):
                ...     match = pattern.matches_index(index, total_length)
                ...     match = match or ''
                ...     print(index, match)
                0 
                1 
                2 
                3 
                4 
                5 
                6 
                7 
                8 
                9 
                10 
                11 
                12 
                13 
                14 
                15 

            Total length 8:

            ::

                >>> total_length = 8
                >>> for index in range(total_length):
                ...     match = pattern.matches_index(index, total_length)
                ...     match = match or ''
                ...     print(index, match)
                0 
                1 
                2 
                3 
                4 
                5 
                6 
                7 

            Total length 4:

            ::

                >>> total_length = 4
                >>> for index in range(total_length):
                ...     match = pattern.matches_index(index, total_length)
                ...     match = match or ''
                ...     print(index, match)
                0 
                1 True
                2 True
                3 

            Matches every index that is (one of the first three indices) AND
            (one of the last three indices).

        ..  container:: example

            **Example 5.** Two-part pattern with logical XOR:

            ::

                >>> pattern = rhythmmakertools.CompoundPattern(
                ...     [
                ...         rhythmmakertools.BooleanPattern(
                ...             indices=[0, 1, 2],
                ...             ),
                ...         rhythmmakertools.BooleanPattern(
                ...             indices=[-3, -2, -1],
                ...             ),
                ...         ],
                ...     operator='xor',
                ...     )

            Total length 16:

            ::

                >>> total_length = 16
                >>> for index in range(total_length):
                ...     match = pattern.matches_index(index, total_length)
                ...     match = match or ''
                ...     print(index, match)
                0 True
                1 True
                2 True
                3 
                4 
                5 
                6 
                7 
                8 
                9 
                10 
                11 
                12 
                13 True
                14 True
                15 True

            Total length 8:

            ::

                >>> total_length = 8
                >>> for index in range(total_length):
                ...     match = pattern.matches_index(index, total_length)
                ...     match = match or ''
                ...     print(index, match)
                0 True
                1 True
                2 True
                3 
                4 
                5 True
                6 True
                7 True

            Total length 4:

            ::

                >>> total_length = 4
                >>> for index in range(total_length):
                ...     match = pattern.matches_index(index, total_length)
                ...     match = match or ''
                ...     print(index, match)
                0 True
                1
                2
                3 True

            Matches every index that is (one of the first three indices) XOR
            (one of the last three indices).

        ..  container:: example

            **Example 6.** Two-part pattern with mixed periodic and inverted
            parts:

            ::

                >>> pattern = rhythmmakertools.CompoundPattern(
                ...     [
                ...         rhythmmakertools.BooleanPattern(
                ...             indices=[0],
                ...             period=2,
                ...             ),
                ...         rhythmmakertools.BooleanPattern(
                ...             indices=[-3, -2, -1],
                ...             invert=True,
                ...             ),
                ...         ],
                ...     operator='and',
                ...     )

            Total length 16:

            ::

                >>> total_length = 16
                >>> for index in range(total_length):
                ...     match = pattern.matches_index(index, total_length)
                ...     match = match or ''
                ...     print(index, match)
                0 True
                1 
                2 True
                3 
                4 True
                5 
                6 True
                7 
                8 True
                9 
                10 True
                11 
                12 True
                13 
                14 
                15 

            Total length 8:

            ::

                >>> total_length = 8
                >>> for index in range(total_length):
                ...     match = pattern.matches_index(index, total_length)
                ...     match = match or ''
                ...     print(index, match)
                0 True
                1 
                2 True
                3 
                4 True
                5 
                6 
                7 

            Total length 4:

            ::

                >>> total_length = 4
                >>> for index in range(total_length):
                ...     match = pattern.matches_index(index, total_length)
                ...     match = match or ''
                ...     print(index, match)
                0 True
                1 
                2 
                3 

            Matches every index that is (equal to 0 % 2) AND (not one of the
            last three indices).

        ..  container:: example

            **Example 7.** Complex pattern with compound and simple parts:

            ::

                >>> pattern = rhythmmakertools.CompoundPattern(
                ...     [
                ...         rhythmmakertools.BooleanPattern(
                ...             indices=[0],
                ...             period=2,
                ...             ),
                ...         rhythmmakertools.BooleanPattern(
                ...             indices=[-3, -2, -1],
                ...             invert=True,
                ...             ),
                ...         ],
                ...     operator='and',
                ...     )
                >>> pattern = rhythmmakertools.CompoundPattern(
                ...     [
                ...         pattern,
                ...         rhythmmakertools.BooleanPattern(
                ...             indices=[0, 1, 2],
                ...             ),
                ...         ],
                ...     operator='or',
                ...     )

            ::

                >>> print(format(pattern))
                rhythmmakertools.CompoundPattern(
                    (
                        rhythmmakertools.CompoundPattern(
                            (
                                rhythmmakertools.BooleanPattern(
                                    indices=(0,),
                                    period=2,
                                    ),
                                rhythmmakertools.BooleanPattern(
                                    indices=(-3, -2, -1),
                                    invert=True,
                                    ),
                                ),
                            operator='and',
                            ),
                        rhythmmakertools.BooleanPattern(
                            indices=(0, 1, 2),
                            ),
                        ),
                    operator='or',
                    )

            Total length 16:

            ::

                >>> total_length = 16
                >>> for index in range(total_length):
                ...     match = pattern.matches_index(index, total_length)
                ...     match = match or ''
                ...     print(index, match)
                0 True
                1 True
                2 True
                3 
                4 True
                5 
                6 True
                7 
                8 True
                9 
                10 True
                11 
                12 True
                13 
                14 
                15 

            Total length 8:

            ::

                >>> total_length = 8
                >>> for index in range(total_length):
                ...     match = pattern.matches_index(index, total_length)
                ...     match = match or ''
                ...     print(index, match)
                0 True
                1 True
                2 True
                3 
                4 True
                5 
                6 
                7 

            Total length 4:

            ::

                >>> total_length = 4
                >>> for index in range(total_length):
                ...     match = pattern.matches_index(index, total_length)
                ...     match = match or ''
                ...     print(index, match)
                0 True
                1 True
                2 True
                3 

            Matches every index that is ((equal to 0 % 2) AND (not one of the
            last three indices)) OR is (one of the first three indices).

        Returns true or false.
        '''
        if not self.items:
            result = False
        elif len(self.items) == 1:
            pattern = self.items[0]
            result = pattern.matches_index(
                index, 
                total_length,
                rotation=rotation,
                )
        else:
            operator_ = self._name_to_operator[self.operator]
            pattern = self.items[0]
            result = pattern.matches_index(
                index, 
                total_length, 
                rotation=rotation,
                )
            for pattern in self.items[1:]:
                result_ = pattern.matches_index(
                    index, 
                    total_length,
                    rotation=rotation,
                    )
                result = operator_(result, result_)
        if self.invert:
            result = not(result)
        return result