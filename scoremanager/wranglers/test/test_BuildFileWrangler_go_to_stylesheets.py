# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_BuildFileWrangler_go_to_stylesheets_01():
    r'''Goes from score build files to score stylesheets.
    '''

    input_ = 'red~example~score u y q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build files',
        'Red Example Score (2013) - stylesheets',
        ]
    assert score_manager._transcript.titles == titles


def test_BuildFileWrangler_go_to_stylesheets_02():
    r'''Goes from build file library to stylesheet library.
    '''

    input_ = 'u y q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - build files',
        'Abjad IDE - stylesheets',
        ]
    assert score_manager._transcript.titles == titles