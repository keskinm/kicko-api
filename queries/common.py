from sqlalchemy.orm import sessionmaker

from engine.engine import MAIN_ENGINE


def delete_row(handling_class, filters):
    session = sessionmaker(bind=MAIN_ENGINE)()
    session.query(handling_class).filter(*filters).delete()
    session.commit()
    session.close()


def add_row(handling_class, content):
    session = sessionmaker(bind=MAIN_ENGINE)()
    session.add(handling_class(**content))
    session.commit()
    session.close()


def make_query(handling_class, filters=None, end_session=True):
    session = sessionmaker(bind=MAIN_ENGINE)()
    if filters is not None:
        query_result = session.query(handling_class).filter(filters)
    else:
        query_result = session.query(handling_class).filter()
    if not end_session:
        return query_result, session
    else:
        session.close()
        return query_result


def row_to_dict(row):
    d = {}
    for column in row.__table__.columns:
        v = getattr(row, column.name)
        if v is not None:
            if column.name.endswith("id"):
                v = str(v)
            d[column.name] = v
    return d


def replace(session, table_row, fields):
    for key, value in fields.items():
        setattr(table_row, key, value)
    session.commit()
    session.close()


def unique(handling_class, column_name, filters=None):
    session = sessionmaker(bind=MAIN_ENGINE)()
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


# def aggregate_by_column(self, column_name, selection=None):
#     unique_column = self.unique(column_name)
#
#     aggregated = {}
#     for item in unique_column:
#         item_aggregated_list = list(self.session.query(User).filter(getattr(self.handling_class, column_name) == item))
#         if selection:
#             item_aggregated_list = list(map(lambda x: getattr(x, selection), item_aggregated_list))
#         aggregated.update({item: item_aggregated_list})
#
#     return aggregated
