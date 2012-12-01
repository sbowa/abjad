from abjad import *
from experimental import *


def test_SegmentSpecification__select_divisions_time_relation_01():
    '''Stop-based time relation.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    red_segment.set_time_signatures(2 * [(3, 8)])
    red_segment.set_divisions([(4, 8)])
    time_relation = timerelationtools.timespan_2_stops_during_timespan_1
    divisions_that_stop_during_red = red_segment.select_division_timespan(time_relation=time_relation)
    divisions_that_stop_during_blue = blue_segment.select_division_timespan(time_relation=time_relation)
    red_segment.set_rhythm(library.sixteenths, selector=divisions_that_stop_during_red)
    blue_segment.set_rhythm(library.eighths, selector=divisions_that_stop_during_blue)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
