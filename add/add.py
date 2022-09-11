from sqlalchemy.orm import sessionmaker

from engine.engine import MAIN_ENGINE
from tables.professional.user import User


class Add:
    @staticmethod
    def add(handling_class, content):
        session = sessionmaker(bind=MAIN_ENGINE)()
        session.add(handling_class(**content))
        session.commit()
        session.close()

    # def delete_by_column(self, column_name, value):
    #     self.session.query(User).filter(getattr(self.handling_class, column_name) == value).delete()
    #     self.session.commit()


# # q.delete_by_column('zone', 'Foo')
# agg = q.aggregate_by_column('zone')
# print(agg)
