# -*- coding: utf-8 -*-
from abjad import *


def test_sequencetools_join_subsequences_01():

    result = sequencetools.join_subsequences([(1, 2, 3), (), (4, 5), (), (6,)])
    assert result == (1, 2, 3, 4, 5, 6)
