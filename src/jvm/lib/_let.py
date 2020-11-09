# Copyright (c) 2016 Taylor Marks
# Copyright (c) 2016-2020 Adam Karpierz
# Licensed under the MIT License
# https://opensource.org/licenses/MIT

import sys

__all__ = ('let',)


def let(**name_value_pair):
    """Takes in a single name = value pair.
    The value is assigned to the name and returned.
    This is useful in if statements, while loops, and anyplace else
    where you want to both assign and use a value.

    Examples:

    Instead of:

        name = longInstanceName.longAttributeName
        if name:
            ...

    - Or worse, using that long identifier in the condition and then
    repeatedly in the body - you can use this:

        if let(name = longInstanceName.longAttributeName):
            ...

    Instead of:

        results = dbConnection.fetch_results():
        while results:
            ...
            results = dbConnection.fetch_results()

    You can do this:

        while let(results = dbConnection.fetch_results):
            ...

    Instead of:

        if len(sequence) != 1:
            raise Exception('Bad amount: {}'.format(len(sequence)))

    You could use:

        if let(count = len(sequence)) != 1:
            raise Exception('Bad amount: {}'.format(count))
    """
    count = len(name_value_pair)
    if count != 1:
        raise TypeError("let() takes exactly one key = value pair ({} given)"
                        .format(count))

    frame = sys._getframe(1)

    name, value = next(iter(name_value_pair.items()))
    if name in frame.f_locals:
        raise Exception("{} has already been locally assigned. "
                        "Due to optimizations in the Python interpreter, "
                        "it is not possible to write over it using let(). "
                        "Sorry!".format(name))

    frame.f_globals[name] = value
    return value
