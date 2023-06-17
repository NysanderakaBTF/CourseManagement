from datetime import datetime

from sqlalchemy.orm import class_mapper


def serialize(model):
    columns = [c.key for c in class_mapper(model.__class__).columns]
    dic = {}
    dict((c, getattr(model, c)) for c in columns)
    for c in columns:
        if isinstance(c, datetime):
            dic[c] = getattr(model, c).isoformat()
        else:
            dic[c] = getattr(model, c)
    return dic

def datetime_handler(x):
    if isinstance(x, datetime):
        return x.isoformat()
    raise TypeError("Unknown type")
