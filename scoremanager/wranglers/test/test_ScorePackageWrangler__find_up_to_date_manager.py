# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
configuration = scoremanager.iotools.Configuration()
session = scoremanager.iotools.Session()
score_manager = scoremanager.iotools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler__find_up_to_date_manager_01():
    r'''Works with Git.
    '''

    wrangler = score_manager._score_package_wrangler
    manager = wrangler._find_up_to_date_manager(
        inside_score=False,
        system=True,
        repository='git',
        )

    storehouse = configuration.example_score_packages_directory

    assert isinstance(manager, scoremanager.wranglers.ScorePackageManager)
    assert manager._is_git_versioned()
    assert manager._is_up_to_date()
    assert manager._path.startswith(storehouse)
    assert not manager._path == storehouse


def test_ScorePackageWrangler__find_up_to_date_manager_02():
    r'''Works with Subversion.
    '''

    wrangler = score_manager._score_package_wrangler
    manager = wrangler._find_up_to_date_manager(
        inside_score=False,
        system=False,
        repository='svn',
        )

    if not manager:
        return

    storehouse = configuration.user_score_packages_directory

    assert isinstance(manager, scoremanager.wranglers.ScorePackageManager)
    assert manager._is_svn_versioned()
    assert manager._is_up_to_date()
    assert manager._path.startswith(storehouse)
    assert not manager._path == storehouse