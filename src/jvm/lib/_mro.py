
__all__ = ('mro',)

from itertools import count


def mro(cls):
    # Find a superclass linearization that honors the constraints
    # of the explicit lists of bases and the constraints implied by
    # each base class.
    #
    # to_merge is a list of lists, where each list is a superclass
    # linearization implied by a base class.
    # The last element of to_merge is the declared list of bases.

    # This is just a basic sanity check.
    _check_duplicates(cls.__bases__)

    to_merge = [(bcls.__mro__ if isinstance(bcls, type) else classic_mro(bcls))  # noqa: F821 # !!!
                for bcls in cls.__bases__]
    to_merge.append(cls.__bases__)

    result = [cls]
    _merge(result, to_merge)
    return result


def _merge(result, to_merge):
    # remain stores an index into each sublist of to_merge.
    # remain[i] is the index of the next base in to_merge[i]
    # that is not included in result.

    remain = [0] * len(to_merge)

    again = True
    while again:
        again = False

        empty_cnt = 0

        for cseq, rem in zip(to_merge, remain):
            if rem >= len(cseq):
                empty_cnt += 1
            else:
                # Choose next candidate for MRO.
                #
                # The input sequences alone can determine the choice.
                # If not, choose the class which appears in the MRO
                # of the earliest direct superclass of the new class.
                #
                candidate = cseq[rem]
                for cseq_nxt, rem_nxt in zip(to_merge, remain):
                    if any((cseq_nxt[k] is candidate) for k in range(rem_nxt+1, len(cseq_nxt))):
                        break  # continue outer loop
                else:
                    result.append(candidate)
                    for cseq_nxt, rem_nxt, i in zip(to_merge, remain, count()):
                        if rem_nxt < len(cseq_nxt) and cseq_nxt[rem_nxt] is candidate:
                            remain[i] += 1
                    again = True
                    break

    if empty_cnt != len(to_merge):
        classes = {cseq[rem] for cseq, rem in zip(to_merge, remain) if rem < len(cseq)}
        msg  = "Cannot create a consistent method resolution\norder (MRO) for bases"
        msg += ",".join(" {}".format(_class_name(cls) or "?") for cls in classes)
        raise TypeError(msg)


def _check_duplicates(seq):
    size = len(seq)
    for i, cls in enumerate(seq):
        for j in range(i+1, size):
            if seq[j] == cls:
                raise TypeError("duplicate base class {}".format(_class_name(cls) or "?"))


def _class_name(cls):
    try:
        name = getattr(cls, "__name__", repr(cls))
        return name if isinstance(name, str) and name else None
    except Exception:
        return None
