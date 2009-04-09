from abjad.helpers.assess_components import assess_components
from abjad.tools.tietools.is_chain import is_chain


def is_in_same_parent(expr):
   r'''True when expr is a tie chain with all leaves in same parent.
      IE, True when tie chain crosses no container boundaries.
      Otherwise False.

      Example:

      t = Staff(RigidMeasure((2, 8), run(2)) * 2)
      Tie(t.leaves[1:3])

      \new Staff {
            \time 2/8
            c'8
            c'8 ~
            \time 2/8
            c'8
            c'8
      }

      assert tietools.is_in_same_parent(t.leaves[0].tie.chain)
      assert not tietools.is_in_same_parent(t.leaves[1].tie.chain)
      assert not tietools.is_in_same_parent(t.leaves[2].tie.chain)
      assert tietools.is_in_same_parent(t.leaves[3].tie.chain)'''

   return is_chain(expr) and \
      assess_components(list(expr), share = 'parent')
