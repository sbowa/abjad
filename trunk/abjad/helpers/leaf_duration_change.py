from abjad.exceptions.exceptions import AssignabilityError
from abjad.helpers.check import check
from abjad.helpers.withdraw_from_contained_spanners import \
   _withdraw_from_contained_spanners
from abjad.leaf.leaf import _Leaf
from abjad.rational.rational import Rational
from abjad.tie.spanner import Tie
from abjad.tools import construct
from abjad.tuplet.fm.tuplet import FixedMultiplierTuplet

   
def leaf_duration_change(leaf, new_written_duration):
   '''Change the written duration of leaf, splicing tied notes
      for nonassignable durations like 5/16.

      Return list of all modified and new leaves.'''

   assert isinstance(leaf, _Leaf)
   assert isinstance(new_written_duration, Rational)

   try:
      leaf.duration.written = new_written_duration  
      all_leaves = [leaf]
   except AssignabilityError:
      duration_tokens = construct.notes(0, new_written_duration)
      if isinstance(duration_tokens[0], _Leaf):
         num_tied_leaves = len(duration_tokens) - 1
         tied_leaves = leaf * num_tied_leaves
         _withdraw_from_contained_spanners(tied_leaves)
         all_leaves = [leaf] + tied_leaves
         for x, token in zip(all_leaves, duration_tokens):
            x.duration.written = token.duration.written
         leaf.splice(tied_leaves)
         if not leaf.tie.spanned:
            Tie(all_leaves)
      elif isinstance(duration_tokens[0], FixedMultiplierTuplet):
         fmtuplet = duration_tokens[0]
         duration_tokens = fmtuplet[:]
         num_tied_leaves = len(duration_tokens) - 1
         tied_leaves = leaf * num_tied_leaves
         _withdraw_from_contained_spanners(tied_leaves)
         all_leaves = [leaf] + tied_leaves
         for x, token in zip(all_leaves, duration_tokens):
            x.duration.written = token.duration.written
         leaf.splice(tied_leaves)
         if not leaf.tie.spanned:
            Tie(all_leaves) 
         tuplet_multiplier = fmtuplet.duration.multiplier
         FixedMultiplierTuplet(tuplet_multiplier, all_leaves)
      else:
         raise ValueError('unexpected output from construct.notes.')

   return all_leaves
