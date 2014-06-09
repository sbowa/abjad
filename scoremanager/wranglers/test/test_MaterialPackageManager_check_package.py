# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.iotools.AbjadIDE(is_test=True)


def test_MaterialPackageManager_check_package_01():
    r'''Displays problems only.
    '''

    input_ = 'red~example~score m tempo~inventory ck y q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'Top level (6 assets): OK' in contents
    assert 'found' not in contents
    assert 'missing' not in contents


def test_MaterialPackageManager_check_package_02():
    r'''Displays everything.
    '''

    input_ = 'red~example~score m tempo~inventory ck n q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    lines = [
        '1 of 1 required directory found:',
        '2 of 2 required files found:',
        '3 optional files found:',
        ]
    for line in lines:
        assert line in contents
    assert 'No problem assets found.' not in contents


def test_MaterialPackageManager_check_package_03():
    r'''Supplies missing directory and missing file.
    '''

    material_directory = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'tempo_inventory',
        )
    versions_directory = os.path.join(material_directory, 'versions')
    initializer = os.path.join(material_directory, '__init__.py')
        
    with systemtools.FilesystemState(keep=[versions_directory, initializer]):
        os.remove(initializer)
        shutil.rmtree(versions_directory)
        input_ = 'red~example~score m tempo~inventory ck y y q'
        score_manager._run(input_=input_)
        assert os.path.isfile(initializer)
        assert os.path.isdir(versions_directory)