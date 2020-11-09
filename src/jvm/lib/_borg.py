# Alex Martelli's 'Borg' singleton implementation:
# http://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html#id1
#
# Modified (and a bit improved/enhanced) by Adam Karpierz, 2014

__all__ = ('Borg',)


class Borg:

    __shared_state = {}

    def __new__(cls, *args, **kargs):
        self = super().__new__(cls)
        self.__dict__ = Borg.__shared_state
        return self
