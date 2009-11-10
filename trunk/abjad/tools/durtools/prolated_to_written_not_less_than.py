from abjad.rational import Rational
from abjad.tools import mathtools
from abjad.tools.durtools.is_assignable import is_assignable as \
   durtools_is_assignable
from abjad.tools.durtools.naive_prolated_to_written_not_less_than \
   import naive_prolated_to_written_not_less_than \
   as durtools_naive_prolated_to_written_not_less_than
import math


def prolated_to_written_not_less_than(prolated_duration):
   '''Return the greatest note-head-assignabel rational not
   less than `prolated_duration`. ::

      abjad> for n in range(1, 17):
      ...     prolated = Rational(n, 16)
      ...     written = durtools.prolated_to_written_not_less_than(prolated)
      ...     print '%s/16\\t%s' % (n, written)
      ... 
      1/16    1/16
      2/16    1/8
      3/16    3/16
      4/16    1/4
      5/16    3/8
      6/16    3/8
      7/16    7/16
      8/16    1/2
      9/16    3/4
      10/16   3/4
      11/16   3/4
      12/16   3/4
      13/16   7/8
      14/16   7/8
      15/16   15/16
      16/16   1

   .. note:: this function returns dotted and double dotted durations
      where possible.

   .. versionchanged:: 1.1.2
      Fixed to produce monotonically increasing output in response
      to monotonically increasing input.
   '''

#   if durtools_is_assignable(prolated_duration):
#      return prolated_duration
#   else:
#      return durtools_naive_prolated_to_written_not_less_than(
#         prolated_duration)

   good_denominator = mathtools.greatest_power_of_two_less_equal(
      prolated_duration._d)
   #print good_denominator

   cur_numerator = prolated_duration._n
   candidate = Rational(cur_numerator, good_denominator)

   while not durtools_is_assignable(candidate):
      #print cur_numerator
      cur_numerator += 1
      candidate = Rational(cur_numerator, good_denominator)

   return candidate
