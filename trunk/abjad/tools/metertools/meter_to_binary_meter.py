from abjad.tools import durtools
from abjad.tools import contexttools
from abjad.tools import mathtools
from abjad.tools.metertools.Meter import Meter
from fractions import Fraction


def meter_to_binary_meter(nonbinary_meter, contents_multiplier = Fraction(1)):
   '''Change nonbinary `meter` to binary meter::

      abjad> metertools.meter_to_binary_meter(Meter(3, 12))
      Meter(2, 8)

   Preserve binary `meter`::

      abjad> metertools.meter_to_binary_meter(metertools.Meter(2, 8))
      Meter(2, 8)

   Return newly constructed meter.

   .. versionchanged:: 1.1.2
      renamed ``metertools.make_binary( )`` to
      ``metertools.meter_to_binary_meter( )``.
   '''
   
   ## check input
   assert isinstance(nonbinary_meter, (Meter, contexttools.TimeSignatureMark))
   assert isinstance(contents_multiplier, Fraction)

   ## save nonbinary meter and denominator
   nonbinary_denominator = nonbinary_meter.denominator

   ## find binary denominator
   if contents_multiplier == Fraction(1):
      binary_denominator = mathtools.greatest_power_of_two_less_equal(nonbinary_denominator)
   else:
      binary_denominator = mathtools.greatest_power_of_two_less_equal(nonbinary_denominator, 1)

   ## find binary pair
   nonbinary_pair = (nonbinary_meter.numerator, nonbinary_meter.denominator)
   binary_pair = durtools.rational_to_duration_pair_with_specified_integer_denominator(
      nonbinary_pair, binary_denominator)

   ## return new binary meter
   return Meter(*binary_pair)
