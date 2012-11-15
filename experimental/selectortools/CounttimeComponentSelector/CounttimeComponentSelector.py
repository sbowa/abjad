from experimental import helpertools
from experimental.selectortools.InequalitySelector import InequalitySelector
from experimental.selectortools.SliceSelector import SliceSelector


class CounttimeComponentSelector(SliceSelector, InequalitySelector):
    r'''.. versionadded:: 1.0

    Select zero or more counttime components restricted according to keywords.

        >>> from experimental import *

    Select the first five counttime components::

        >>> selectortools.CounttimeComponentSelector(stop_identifier=5)
        CounttimeComponentSelector(stop_identifier=5)

    Select the last five counttime components::

        >>> selectortools.CounttimeComponentSelector(start_identifier=-5)
        CounttimeComponentSelector(start_identifier=-5)

    Select counttime components from ``5`` up to but not including ``-5``::

        >>> selectortools.CounttimeComponentSelector(start_identifier=5, stop_identifier=-5)
        CounttimeComponentSelector(start_identifier=5, stop_identifier=-5)

    Select all counttime components::

        >>> selectortools.CounttimeComponentSelector()
        CounttimeComponentSelector()

    Select counttime measure ``3`` to starting during segment ``'red'``.
    Then select the last three leaves in tuplet ``-1`` in this measure::

        >>> segment_selector = selectortools.SingleSegmentSelector(identifier='red')
        >>> time_relation = timerelationtools.timespan_2_starts_during_timespan_1(timespan_1=segment_selector.timespan)

    ::

        >>> measure_selector = selectortools.CounttimeComponentSelector(
        ... time_relation=time_relation, klass=Measure, start_identifier=3, stop_identifier=4)

    ::

        >>> tuplet_selector = selectortools.CounttimeComponentSelector(
        ... selector=measure_selector, klass=Tuplet, start_identifier=-1)

    ::

        >>> leaf_slice_selector = selectortools.CounttimeComponentSelector(
        ... selector=tuplet_selector, klass=leaftools.Leaf, start_identifier=-3)

    ::

        >>> z(leaf_slice_selector)
        selectortools.CounttimeComponentSelector(
            klass=leaftools.Leaf,
            selector=selectortools.CounttimeComponentSelector(
                klass=tuplettools.Tuplet,
                selector=selectortools.CounttimeComponentSelector(
                    time_relation=timerelationtools.TimespanTimespanTimeRelation(
                        'timespan_1.start <= timespan_2.start < timespan_1.stop',
                        timespan_1=symbolictimetools.SingleSourceSymbolicTimespan(
                            selector=selectortools.SingleSegmentSelector(
                                identifier='red'
                                )
                            )
                        ),
                    klass=measuretools.Measure,
                    start_identifier=3,
                    stop_identifier=4
                    ),
                start_identifier=-1
                ),
            start_identifier=-3
            )

    Counttime component slice selectors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, time_relation=None, klass=None, predicate=None, selector=None,
        start_identifier=None, stop_identifier=None):
        from experimental import selectortools
        assert isinstance(selector, (selectortools.SliceSelector, type(None))), repr(selector)
        assert klass is None or helpertools.is_counttime_component_klass_expr(klass), repr(klass)
        assert isinstance(predicate, (helpertools.Callback, type(None))), repr(predicate)
        SliceSelector.__init__(self, start_identifier=start_identifier, stop_identifier=stop_identifier)
        InequalitySelector.__init__(self, time_relation=time_relation)
        self._selector = selector
        if isinstance(klass, tuple):
            klass = helpertools.KlassInventory(klass)
        self._klass = klass
        self._predicate = predicate

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def klass(self):
        '''Class of counttime component selector specified by user.

        Return counttime component class or none.
        '''
        return self._klass

    @property
    def predicate(self):
        '''Predicate of counttime component selector specified by user.

        Return callback or none.
        '''
        return self._predicate

    @property
    def selector(self):
        '''Counttime component slice selector selector.

        To allow selectors to selector recursively.

        Return slice selector.
        '''
        return self._selector

    ### PUBLIC METHODS ###

    def get_offsets(self, score_specification, context_name):
        '''Evaluate start and stop offsets of selector when applied
        to `context_name` in `score_specification`.

        .. note:: not yet implemented.

        Return pair.
        '''
        raise NotImplementedError

    def get_selected_objects(self, score_specification, context_name):
        '''Get counttime components selected when selector is applied
        to `context_name` in `score_specification`.

        Return list.
        '''
        raise NotImplementedError
