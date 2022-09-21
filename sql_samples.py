def many_to_many():
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker, relationship
    from sqlalchemy import Table, Column, ForeignKey, Integer, create_engine, String

    Base = declarative_base()
    draft_engine = create_engine("sqlite:///draft_engine", echo=True)

    # association_table = Table(
    #     "association",
    #     Base.metadata,
    #     Column("left_id", ForeignKey("left.id"), primary_key=True),
    #     Column("right_id", ForeignKey("right.id"), primary_key=True),
    # )
    #
    #
    # class Parent(Base):
    #     __tablename__ = "left"
    #     id = Column(Integer, primary_key=True)
    #     children = relationship("Child", secondary="association", backref="parents")
    #
    #
    # class Child(Base):
    #     __tablename__ = "right"
    #     id = Column(Integer, primary_key=True)
    #
    #
    # Base.metadata.create_all(draft_engine)
    #
    Session = sessionmaker(bind=draft_engine)
    session = Session()
    # session.add(Parent())
    # b = session.query(Parent).filter().first()
    # r = list(session.query(Child).filter())
    # session.close()

    student_identifier = Table('student_identifier',
                                  Column('class_id', Integer, ForeignKey('classes.class_id')),
                                  Column('user_id', Integer, ForeignKey('students.user_id'))
                                  )

    class Student(Model):
        __tablename__ = 'students'
        user_id = Column(Integer, primary_key=True)
        user_fistName = Column(String(64))
        user_lastName = Column(String(64))
        user_email = Column(String(128), unique=True)

    class Class(Base):
        __tablename__ = 'classes'
        class_id = Column(Integer, primary_key=True)
        class_name = Column(String(128), unique=True)
        students = relationship("Student",
                                   secondary=student_identifier)

    s = Student()
    c = Class()
    c.students.append(s)
    session.add(c)
    session.commit()


many_to_many()

