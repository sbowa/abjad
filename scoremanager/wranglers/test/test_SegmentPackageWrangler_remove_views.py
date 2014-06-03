# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)
views_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__SegmentPackageWrangler_views__.py',
    )


def test_SegmentPackageWrangler_remove_views_01():
    r'''Makes two views. Removes two views at one time.
    '''

    with systemtools.FilesystemState(keep=[views_file]):
        input_ = 'g vnew _test_100 rm all'
        input_ += ' add A~(Red~Example~Score) done <return>' 
        input_ += ' g vnew _test_101 rm all'
        input_ += ' add segment~02~(Red~Example~Score) done <return>'
        input_ += ' q' 
        score_manager._run(input_=input_)

        input_ = 'g vls q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        assert 'found' in contents
        assert '_test_100' in contents
        assert '_test_101' in contents

        input_ = 'g vrm _test_100-_test_101 <return> q'
        score_manager._run(input_=input_)

        input_ = 'g vls q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        assert 'found' in contents or 'found' in contents
        assert '_test_100' not in contents
        assert '_test_101' not in contents


def test_SegmentPackageWrangler_remove_views_02():
    r'''Makes sure selector backtracking works.
    '''

    with systemtools.FilesystemState(keep=[views_file]):
        input_ = 'g vrm b q'
        score_manager._run(input_=input_)
        titles = [
            'Abjad IDE - scores',
            'Abjad IDE - segments',
            'Abjad IDE - segments - select view(s) to remove:',
            'Abjad IDE - segments',
            ]
        assert score_manager._transcript.titles == titles