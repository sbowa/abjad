from abc import ABCMeta
from abc import abstractmethod
from abjad.tools import containertools
from abjad.tools import leaftools
from abjad.tools import voicetools
from abjad.tools.abctools.AbjadObject import AbjadObject


class Selector(AbjadObject):
    r'''.. versionadded:: 1.0

    Abstract base class from which all selectors inherit.
    '''

    ### INITIALIZER ###

    @abstractmethod
    def __init__(self):
        pass

    ### PRIVATE METHODS ###

    def _interprets_as_sliceable_selector(self, expr):
        from experimental import selectortools
        # voices are sliceable
        if isinstance(expr, (voicetools.Voice, str)):
            return True
        # slice selectors are sliceable
        elif isinstance(expr, selectortools.SliceSelector):
            return True
        # counttime container item selectors are sliceable
        elif isinstance(expr, Selector) and issubclass(expr.klass, containertools.Container):
            return True
        # nothing else is sliceable
        else:
            return False

    def _reference_to_storable_form(self, reference):
        if isinstance(reference, voicetools.Voice):
            return reference.name
        else:
            return reference

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def timespan(self):
        '''Timespan of selector.

        Return timespan object.
        '''
        from experimental import timespantools
        return timespantools.Timespan(selector=self)
