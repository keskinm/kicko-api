from sqlalchemy.orm import sessionmaker

from engine.engine import MAIN_ENGINE


def delete_row(handling_class, filters):
    session = sessionmaker(bind=MAIN_ENGINE)()
    session.query(handling_class).filter(filters).delete()
    session.commit()
    session.close()


def add_row(handling_class, content):
    session = sessionmaker(bind=MAIN_ENGINE)()
    session.add(handling_class(**content))
    session.commit()
    session.close()


def make_query(handling_class, filters=None):
    session = sessionmaker(bind=MAIN_ENGINE)()
    query_result = session.query(handling_class).filter(filters)
    session.close()
    return query_result


def row_to_dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d


# def unique(self, column_name):
#     providers_table = self.session.query(User).filter()
#     zones = list(map(lambda x: getattr(x, column_name), list(providers_table)))
#     zones = list(dict.fromkeys(zones))
#     return zones
#
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