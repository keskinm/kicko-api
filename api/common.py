"""Common query methods."""

import enum

from database.database import SessionLocal


def delete_row(handling_class, filters):
    """Delete rows based on filter."""
    session = SessionLocal()
    session.query(handling_class).filter(*filters).delete()
    session.commit()
    session.close()


def add_row(handling_class, content, end_session=True):
    """Add instance."""
    session = SessionLocal()
    instance = handling_class(**content)
    session.add(instance)
    session.commit()
    if not end_session:
        return instance, session
    session.close()
    return instance


def make_query(handling_class, filters=None, end_session=True, session=None):
    """Perform a query."""
    session = session or SessionLocal()
    if filters is not None:
        query_result = session.query(handling_class).filter(filters)
    else:
        query_result = session.query(handling_class).filter()
    if not end_session:
        return query_result, session
    session.close()
    return query_result


def row_to_dict(row):
    """Transform an instance to dict."""
    d = {}
    for column in row.__table__.columns:
        v = getattr(row, column.name)
        if v is not None:
            if column.name.endswith("id"):
                v = str(v)
            if isinstance(v, enum.Enum):
                v = v.value
            d[column.name] = v
    return d


def replace(session, table_row, fields):
    """Update instance fields."""
    for key, value in fields.items():
        setattr(table_row, key, value)
    session.commit()
    session.close()


def unique(handling_class, column_name, filters=None):
    """Get all unique instances column value(remove duplicates)."""
    session = SessionLocal()
    if filters is not None:
        providers_table = session.query(handling_class).filter(filters)
    else:
        providers_table = session.query(handling_class).filter()
    _list = list(map(lambda x: getattr(x, column_name), list(providers_table)))
    _unique = list(dict.fromkeys(_list))
    if column_name.endswith("id"):
        _unique = [str(v) for v in _unique]
    session.close()
    return _unique
