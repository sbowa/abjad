from abjad.tools.abctools.ImmutableAbjadObject import ImmutableAbjadObject


class Ratio(ImmutableAbjadObject, tuple):
    '''.. versionadded:: 2.10

    Ratio of two or more nonzero integers.

    Initialize from one or more nonzero integers::

        >>> mathtools.Ratio(2, 4, 2)
        Ratio(1, 2, 1)

    Or initialize from a tuple or list::

        >>> ratio = mathtools.Ratio((2, 4, 2))
        >>> ratio
        Ratio(1, 2, 1)

    Use a tuple to return ratio integers.

        >>> tuple(ratio)
        (1, 2, 1)

    Ratios are immutable.
    '''

    ### INITIALIZER ###

    def __new__(klass, *args):
        from abjad.tools import sequencetools
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            args = args[0]
        assert args, repr(args)
        assert all([x != 0 for x in args]), repr(args) 
        args = sequencetools.divide_sequence_elements_by_greatest_common_divisor(args)
        self = tuple.__new__(klass, args)
        return self

    ### SPECIAL METHODS ###

    def __eq__(self, other):
        other = type(self)(other)
        return tuple(self) == tuple(other)
        
    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _mandatory_argument_values(self):
        return tuple(self)

    ### PRIVATE METHODS ###

    # do not indent in storage
    def _get_tools_package_qualified_repr_pieces(self, is_indented=True):
        return [''.join(
            ImmutableAbjadObject._get_tools_package_qualified_repr_pieces(self, is_indented=False))]
