from tagstr_site import Thunk


def _f(): pass


CodeType = type(_f.__code__)


def memoization_key(*args: str | Thunk) -> tuple[str | tuple[CodeType], ...]:
    bits = []
    for arg in args:
        if isinstance(arg, str):
            bits.append(arg)
        else:
            kode: CodeType = arg[0].__code__
            bits.append((kode,))
    return tuple(bits)


def make_greet_tag(*args: str | Thunk) -> str:
    """Use caching of templates in greeting."""
    result = []
    for arg in args:
        match arg:
            case str():
                result.append(arg)
            case getvalue, _, _, _:
                result.append(getvalue())
            case gv:
                gv_ = gv[0]()
                result.append(gv_)

    return f"{''.join(result)}!"


def greet2(*args: str | Thunk) -> str:
    """The actual greet tag, as a cache-oriented wrapper."""
    cache_key = memoization_key(*args)
    return make_greet_tag(*args)
