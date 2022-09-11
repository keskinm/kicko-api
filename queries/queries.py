from sqlalchemy.orm import sessionmaker

from engine.engine import MAIN_ENGINE
from tables.professional.user import User


class Queries:
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

    @staticmethod
    def make_query(handling_class, filters=None):
        session = sessionmaker(bind=MAIN_ENGINE)()
        query_result = session.query(handling_class).filter(filters)
        session.close()
        return query_result

    @staticmethod
    def delete_by_column(handling_class, column_name, value):
        session = sessionmaker(bind=MAIN_ENGINE)()
        session.query(handling_class).filter(
            getattr(handling_class, column_name) == value
        ).delete()
        session.commit()
        session.close()

    @staticmethod
    def row_to_dict(row):
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))
        return d


# q = Queries()
# q.delete_by_column(User, "email", "toto44@gmail.com")
# r = (q.make_query(User, User.email=="toto7@gmail.com"))
# print("R", r)

# # q.delete_by_column('zone', 'Foo')
# agg = q.aggregate_by_column('zone')
# print(agg)
