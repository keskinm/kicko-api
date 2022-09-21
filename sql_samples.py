import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Table, Column, ForeignKey, Integer, create_engine, String


def test_many_to_many():
    Class, Student, session = many_to_many()
    s = Student()
    c = Class()
    session.add(c)
    session.add(s)
    session.commit()
    class_sample = session.query(Class).filter().one()
    student_sample = session.query(Student).filter().one()
    class_sample.students.append(student_sample)
    assert len(student_sample.classes) == 1
    assert len(class_sample.students) == 1
    session.close()
    #  -----------------------------------------------------
    Class, Student, session = many_to_many()
    s = Student()
    c = Class()
    c.students.append(s)
    session.add(c)
    session.commit()
    class_sample = session.query(Class).one()
    student_sample = session.query(Student).one()

    assert len(student_sample.classes) == 1
    assert len(class_sample.students) == 1
    session.close()


def many_to_many():
    Base = declarative_base()
    if os.path.exists("draft_engine"):
        os.remove("draft_engine")
    draft_engine = create_engine("sqlite:///draft_engine", echo=True)
    Session = sessionmaker(bind=draft_engine)
    session = Session()
    student_identifier = Table(
        "student_identifier",
        Base.metadata,
        Column("class_id", Integer, ForeignKey("classes.class_id")),
        Column("user_id", Integer, ForeignKey("students.user_id")),
    )

    class Student(Base):
        __tablename__ = "students"
        user_id = Column(Integer, primary_key=True)
        user_fistName = Column(String(64))
        user_lastName = Column(String(64))
        user_email = Column(String(128), unique=True)
        classes = relationship(
            "Class", secondary=student_identifier, back_populates="students"
        )

    class Class(Base):
        __tablename__ = "classes"
        class_id = Column(Integer, primary_key=True)
        class_name = Column(String(128), unique=True)
        students = relationship(
            "Student", secondary=student_identifier, back_populates="classes"
        )

    Base.metadata.create_all(draft_engine)
    return Class, Student, session

# test_many_to_many()

