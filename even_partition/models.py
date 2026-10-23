from collections import namedtuple


class PartitionResult(namedtuple("PartitionResultBase", "edges cost")):
    __slots__ = ()

    @property
    def edge_count(self):
        return len(self.edges)
