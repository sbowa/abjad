import os
import scf


def test_DistDirectoryProxy_01():

    dist_proxy = scf.proxies.DistDirectoryProxy('example_score_1')

    assert dist_proxy.path_name == os.path.join(os.environ.get('SCORES'), 'example_score_1', 'dist')
    assert dist_proxy.source_file_name == \
        os.path.join(os.environ.get('SCFPATH'), 'proxies', 'DistDirectoryProxy', 'DistDirectoryProxy.py')
    assert dist_proxy.spaced_class_name == 'dist directory proxy'
