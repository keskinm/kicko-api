from sqlalchemy.orm import sessionmaker

from engine.engine import MAIN_ENGINE
from tables.professional.user import User


class Add:
    def __init__(self, handling_class=User):
        self.session = sessionmaker(bind=MAIN_ENGINE)()
        self.handling_class = handling_class

    def add(self, handling_class, content):
        self.session.add(handling_class(**content))
        self.session.commit()

    # def delete_by_column(self, column_name, value):
    #     self.session.query(User).filter(getattr(self.handling_class, column_name) == value).delete()
    #     self.session.commit()


# # q.delete_by_column('zone', 'Foo')
# agg = q.aggregate_by_column('zone')
# print(agg)

