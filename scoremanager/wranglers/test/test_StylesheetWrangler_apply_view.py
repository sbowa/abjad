# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager

# must have is_test=False to test views
score_manager = scoremanager.core.ScoreManager(is_test=False)


def test_StylesheetWrangler_apply_view_01():
    r'''In library. Applies view.
    
    Makes sure only one stylesheet is visible after view is applied.
    '''
    
    input_ = 'y vnew _test rm all add clean-letter-14.ily done default'
    input_ += ' va _test vrm _test default q'
    score_manager._run(pending_user_input=input_)
    applied_view = score_manager._transcript[-8]

    lines = [
        'Score manager - stylesheet library (_test view)',
        '',
        '    1: clean-letter-14.ily (Abjad)',
        '',
        '    stylesheets - copy (cp)',
        '    stylesheets - new (new)',
        '    stylesheets - remove (rm)',
        '    stylesheets - rename (ren)',
        '',
        ]
    assert applied_view.lines == lines


def test_StylesheetWrangler_apply_view_02():
    r'''In score package. Applies view.
    
    Makes sure only one stylesheet is visible after view is applied.
    '''
    
    input_ = 'ssx red~example~score y vnew _test'
    input_ += ' rm all add stylesheet-addendum.ily done default'
    input_ += ' va _test vrm _test default q'
    score_manager._run(pending_user_input=input_)
    applied_view = score_manager._transcript[-8]

    lines = [
        'Red Example Score (2013) - stylesheets (_test view)',
        '',
        '    1: stylesheet-addendum.ily',
        '',
        '    stylesheets - copy (cp)',
        '    stylesheets - new (new)',
        '    stylesheets - remove (rm)',
        '    stylesheets - rename (ren)',
        '',
        ]
    assert applied_view.lines == lines