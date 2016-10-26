# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class SetClass(AbjadValueObject):
    r'''Set class.

    ..  container:: example

        **Example 1.** Initializes set class against Forte's list:

        ::

            >>> set_class = pitchtools.SetClass(4, 29)

        ::

            >>> str(set_class)
            'SC(4-29){0, 1, 3, 7}'

    ..  container:: example

        **Example 2.** Initializes set class lexically:

        ::

            >>> set_class = pitchtools.SetClass(4, 29, lex_rank=True)

        ::

            >>> str(set_class)
            'SC(4-29){0, 3, 6, 9}'

    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        '_cardinality',
        '_lex_rank',
        '_prime_form',
        '_rank',
        )

    _forte_identifier_to_prime_form = {
        (0, 1): (),
        (1, 1): (0,),
        (2, 1): (0, 1),
        (2, 2): (0, 2),
        (2, 3): (0, 3),
        (2, 4): (0, 4),
        (2, 5): (0, 5),
        (2, 6): (0, 6),
        (3, 1): (0, 1, 2),
        (3, 2): (0, 1, 3),
        (3, 3): (0, 1, 4),
        (3, 4): (0, 1, 5),
        (3, 5): (0, 1, 6),
        (3, 6): (0, 2, 4),
        (3, 7): (0, 2, 5),
        (3, 8): (0, 2, 6),
        (3, 9): (0, 2, 7),
        (3, 10): (0, 3, 6),
        (3, 11): (0, 3, 7),
        (3, 12): (0, 4, 8),
        (4, 1): (0, 1, 2, 3),
        (4, 2): (0, 1, 2, 4),
        (4, 3): (0, 1, 3, 4),
        (4, 4): (0, 1, 2, 5),
        (4, 5): (0, 1, 2, 6),
        (4, 6): (0, 1, 2, 7),
        (4, 7): (0, 1, 4, 5),
        (4, 8): (0, 1, 5, 6),
        (4, 9): (0, 1, 6, 7),
        (4, 10): (0, 2, 3, 5),
        (4, 11): (0, 1, 3, 5),
        (4, 12): (0, 2, 3, 6),
        (4, 13): (0, 1, 3, 6),
        (4, 14): (0, 2, 3, 7),
        (4, 15): (0, 1, 4, 6),
        (4, 16): (0, 1, 5, 7),
        (4, 17): (0, 3, 4, 7),
        (4, 18): (0, 1, 4, 7),
        (4, 19): (0, 1, 4, 8),
        (4, 20): (0, 1, 5, 8),
        (4, 21): (0, 2, 4, 6),
        (4, 22): (0, 2, 4, 7),
        (4, 23): (0, 2, 5, 7),
        (4, 24): (0, 2, 4, 8),
        (4, 25): (9, 2, 6, 8),
        (4, 26): (0, 3, 5, 8),
        (4, 27): (0, 2, 5, 8),
        (4, 28): (0, 3, 6, 9),
        (4, 29): (0, 1, 3, 7),
        (5, 1): (0, 1, 2, 3, 4),
        (5, 2): (0, 1, 2, 3, 5),
        (5, 3): (0, 1, 2, 4, 5),
        (5, 4): (0, 1, 2, 3, 6),
        (5, 5): (0, 1, 2, 3, 7),
        (5, 6): (0, 1, 2, 5, 6),
        (5, 7): (0, 1, 2, 6, 7),
        (5, 8): (0, 2, 3, 4, 6),
        (5, 9): (0, 1, 2, 4, 6),
        (5, 10): (0, 1, 3, 4, 6),
        (5, 11): (0, 2, 3, 4, 7),
        (5, 12): (0, 1, 3, 5, 6),
        (5, 13): (0, 1, 2, 4, 8),
        (5, 14): (0, 1, 2, 5, 7),
        (5, 15): (0, 1, 2, 6, 8),
        (5, 16): (0, 1, 3, 4, 7),
        (5, 17): (0, 1, 3, 4, 8),
        (5, 18): (0, 1, 4, 5, 7),
        (5, 19): (0, 1, 3, 6, 7),
        (5, 20): (0, 1, 3, 7, 8),
        (5, 21): (0, 1, 4, 5, 8),
        (5, 22): (0, 1, 4, 7, 8),
        (5, 23): (0, 2, 3, 5, 7),
        (5, 24): (0, 1, 3, 5, 7),
        (5, 25): (0, 2, 3, 5, 8),
        (5, 26): (0, 2, 4, 5, 8),
        (5, 27): (0, 1, 3, 5, 8),
        (5, 28): (0, 2, 3, 6, 8),
        (5, 29): (0, 1, 3, 6, 8),
        (5, 30): (0, 1, 4, 6, 8),
        (5, 31): (0, 1, 3, 6, 9),
        (5, 32): (0, 1, 4, 6, 9),
        (5, 33): (0, 2, 4, 6, 8),
        (5, 34): (0, 2, 4, 6, 9),
        (5, 35): (0, 2, 4, 7, 9),
        (5, 36): (0, 1, 2, 4, 7),
        (5, 37): (0, 3, 4, 5, 8),
        (5, 38): (0, 1, 2, 5, 8),
        (6, 1): (0, 1, 2, 3, 4, 5),
        (6, 2): (0, 1, 2, 3, 4, 6),
        (6, 3): (0, 1, 2, 3, 5, 6),
        (6, 4): (0, 1, 2, 4, 5, 6),
        (6, 5): (0, 1, 2, 5, 6, 7),
        (6, 6): (0, 1, 2, 5, 6, 7),
        (6, 7): (0, 1, 2, 6, 7, 8),
        (6, 8): (0, 2, 3, 4, 5, 7),
        (6, 9): (0, 1, 2, 3, 5, 7),
        (6, 10): (0, 1, 3, 4, 5, 7),
        (6, 11): (0, 1, 2, 4, 5, 7),
        (6, 12): (0, 1, 2, 4, 6, 7),
        (6, 13): (0, 1, 3, 4, 6, 7),
        (6, 14): (0, 1, 3, 4, 5, 8),
        (6, 15): (0, 1, 2, 4, 5, 8),
        (6, 16): (0, 1, 4, 5, 6, 8),
        (6, 17): (0, 1, 2, 4, 7, 8),
        (6, 18): (0, 1, 2, 5, 7, 8),
        (6, 19): (0, 1, 3, 4, 7, 8),
        (6, 20): (0, 1, 4, 5, 8, 9),
        (6, 21): (0, 2, 3, 4, 6, 8),
        (6, 22): (0, 1, 2, 4, 6, 8),
        (6, 23): (0, 2, 3, 5, 6, 8),
        (6, 24): (0, 1, 3, 4, 6, 8),
        (6, 25): (0, 1, 3, 5, 6, 8),
        (6, 26): (0, 1, 3, 5, 7, 8),
        (6, 27): (0, 1, 3, 4, 6, 9),
        (6, 28): (0, 1, 3, 5, 6, 9),
        (6, 29): (0, 1, 3, 6, 8, 9),
        (6, 30): (0, 1, 3, 6, 7, 9),
        (6, 31): (0, 1, 3, 5, 8, 9),
        (6, 32): (0, 2, 4, 5, 7, 9),
        (6, 33): (0, 2, 3, 5, 7, 9),
        (6, 34): (0, 1, 3, 5, 7, 9),
        (6, 35): (0, 2, 4, 6, 8, 10),
        (6, 36): (0, 1, 2, 3, 4, 7),
        (6, 37): (0, 1, 2, 3, 4, 8),
        (6, 38): (0, 1, 2, 3, 7, 8),
        (6, 39): (0, 2, 3, 4, 5, 8),
        (6, 40): (0, 1, 2, 3, 5, 8),
        (6, 41): (0, 1, 2, 3, 6, 8),
        (6, 42): (0, 1, 2, 3, 6, 9),
        (6, 43): (0, 1, 2, 5, 6, 8),
        (6, 44): (0, 1, 2, 5, 6, 9),
        (6, 45): (0, 2, 3, 4, 6, 9),
        (6, 46): (0, 1, 2, 4, 6, 9),
        (6, 47): (0, 1, 2, 4, 7, 9),
        (6, 48): (0, 1, 2, 5, 7, 9),
        (6, 49): (0, 1, 3, 4, 7, 9),
        (6, 50): (0, 1, 4, 6, 7, 9),
        }

    assert len(_forte_identifier_to_prime_form) == 137

    _lex_identifier_to_prime_form = {
        (0, 1): (),
        (1, 1): (0,),
        (2, 1): (0, 1),
        (2, 2): (0, 2),
        (2, 3): (0, 3),
        (2, 4): (0, 4),
        (2, 5): (0, 5),
        (2, 6): (0, 6),
        (3, 1): (0, 1, 2),
        (3, 2): (0, 1, 3),
        (3, 3): (0, 1, 4),
        (3, 4): (0, 1, 5),
        (3, 5): (0, 1, 6),
        (3, 6): (0, 2, 4),
        (3, 7): (0, 2, 5),
        (3, 8): (0, 2, 6),
        (3, 9): (0, 2, 7),
        (3, 10): (0, 3, 6),
        (3, 11): (0, 3, 7),
        (3, 12): (0, 4, 8),
        (4, 1): (0, 1, 2, 3),
        (4, 2): (0, 1, 2, 4),
        (4, 3): (0, 1, 2, 5),
        (4, 4): (0, 1, 2, 6),
        (4, 5): (0, 1, 2, 7),
        (4, 6): (0, 1, 3, 4),
        (4, 7): (0, 1, 3, 5),
        (4, 8): (0, 1, 3, 6),
        (4, 9): (0, 1, 3, 7),
        (4, 10): (0, 1, 4, 5),
        (4, 11): (0, 1, 4, 6),
        (4, 12): (0, 1, 4, 7),
        (4, 13): (0, 1, 4, 8),
        (4, 14): (0, 1, 5, 6),
        (4, 15): (0, 1, 5, 7),
        (4, 16): (0, 1, 5, 8),
        (4, 17): (0, 1, 6, 7),
        (4, 18): (0, 2, 3, 5),
        (4, 19): (0, 2, 3, 6),
        (4, 20): (0, 2, 3, 7),
        (4, 21): (0, 2, 4, 6),
        (4, 22): (0, 2, 4, 7),
        (4, 23): (0, 2, 4, 8),
        (4, 24): (0, 2, 5, 7),
        (4, 25): (0, 2, 5, 8),
        (4, 26): (0, 2, 6, 8),
        (4, 27): (0, 3, 4, 7),
        (4, 28): (0, 3, 5, 8),
        (4, 29): (0, 3, 6, 9),
        (5, 1): (0, 1, 2, 3, 4),
        (5, 2): (0, 1, 2, 3, 5),
        (5, 3): (0, 1, 2, 3, 6),
        (5, 4): (0, 1, 2, 3, 7),
        (5, 5): (0, 1, 2, 4, 5),
        (5, 6): (0, 1, 2, 4, 6),
        (5, 7): (0, 1, 2, 4, 7),
        (5, 8): (0, 1, 2, 4, 8),
        (5, 9): (0, 1, 2, 5, 6),
        (5, 10): (0, 1, 2, 5, 7),
        (5, 11): (0, 1, 2, 5, 8),
        (5, 12): (0, 1, 2, 6, 7),
        (5, 13): (0, 1, 2, 6, 8),
        (5, 14): (0, 1, 3, 4, 6),
        (5, 15): (0, 1, 3, 4, 7),
        (5, 16): (0, 1, 3, 4, 8),
        (5, 17): (0, 1, 3, 5, 6),
        (5, 18): (0, 1, 3, 5, 7),
        (5, 19): (0, 1, 3, 5, 8),
        (5, 20): (0, 1, 3, 6, 7),
        (5, 21): (0, 1, 3, 6, 8),
        (5, 22): (0, 1, 3, 6, 9),
        (5, 23): (0, 1, 3, 7, 8),
        (5, 24): (0, 1, 4, 5, 7),
        (5, 25): (0, 1, 4, 5, 8),
        (5, 26): (0, 1, 4, 6, 8),
        (5, 27): (0, 1, 4, 7, 8),
        (5, 28): (0, 1, 4, 7, 9),
        (5, 29): (0, 2, 3, 4, 6),
        (5, 30): (0, 2, 3, 4, 7),
        (5, 31): (0, 2, 3, 5, 7),
        (5, 32): (0, 2, 3, 5, 8),
        (5, 33): (0, 2, 3, 6, 8),
        (5, 34): (0, 2, 4, 5, 8),
        (5, 35): (0, 2, 4, 6, 8),
        (5, 36): (0, 2, 4, 6, 9),
        (5, 37): (0, 2, 4, 7, 9),
        (5, 38): (0, 3, 4, 5, 8),
        (6, 1): (0, 1, 2, 3, 4, 5),
        (6, 2): (0, 1, 2, 3, 4, 6),
        (6, 3): (0, 1, 2, 3, 4, 7),
        (6, 4): (0, 1, 2, 3, 4, 8),
        (6, 5): (0, 1, 2, 3, 5, 6),
        (6, 6): (0, 1, 2, 3, 5, 7),
        (6, 7): (0, 1, 2, 3, 5, 8),
        (6, 8): (0, 1, 2, 3, 6, 7),
        (6, 9): (0, 1, 2, 3, 6, 8),
        (6, 10): (0, 1, 2, 3, 6, 9),
        (6, 11): (0, 1, 2, 3, 7, 8),
        (6, 12): (0, 1, 2, 4, 5, 6),
        (6, 13): (0, 1, 2, 4, 5, 7),
        (6, 14): (0, 1, 2, 4, 5, 8),
        (6, 15): (0, 1, 2, 4, 6, 7),
        (6, 16): (0, 1, 2, 4, 6, 8),
        (6, 17): (0, 1, 2, 4, 6, 9),
        (6, 18): (0, 1, 2, 4, 7, 8),
        (6, 19): (0, 1, 2, 4, 7, 9),
        (6, 20): (0, 1, 2, 5, 6, 7),
        (6, 21): (0, 1, 2, 5, 6, 8),
        (6, 22): (0, 1, 2, 5, 7, 8),
        (6, 23): (0, 1, 2, 5, 7, 9),
        (6, 24): (0, 1, 2, 5, 8, 9),
        (6, 25): (0, 1, 2, 6, 7, 8),
        (6, 26): (0, 1, 3, 4, 5, 7),
        (6, 27): (0, 1, 3, 4, 5, 8),
        (6, 28): (0, 1, 3, 4, 6, 7),
        (6, 29): (0, 1, 3, 4, 6, 8),
        (6, 30): (0, 1, 3, 4, 6, 9),
        (6, 31): (0, 1, 3, 4, 7, 8),
        (6, 32): (0, 1, 3, 4, 7, 9),
        (6, 33): (0, 1, 3, 5, 6, 8),
        (6, 34): (0, 1, 3, 5, 6, 9),
        (6, 35): (0, 1, 3, 5, 7, 8),
        (6, 36): (0, 1, 3, 5, 7, 9),
        (6, 37): (0, 1, 3, 5, 8, 9),
        (6, 38): (0, 1, 3, 6, 7, 9),
        (6, 39): (0, 1, 3, 6, 8, 9),
        (6, 40): (0, 1, 4, 5, 6, 8),
        (6, 41): (0, 1, 4, 5, 8, 9),
        (6, 42): (0, 1, 4, 6, 7, 9),
        (6, 43): (0, 2, 3, 4, 5, 7),
        (6, 44): (0, 2, 3, 4, 5, 8),
        (6, 45): (0, 2, 3, 4, 6, 8),
        (6, 46): (0, 2, 3, 4, 6, 9),
        (6, 47): (0, 2, 3, 5, 6, 8),
        (6, 48): (0, 2, 3, 5, 7, 9),
        (6, 49): (0, 2, 4, 5, 7, 9),
        (6, 50): (0, 2, 4, 6, 8, 10),
        (7, 1): (0, 1, 2, 3, 4, 5, 6),
        (7, 2): (0, 1, 2, 3, 4, 5, 7),
        (7, 3): (0, 1, 2, 3, 4, 5, 8),
        (7, 4): (0, 1, 2, 3, 4, 6, 7),
        (7, 5): (0, 1, 2, 3, 4, 6, 8),
        (7, 6): (0, 1, 2, 3, 4, 6, 9),
        (7, 7): (0, 1, 2, 3, 4, 7, 8),
        (7, 8): (0, 1, 2, 3, 4, 7, 9),
        (7, 9): (0, 1, 2, 3, 5, 6, 7),
        (7, 10): (0, 1, 2, 3, 5, 6, 8),
        (7, 11): (0, 1, 2, 3, 5, 6, 9),
        (7, 12): (0, 1, 2, 3, 5, 7, 8),
        (7, 13): (0, 1, 2, 3, 5, 7, 9),
        (7, 14): (0, 1, 2, 3, 5, 8, 9),
        (7, 15): (0, 1, 2, 3, 6, 7, 8),
        (7, 16): (0, 1, 2, 3, 6, 8, 9),
        (7, 17): (0, 1, 2, 4, 5, 6, 8),
        (7, 18): (0, 1, 2, 4, 5, 6, 9),
        (7, 19): (0, 1, 2, 4, 5, 7, 8),
        (7, 20): (0, 1, 2, 4, 5, 7, 9),
        (7, 21): (0, 1, 2, 4, 5, 8, 9),
        (7, 22): (0, 1, 2, 4, 6, 7, 8),
        (7, 23): (0, 1, 2, 4, 6, 7, 9),
        (7, 24): (0, 1, 2, 4, 6, 8, 10),
        (7, 25): (0, 1, 2, 4, 6, 8, 9),
        (7, 26): (0, 1, 2, 4, 7, 8, 9),
        (7, 27): (0, 1, 2, 5, 6, 8, 9),
        (7, 28): (0, 1, 3, 4, 5, 6, 8),
        (7, 29): (0, 1, 3, 4, 5, 7, 8),
        (7, 30): (0, 1, 3, 4, 5, 7, 9),
        (7, 31): (0, 1, 3, 4, 6, 7, 9),
        (7, 32): (0, 1, 3, 4, 6, 8, 10),
        (7, 33): (0, 1, 3, 4, 6, 8, 9),
        (7, 34): (0, 1, 3, 5, 6, 7, 9),
        (7, 35): (0, 1, 3, 5, 6, 8, 10),
        (7, 36): (0, 2, 3, 4, 5, 6, 8),
        (7, 37): (0, 2, 3, 4, 5, 7, 9),
        (7, 38): (0, 2, 3, 4, 6, 7, 9),
        (8, 1): (0, 1, 2, 3, 4, 5, 6, 7),
        (8, 2): (0, 1, 2, 3, 4, 5, 6, 8),
        (8, 3): (0, 1, 2, 3, 4, 5, 6, 9),
        (8, 4): (0, 1, 2, 3, 4, 5, 7, 8),
        (8, 5): (0, 1, 2, 3, 4, 5, 7, 9),
        (8, 6): (0, 1, 2, 3, 4, 5, 8, 9),
        (8, 7): (0, 1, 2, 3, 4, 6, 7, 8),
        (8, 8): (0, 1, 2, 3, 4, 6, 7, 9),
        (8, 9): (0, 1, 2, 3, 4, 6, 8, 10),
        (8, 10): (0, 1, 2, 3, 4, 6, 8, 9),
        (8, 11): (0, 1, 2, 3, 4, 7, 8, 9),
        (8, 12): (0, 1, 2, 3, 5, 6, 7, 8),
        (8, 13): (0, 1, 2, 3, 5, 6, 7, 9),
        (8, 14): (0, 1, 2, 3, 5, 6, 8, 9),
        (8, 15): (0, 1, 2, 3, 5, 7, 8, 10),
        (8, 16): (0, 1, 2, 3, 5, 7, 8, 9),
        (8, 17): (0, 1, 2, 3, 5, 7, 9, 10),
        (8, 18): (0, 1, 2, 3, 6, 7, 8, 9),
        (8, 19): (0, 1, 2, 4, 5, 6, 7, 9),
        (8, 20): (0, 1, 2, 4, 5, 6, 8, 10),
        (8, 21): (0, 1, 2, 4, 5, 6, 8, 9),
        (8, 22): (0, 1, 2, 4, 5, 7, 8, 10),
        (8, 23): (0, 1, 2, 4, 5, 7, 8, 9),
        (8, 24): (0, 1, 2, 4, 5, 7, 9, 10),
        (8, 25): (0, 1, 2, 4, 6, 7, 8, 10),
        (8, 26): (0, 1, 3, 4, 5, 6, 7, 9),
        (8, 27): (0, 1, 3, 4, 5, 6, 8, 9),
        (8, 28): (0, 1, 3, 4, 6, 7, 9, 10),
        (8, 29): (0, 2, 3, 4, 5, 6, 7, 9),
        (9, 1): (0, 1, 2, 3, 4, 5, 6, 7, 8),
        (9, 2): (0, 1, 2, 3, 4, 5, 6, 7, 9),
        (9, 3): (0, 1, 2, 3, 4, 5, 6, 8, 10),
        (9, 4): (0, 1, 2, 3, 4, 5, 6, 8, 9),
        (9, 5): (0, 1, 2, 3, 4, 5, 7, 8, 9),
        (9, 6): (0, 1, 2, 3, 4, 5, 7, 9, 10),
        (9, 7): (0, 1, 2, 3, 4, 6, 7, 8, 9),
        (9, 8): (0, 1, 2, 3, 4, 6, 7, 9, 10),
        (9, 9): (0, 1, 2, 3, 4, 6, 8, 9, 10),
        (9, 10): (0, 1, 2, 3, 5, 6, 7, 8, 10),
        (9, 11): (0, 1, 2, 3, 5, 6, 8, 9, 10),
        (9, 12): (0, 1, 2, 4, 5, 6, 8, 9, 10),
        (10, 1): (0, 1, 2, 3, 4, 5, 6, 7, 8, 10),
        (10, 2): (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
        (10, 3): (0, 1, 2, 3, 4, 5, 6, 7, 9, 10),
        (10, 4): (0, 1, 2, 3, 4, 5, 6, 8, 9, 10),
        (10, 5): (0, 1, 2, 3, 4, 5, 7, 8, 9, 10),
        (10, 6): (0, 1, 2, 3, 4, 6, 7, 8, 9, 10),
        (11, 1): (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
        (12, 1): (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11),
        }

    _prime_form_to_forte_identifier = {
        v: k for k, v in
        _forte_identifier_to_prime_form.items()
        }

    _prime_form_to_lex_identifier = {
        v: k for k, v in
        _lex_identifier_to_prime_form.items()
        }

    ### INITIALIZER ###

    def __init__(self, cardinality=1, rank=1, lex_rank=None):
        from abjad.tools import pitchtools
        cardinality = int(cardinality)
        assert 0 <= cardinality < 12, repr(cardinality)
        self._cardinality = cardinality
        rank = int(rank)
        assert 1 <= rank, repr(rank)
        self._rank = rank
        assert isinstance(lex_rank, (type(None), type(True)))
        self._lex_rank = lex_rank
        prime_form = self._unrank(self.cardinality, self.rank)
        self._prime_form = prime_form

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''Gets string representation.

        ..  container:: example

            **Example 1.** Gets string:

            ::

                >>> set_class = pitchtools.SetClass(4, 29)
                >>> str(set_class)
                'SC(4-29){0, 1, 3, 7}'

        ..  container:: example

            **Example 2.** Gets string:

            ::

                >>> set_class = pitchtools.SetClass(6, 22)
                >>> str(set_class)
                'SC(6-22){0, 1, 2, 4, 6, 8}'

        Returns string.
        '''
        string = 'SC({}-{}){!s}'
        string = string.format(self.cardinality, self.rank, self.prime_form)
        return string

    ### PRIVATE METHODS ###

    def _unrank(self, cardinality, rank):
        from abjad.tools import pitchtools
        pair = (cardinality, rank)
        if self.lex_rank:
            prime_form = self._lex_identifier_to_prime_form[pair]
        else:
            prime_form = self._forte_identifier_to_prime_form[pair]
        prime_form = pitchtools.PitchClassSet(
            items=prime_form,
            item_class=pitchtools.NumberedPitchClass
            )
        return prime_form

    ### PUBLIC PROPERTIES ###

    @property
    def cardinality(self):
        r'''Gets cardinality.

        ..  container:: example

            **Example 0.** Gets cardinality of empty set class:

            ::

                >>> set_class = pitchtools.SetClass(0, 1)
                >>> set_class.cardinality
                0

        ..  container:: example

            **Example 1.** Gets cardinality:

            ::

                >>> set_class = pitchtools.SetClass(4, 29)
                >>> set_class.cardinality
                4

        ..  container:: example

            **Example 2.** Gets cardinality:

            ::

                >>> set_class = pitchtools.SetClass(6, 22)
                >>> set_class.cardinality
                6

        Set to integer between 0 and 12, inclusive.
        '''
        return self._cardinality

    @property
    def lex_rank(self):
        r'''Is true when set class uses lex rank.

        ..  container:: example
    
            **Example 1.** Uses Forte rank instead of lex rank:

            ::

                >>> set_class = pitchtools.SetClass(4, 29)
                >>> set_class
                SetClass(cardinality=4, rank=29)

            ::

                >>> str(set_class)
                'SC(4-29){0, 1, 3, 7}'

        ..  container:: example
    
            **Example 2.** Uses lex rank:

            ::

                >>> set_class = pitchtools.SetClass(4, 29, lex_rank=True)
                >>> set_class
                SetClass(cardinality=4, rank=29, lex_rank=True)

            ::

                >>> str(set_class)
                'SC(4-29){0, 3, 6, 9}'

        Set to true, false or none.

        Defaults to none.

        Returns true, false or none.
        '''
        return self._lex_rank

    @property
    def prime_form(self):
        r'''Gets prime form.

        ..  container:: example

            **Example 1.** Gets prime form:

            ::

                >>> set_class = pitchtools.SetClass(4, 29)
                >>> str(set_class)
                'SC(4-29){0, 1, 3, 7}'

            ::

                >>> set_class.prime_form
                PitchClassSet([0, 1, 3, 7])

        ..  container:: example

            **Example 2.** Gets prime form:

            ::

                >>> set_class = pitchtools.SetClass(6, 22)
                >>> str(set_class)
                'SC(6-22){0, 1, 2, 4, 6, 8}'

            ::

                >>> set_class.prime_form
                PitchClassSet([0, 1, 2, 4, 6, 8])

        Returns numbered pitch-class set.
        '''
        return self._prime_form

    @property
    def rank(self):
        r'''Gets rank.

        ..  container:: example

            **Example 1.** Gets rank of Forte-ranked set class:

            ::

                >>> set_class = pitchtools.SetClass(4, 29)
                >>> str(set_class)
                'SC(4-29){0, 1, 3, 7}'

            ::

                >>> set_class.rank
                29

        ..  container:: example

            **Example 2.** Gets rank of lex-ranked set class:

            ::

                >>> set_class = pitchtools.SetClass(4, 29, lex_rank=True)
                >>> str(set_class)
                'SC(4-29){0, 3, 6, 9}'

            ::

                >>> set_class.rank
                29

        Set to positive integer.

        Returns positive integer.
        '''
        return self._rank

    ### PUBLIC METHODS ###

    @staticmethod
    def from_pitch_class_set(pitch_class_set, lex_rank=None):
        r'''Makes set class from `pitch_class_set`.

        ..  container:: example

            **Example 1.** Makes set class from pitch-class set:

            ::

                >>> pc_set = pitchtools.PitchClassSet([9, 0, 3, 5, 6])
                >>> set_class = pitchtools.SetClass.from_pitch_class_set(pc_set)
                >>> print(set_class)
                SC(5-31){0, 1, 3, 6, 9}

            ::

                >>> pc_set = pitchtools.PitchClassSet([9, 0, 3, 5, 6])
                >>> set_class = pitchtools.SetClass.from_pitch_class_set(pc_set, lex_rank=True)
                >>> print(set_class)
                SC(5-22){0, 1, 3, 6, 9}

        ..  container:: example

            **Example 2.** Makes set class from pitch-class set:

            ::

                >>> pc_set = pitchtools.PitchClassSet([9, 11, 1, 2, 4, 6])
                >>> set_class = pitchtools.SetClass.from_pitch_class_set(pc_set)
                >>> print(set_class)
                SC(6-32){0, 2, 4, 5, 7, 9}

            ::

                >>> pc_set = pitchtools.PitchClassSet([9, 11, 1, 2, 4, 6])
                >>> set_class = pitchtools.SetClass.from_pitch_class_set(pc_set, lex_rank=True)
                >>> print(set_class)
                SC(6-49){0, 2, 4, 5, 7, 9}

        ..  container:: example

            **Example 3.** Makes set class from pitch-class set:

            ::

                >>> pc_set = pitchtools.PitchClassSet([11, 0, 5, 6])
                >>> set_class = pitchtools.SetClass.from_pitch_class_set(pc_set)
                >>> print(set_class)
                SC(4-9){0, 1, 6, 7}

            ::

                >>> pc_set = pitchtools.PitchClassSet([11, 0, 5, 6])
                >>> set_class = pitchtools.SetClass.from_pitch_class_set(pc_set, lex_rank=True)
                >>> print(set_class)
                SC(4-17){0, 1, 6, 7}

        Returns set class.
        '''
        from abjad.tools import pitchtools
        pitch_class_set = pitchtools.PitchClassSet(
            items=pitch_class_set,
            item_class=pitchtools.NumberedPitchClass,
            )
        prime_form = pitch_class_set.get_prime_form()
        prime_form = tuple([_.pitch_class_number for _ in sorted(prime_form)])
        if lex_rank:
            pair = SetClass._prime_form_to_lex_identifier[prime_form]
        else:
            pair = SetClass._prime_form_to_forte_identifier[prime_form]
        cardinality, rank = pair
        set_class = SetClass(
            cardinality=cardinality,
            rank=rank,
            lex_rank=lex_rank,
            )
        return set_class
