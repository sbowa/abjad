from abjad.rational import Rational
from abjad.tools import mathtools
from abjad.tools.listtools.cumulative_sums import cumulative_sums as \
   listtools_cumulative_sums
from abjad.tools.listtools.flatten import flatten as listtools_flatten
from abjad.tools.listtools.weight import weight as listtools_weight


def partition_by_weights_ratio(l, ratio):
   '''.. versionadded:: 1.1.2

   Partition list `l` into disjunct parts such that propotions of 
   the weights of the parts equal the proportions in `ratio`
   with some rounding magic. ::

      abjad> l = [1] * 10
      abjad> listtools.partition_by_weights_ratio(l, [1, 1, 1])
      [[1, 1, 1], [1, 1, 1, 1], [1, 1, 1]]

   ::

      abjad> listtools.partition_by_weights_ratio(l, [1, 1, 1, 1])
      [[1, 1, 1], [1, 1], [1, 1, 1], [1, 1]]

   ::

      abjad> listtools.partition_by_weights_ratio(l, [2, 2, 3])
      [[1, 1, 1], [1, 1, 1], [1, 1, 1, 1]]

   ::

      abjad> listtools.partition_by_weights_ratio(l, [3, 2, 2])
      [[1, 1, 1, 1], [1, 1, 1], [1, 1, 1]]
   '''

   weight = listtools_weight(l)
   weights = mathtools.partition_integer_by_ratio(weight, ratio)
   cumulative_weights = listtools_cumulative_sums(weights)

   result = [ ]
   sublist = [ ]
   result.append(sublist)
   cur_cumulative_weight = cumulative_weights.pop(0)
   for n in l:
      if not isinstance(n, (int, long, float, Rational)):
         raise TypeError('must be number.')
      sublist.append(n)
      while cur_cumulative_weight <= \
         listtools_weight(listtools_flatten(result)):
         try:
            cur_cumulative_weight = cumulative_weights.pop(0)
            sublist = [ ]
            result.append(sublist)
         except IndexError:
            break

   return result
