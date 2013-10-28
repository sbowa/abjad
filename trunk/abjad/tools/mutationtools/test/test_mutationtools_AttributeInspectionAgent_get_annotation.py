from abjad import *


def test_mutationtools_AttributeInspectionAgent_get_annotation_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    annotation = marktools.Annotation('special dictionary', {})
    attach(annotation, staff[0])

    assert inspect(staff[0]).get_annotation('special dictionary') == {}
