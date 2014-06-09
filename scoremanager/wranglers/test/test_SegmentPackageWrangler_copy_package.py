# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.iotools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_copy_package_01():
    r'''Works in library.
    
    Partial test because we can't be sure any user score packages will be
    present. And because Score PackageManager allows copying into user score 
    packges only (because copying into example score packages could pollute the
    example score packages).
    '''

    input_ = 'g cp A~(Red~Example~Score) q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - segments',
        'Abjad IDE - segments',
        ]
    assert score_manager._transcript.titles == titles
    assert 'Select storehouse:' in contents


def test_SegmentPackageWrangler_copy_package_02():
    r'''Works in score.
    '''

    source_path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'segments',
        'segment_01',
        )
    target_path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'segments',
        'copied_segment_01',
        )

    with systemtools.FilesystemState(keep=[source_path], remove=[target_path]):
        input_ = 'red~example~score g cp'
        input_ += ' A copied_segment_01 y q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        assert os.path.exists(source_path)
        assert os.path.exists(target_path)
        assert 'copied_segment_01' in contents