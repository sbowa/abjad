# -*- encoding: utf-8 -*-
from abjad.tools import componenttools
from abjad.tools import durationtools
from abjad.tools import mathtools


def remove_leaf_and_shrink_durated_parent_containers(leaf):
    r'''Remove `leaf` and shrink durated parent containers:

    ::

        >>> measure = Measure((4, 8), [])
        >>> measure.append(tuplettools.FixedDurationTuplet((2, 8), "c'8 d'8 e'8"))
        >>> measure.append(tuplettools.FixedDurationTuplet((2, 8), "f'8 g'8 a'8"))
        >>> spannertools.BeamSpanner(measure.select_leaves())
        BeamSpanner(c'8, d'8, e'8, f'8, g'8, a'8)

    ..  doctest::

        >>> f(measure)
        {
            \time 4/8
            \times 2/3 {
                c'8 [
                d'8
                e'8
            }
            \times 2/3 {
                f'8
                g'8
                a'8 ]
            }
        }

    ::

        >>> leaftools.remove_leaf_and_shrink_durated_parent_containers(
        ...     measure.select_leaves()[0])

    ..  doctest::

        >>> f(measure)
        {
            \time 5/12
            \scaleDurations #'(2 . 3) {
                {
                    d'8 [
                    e'8
                }
                {
                    f'8
                    g'8
                    a'8 ]
                }
            }
        }

    Return none.
    '''
    from abjad.tools import contexttools
    from abjad.tools import measuretools
    from abjad.tools import tuplettools

    prolated_leaf_duration = leaf.get_duration()
    parentage = leaf.select_parentage(include_self=False)
    prolations = parentage._prolations
    current_prolation, i = durationtools.Duration(1), 0
    parent = leaf._parent

    while parent is not None and not parent.is_simultaneous:
        current_prolation *= prolations[i]
        if isinstance(parent, tuplettools.FixedDurationTuplet):
            candidate_new_parent_dur = parent.target_duration - current_prolation * leaf.written_duration
            if durationtools.Duration(0) < candidate_new_parent_dur:
                parent.target_duration = candidate_new_parent_dur
        elif isinstance(parent, measuretools.Measure):
            parent_time_signature = parent.get_mark(
                contexttools.TimeSignatureMark)
            old_prolation = parent_time_signature.implied_prolation
            naive_time_signature = parent_time_signature.duration - prolated_leaf_duration
            better_time_signature = mathtools.NonreducedFraction(naive_time_signature)
            better_time_signature = better_time_signature.with_denominator(parent_time_signature.denominator)
            better_time_signature = contexttools.TimeSignatureMark(better_time_signature)
            parent.select().detach_marks(contexttools.TimeSignatureMark)
            better_time_signature.attach(parent)
            parent_time_signature = parent.get_mark(
                contexttools.TimeSignatureMark)
            new_denominator = parent_time_signature.denominator
            new_prolation = parent_time_signature.implied_prolation
            adjusted_prolation = old_prolation / new_prolation
            for x in parent:
                if isinstance(x, tuplettools.FixedDurationTuplet):
                    x.target_duration *= adjusted_prolation
                else:
                    if adjusted_prolation != 1:
                        new_target = x._preprolated_duration * adjusted_prolation
                        tuplettools.FixedDurationTuplet(new_target, [x])
        parent = parent._parent
        i += 1
    parentage = leaf.select_parentage(include_self=False)
    componenttools.remove_component_subtree_from_score_and_spanners([leaf])
    for x in parentage:
        if not len(x):
            componenttools.remove_component_subtree_from_score_and_spanners([x])
        else:
            break
