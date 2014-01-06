# -*- encoding: utf-8 -*-
from abjad.tools.lilypondfiletools.Block import Block


class HeaderBlock(Block):
    r'''Abjad model of LilyPond input file header block:

    ::

        >>> header_block = lilypondfiletools.HeaderBlock()

    ::

        >>> header_block
        HeaderBlock()

    ::

        >>> header_block.composer = markuptools.Markup('Josquin')
        >>> header_block.title = markuptools.Markup('Missa sexti tonus')

    ..  doctest::

        >>> print format(header_block)
        \header {
            composer = \markup { Josquin }
            title = \markup { Missa sexti tonus }
        }

    Returns header block.
    '''

    def __init__(self):
        Block.__init__(self)
        self._escaped_name = r'\header'
