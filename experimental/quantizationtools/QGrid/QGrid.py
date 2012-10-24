import bisect
import copy
import inspect
from abjad.tools import containertools
from abjad.tools import durationtools
from abjad.tools import marktools
from abjad.tools.abctools import AbjadObject


class QGrid(AbjadObject):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_next_downbeat', '_root_node')

    ### INITIALIZATION ###

    def __init__(self, root_node=None, next_downbeat=None):
        from experimental import quantizationtools

        if root_node is None:
            root_node = quantizationtools.QGridLeaf(1)
        assert isinstance(root_node,
            (quantizationtools.QGridLeaf, quantizationtools.QGridContainer))

        if next_downbeat is None:
            next_downbeat = quantizationtools.QGridLeaf(1)
        assert isinstance(next_downbeat, quantizationtools.QGridLeaf)

        self._root_node = root_node
        self._next_downbeat = next_downbeat
        self._next_downbeat._offset = durationtools.Offset(1)
        self._next_downbeat._offsets_are_current = True

    ### SPECIAL METHODS ###

    def __call__(self, beatspan):
        result = self.root_node(beatspan)
        result_leaves = []
        for x in result:
            if isinstance(x, containertools.Container):
                result_leaves.extend(x.leaves)
            else:
                result_leaves.append(x)
        for result_leaf, q_grid_leaf in zip(result_leaves, self.leaves[:-1]):
            if q_grid_leaf.q_event_proxies:
                q_events = [q_event_proxy.q_event for q_event_proxy in q_grid_leaf.q_event_proxies]
                q_events.sort(key=lambda x: x.index)
                marktools.Annotation('q_events', tuple(q_events))(result_leaf)
        return result

    def __copy__(self, *args):
        return self.__deepcopy__(None)

    def __deepcopy__(self, memo):
        root_node, next_downbeat = self.__getnewargs__()
        return type(self)(copy.copy(root_node), copy.copy(next_downbeat))

    def __eq__(self, other):
        if type(self) == type(other):
            if self.root_node == other.root_node:
                if self.next_downbeat == other.next_downbeat:
                    return True
        return False

    def __getnewargs__(self):
        return (self.root_node, self.next_downbeat)

    def __getstate__(self):
        return {
            '_next_downbeat': self.next_downbeat,
            '_root_node': self.root_node,
        }

    def __setstate__(self, state):
        self._next_downbeat = state['_next_downbeat']
        self._root_node = state['_root_node']

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def leaves(self):
        '''All of the leaf nodes in the QGrid, includeing the next downbeat's node.'''
        from experimental import quantizationtools
        if isinstance(self._root_node, quantizationtools.QGridLeaf):
            return (self._root_node, self._next_downbeat)
        return self._root_node.leaves + (self._next_downbeat,)

    @property
    def next_downbeat(self):
        '''The node representing the "next" downbeat after the contents
        of the QGrid's tree.
        '''
        return self._next_downbeat

    @property
    def distance(self):
        count = 0
        absolute_distance = 0
        for leaf, offset in zip(self.leaves, self.offsets):
            for q_event_proxy in leaf.q_event_proxies:
                absolute_distance += abs(q_event_proxy.offset - offset)
                count += 1
        if count:
            return absolute_distance / count
        return None

    @property
    def offsets(self):
        '''The offsets between 0 and 1 of all of the leaf nodes in the QGrid.'''
        return tuple([x.start_offset for x in self.leaves[:-1]] + [durationtools.Offset(1)])

    @property
    def root_node(self):
        return self._root_node

    ### PUBLIC METHODS ###

    def fit_q_events(self, q_event_proxies):
        from experimental import quantizationtools
        assert all([isinstance(x, quantizationtools.QEventProxy) for x in q_event_proxies])
        leaves, offsets = self.leaves, self.offsets
        for q_event_proxy in q_event_proxies:
            idx = bisect.bisect_left(offsets, q_event_proxy.offset)
            if q_event_proxy.offset == offsets[idx]:
                leaves[idx].q_event_proxies.append(q_event_proxy)
            else:
                left, right = offsets[idx - 1], offsets[idx]
                left_diff = abs(left - q_event_proxy.offset)
                right_diff = abs(right - q_event_proxy.offset)
                if right_diff < left_diff:
                    leaves[idx].q_event_proxies.append(q_event_proxy)
                else:
                    leaves[idx - 1].q_event_proxies.append(q_event_proxy)

    def sort_q_events_by_index(self):
        for leaf in self.leaves:
            leaf.q_event_proxies.sort(key=lambda x: x.index)

    def subdivide_leaf(self, leaf, subdivisions):
        from experimental import quantizationtools
        container = quantizationtools.QGridContainer(
            leaf.duration, [
                quantizationtools.QGridLeaf(subdivision) for subdivision in subdivisions
            ])
        if leaf.parent is not None:
            index = leaf.parent.index(leaf)
            leaf.parent[index] = container
        else: # otherwise, our root node is just a QGridLeaf
            self._root_node = container
        return leaf.q_event_proxies

    def subdivide_leaves(self, pairs):
        pairs = sorted(dict(pairs).items())
        leaf_indices = [pair[0] for pair in pairs]
        subdivisions = [pair[1] for pair in pairs]

        all_leaves = self.leaves
        leaves_to_subdivide = [all_leaves[idx] for idx in leaf_indices]

        q_event_proxies = []
        for i, leaf in enumerate(leaves_to_subdivide):

            next_leaf = all_leaves[all_leaves.index(leaf) + 1]
            if next_leaf is self.next_downbeat:
                next_leaf_offset = durationtools.Offset(1)
            else:
                next_leaf_offset = next_leaf.start_offset
            
            q_event_proxies.extend(self.subdivide_leaf(leaf, subdivisions[i]))
            for q_event_proxy in tuple(next_leaf.q_event_proxies):
                if q_event_proxy.offset < next_leaf_offset:
                    idx = next_leaf.q_event_proxies.index(q_event_proxy)
                    q_event_proxies.append(next_leaf.q_event_proxies.pop(idx))

        return q_event_proxies
