from sqlalchemy.orm import sessionmaker

from engine.engine import MAIN_ENGINE
from tables.professional.user import User


class Queries:
    def __init__(self, handling_class=User):
        self.session = sessionmaker(bind=MAIN_ENGINE)()
        self.handling_class = handling_class

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

    def get(self, handling_class):
        user = self.session.query(handling_class).filter()
        d = (list(user))
        return d

    # def delete_by_column(self, column_name, value):
    #     self.session.query(User).filter(getattr(self.handling_class, column_name) == value).delete()
    #     self.session.commit()

# q = Queries()
# # q.delete_by_column('zone', 'Foo')
# agg = q.aggregate_by_column('zone')
# print(agg)
