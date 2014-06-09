# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.iotools.AbjadIDE(is_test=True)


def test_SegmentPackageManager_go_to_material_packages_01():

    input_ = 'red~example~score g A m q'
    score_manager._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments',
        'Red Example Score (2013) - segments - A',
        'Red Example Score (2013) - materials',
        ]
    assert score_manager._transcript.titles == titles