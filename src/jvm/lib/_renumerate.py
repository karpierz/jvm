# Copyright (c) 2016 Adam Karpierz
# SPDX-License-Identifier: Zlib

__all__ = ('renumerate',)


def renumerate(sequence, start=None, end=None):
    """Reverse iterator for index, value of sequence.

    renumerate(sequence[, start]|[, end]) -> reverse iterator

    Return an enumerate object.  sequence must be another object that has a
    __reversed__() method or supports the sequence protocol (the __len__()
    method and the __getitem__() method with integer arguments starting at 0).
    The enumerate object yields pairs containing a count (from start, which
    defaults to len(sequence) - 1 or ends at end, which defaults to zero - but
    not both) and a value yielded by the sequence argument in reverse order.
    renumerate is useful for obtaining an indexed list in reverse order:
        (2, seq[2]), (1, seq[1]), (0, seq[0]), ...
    """
    if start is not None and end is not None:
        raise TypeError("renumerate() only accepts start argument or "
                        "end argument - not both.")
    if start is None:
        start = len(sequence) - 1
    if end is None:
        end = 0
    return ((-idx, elem) for idx, elem in enumerate(reversed(sequence),
                                                    start=-(start + end)))
