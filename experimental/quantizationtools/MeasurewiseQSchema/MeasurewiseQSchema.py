from abjad.tools import contexttools
from abjad.tools import durationtools
from experimental.quantizationtools.QSchema import QSchema


class MeasurewiseQSchema(QSchema):
    '''Concrete QSchema subclass which treats "measures" as its time-step unit:

    ::

        >>> from experimental import quantizationtools
        >>> q_schema = quantizationtools.MeasurewiseQSchema()

    Without arguments, it uses smart defaults:

    ::

        >>> q_schema
        quantizationtools.MeasurewiseQSchema(
            search_tree=quantizationtools.SimpleSearchTree(
                definition={   2: {   2: {   2: {   2: None}, 3: None}, 3: None, 5: None, 7: None},
                    3: {   2: {   2: None}, 3: None, 5: None},
                    5: {   2: None, 3: None},
                    7: {   2: None},
                    11: None,
                    13: None}
                ),
            tempo=contexttools.TempoMark(
                durationtools.Duration(1, 4),
                60
                ),
            time_signature=contexttools.TimeSignatureMark(
                (4, 4)
                ),
            use_full_measure=False,
            )

    Each time-step in a ``MeasurewiseQSchema`` is composed of four settings:

        * search_tree
        * tempo
        * time_signature
        * use_full_measure

    These settings are understood to persist for the entirety of the measure which
    comprises that time-step.  All of these settings are self-descriptive, except for
    ``use_full_measure``, which controls whether the measure is subdivided by the
    ``Quantizer`` into beats according to its time signature.

    If ``use_full_measure`` is ``False``, the time-step's measure will be divided 
    into units according to its time-signature, with, for example, a 4/4 measure 
    being divided into 4 units, each having a beatspan of 1/4.

    On the other hand, if ``use_full_measure`` is set to ``True``, the time-step's 
    measure will not be subdivided into independent quantization units, likely
    resulting in tuplets which take up the full duration of that measure.
    
    The computed value at any non-negative time-step can be found by subscripting:

    ::

        >>> index = 0
        >>> for key, value in sorted(q_schema[index].items()): print '{}:'.format(key), value
        ... 
        search_tree: SimpleSearchTree(
            definition={   2: {   2: {   2: {   2: None}, 3: None}, 3: None, 5: None, 7: None},
                3: {   2: {   2: None}, 3: None, 5: None},
                5: {   2: None, 3: None},
                7: {   2: None},
                11: None,
                13: None}
            )
        tempo: TempoMark(Duration(1, 4), 60)
        time_signature: 4/4
        use_full_measure: False

    ::

        >>> index = 1000
        >>> for key, value in sorted(q_schema[index].items()): print '{}:'.format(key), value
        ... 
        search_tree: SimpleSearchTree(
            definition={   2: {   2: {   2: {   2: None}, 3: None}, 3: None, 5: None, 7: None},
                3: {   2: {   2: None}, 3: None, 5: None},
                5: {   2: None, 3: None},
                7: {   2: None},
                11: None,
                13: None}
            )
        tempo: TempoMark(Duration(1, 4), 60)
        time_signature: 4/4
        use_full_measure: False

    Per-time-step settings can be applied in a variety of ways.

    Instantiating the schema via ``*args`` with a series of either ``MeasurewiseQSchemaItem`` instances,
    or dictionaries which could be used to instantiate ``MeasurewiseQSchemaItem`` instances,
    will apply those settings sequentially, starting from time-step ``0``:

    ::

        >>> a = {'search_tree': quantizationtools.SimpleSearchTree({2: None})}
        >>> b = {'search_tree': quantizationtools.SimpleSearchTree({3: None})}
        >>> c = {'search_tree': quantizationtools.SimpleSearchTree({5: None})}

    ::

        >>> q_schema = quantizationtools.MeasurewiseQSchema(a, b, c)

    ::

        >>> q_schema[0]['search_tree']
        SimpleSearchTree(
            definition={   2: None}
            )

    ::

        >>> q_schema[1]['search_tree']
        SimpleSearchTree(
            definition={   3: None}
            )

    ::

        >>> q_schema[2]['search_tree']
        SimpleSearchTree(
            definition={   5: None}
            )

    ::

        >>> q_schema[1000]['search_tree']
        SimpleSearchTree(
            definition={   5: None}
            )

    Similarly, instantiating the schema from a single dictionary, consisting of integer:specification
    pairs, or a sequence via ``*args`` of (integer, specification) pairs, allows for applying settings to 
    non-sequential time-steps:

    ::

        >>> a = {'time_signature': contexttools.TimeSignatureMark((7, 32))}
        >>> b = {'time_signature': contexttools.TimeSignatureMark((3, 4))}
        >>> c = {'time_signature': contexttools.TimeSignatureMark((5, 8))}

    ::

        >>> settings = {
        ...     2: a,
        ...     4: b,
        ...     6: c,
        ... }

    ::

        >>> q_schema = quantizationtools.MeasurewiseQSchema(settings)

    ::

        >>> q_schema[0]['time_signature']
        TimeSignatureMark((4, 4))

    ::

        >>> q_schema[1]['time_signature']
        TimeSignatureMark((4, 4))

    ::

        >>> q_schema[2]['time_signature']
        TimeSignatureMark((7, 32))

    ::

        >>> q_schema[3]['time_signature']
        TimeSignatureMark((7, 32))

    ::

        >>> q_schema[4]['time_signature']
        TimeSignatureMark((3, 4))

    ::

        >>> q_schema[5]['time_signature']
        TimeSignatureMark((3, 4))

    ::

        >>> q_schema[6]['time_signature']
        TimeSignatureMark((5, 8))

    ::

        >>> q_schema[1000]['time_signature']
        TimeSignatureMark((5, 8))

    The following is equivalent to the above schema definition:

    ::

        >>> q_schema = quantizationtools.MeasurewiseQSchema(
        ...     (2, {'time_signature': contexttools.TimeSignatureMark((7, 32))}),
        ...     (4, {'time_signature': contexttools.TimeSignatureMark((3, 4))}),
        ...     (6, {'time_signature': contexttools.TimeSignatureMark((5, 8))}),
        ...     )

    Return ``MeasurewiseQSchema`` instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_items', '_lookups', '_search_tree', '_tempo', '_time_signature', '_use_full_measure')

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        from experimental import quantizationtools

        search_tree = kwargs.get('search_tree', quantizationtools.SimpleSearchTree())
        assert isinstance(search_tree, quantizationtools.SearchTree)
        self._search_tree = search_tree

        self._tempo = contexttools.TempoMark(
            kwargs.get('tempo',
                ((1, 4), 60)))

        self._time_signature = contexttools.TimeSignatureMark(
            kwargs.get('time_signature',
                (4, 4)))

        self._use_full_measure = bool(kwargs.get('use_full_measure'))

        QSchema.__init__(self, *args, **kwargs)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _keyword_argument_names(self):
        return ('search_tree', 'tempo', 'time_signature', 'use_full_measure')

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def item_klass(self):
        '''The schema's item class.'''
        from experimental import quantizationtools
        return quantizationtools.MeasurewiseQSchemaItem

    @property
    def target_item_klass(self):
        from experimental import quantizationtools
        return quantizationtools.QTargetMeasure

    @property
    def target_klass(self):
        from experimental import quantizationtools
        return quantizationtools.MeasurewiseQTarget

    @property
    def time_signature(self):
        '''The default time signature.'''
        return self._time_signature

    @property
    def use_full_measure(self):
        '''The full-measure-as-beatspan default.'''
        return self._use_full_measure
