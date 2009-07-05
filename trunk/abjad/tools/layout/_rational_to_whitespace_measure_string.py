from abjad.measure import RigidMeasure
from abjad.skip import Skip
from abjad.tools import measuretools


def _rational_to_whitespace_measure_string(duration):
   '''Turn rational into whitespace measure string.'''

   ## make measure with hidden staff and hidden time signature
   measure = measuretools.make([duration])[0]
   measure.meter.stencil = False
   measure.meter.promote('stencil', 'Staff')
   measure.staff.hide = True

   ## return measure string
   return measure.format
