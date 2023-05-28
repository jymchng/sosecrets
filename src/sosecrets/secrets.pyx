#cython: language_level=3

from libc.stdlib cimport free

cdef class Secret:

    cdef object inner_secret
    cdef readonly int expose_count
    cdef public int max_expose_count

    def __cinit__(self, object value=None, object func=None, int max_expose_count=-1, tuple func_args=(), dict func_kwargs={}):
        if func is not None:
            self.inner_secret = func(*func_args, **func_kwargs)
        if func is not None and value is not None:
            raise ValueError("`Secret` cannot be initialized with both `value` positional argument and `func` keyword")
        else:
            self.inner_secret = value
        self.expose_count = 0
        self.max_expose_count = max_expose_count

    cpdef object expose_secret(self):
        if self.max_expose_count != -1:
            if self.expose_count < self.max_expose_count:
                self.expose_count += 1
                return self.inner_secret
            else:
                raise AttributeError('`Secret` cannot be exposed more than {} times'.format(self.max_expose_count))
        else:
            self.expose_count += 1
            return self.inner_secret

    cpdef Secret apply(self, object func, tuple func_args, dict func_kwargs):
        return Secret(func(self.expose_secret(), *func_args, **func_kwargs))

    