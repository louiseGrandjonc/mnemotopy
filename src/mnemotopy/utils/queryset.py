def queryset_to_dict(qs, key='pk'):
    """
    Given a queryset will transform it into a dictionary based on ``key``.
    """
    result = {}
    for u in qs:
        result.setdefault(getattr(u, key), u)

    return result
