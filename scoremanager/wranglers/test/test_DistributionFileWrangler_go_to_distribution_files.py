# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_DistributionFileWrangler_go_to_distribution_files_01():
    r'''From distribution directory to distribution directory.
    '''

    input_ = 'red~example~score d d q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - distribution files',
        'Red Example Score (2013) - distribution files',
        ]
    assert score_manager._transcript.titles == titles