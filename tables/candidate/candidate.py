import enum

from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.orm import relationship

from engine.base import Base
from tables.associations.associations import job_offer_candidate_association


class Sex(enum.Enum):
    null = ""
    male = "Homme"
    female = "Femme"
    non_binary = "Non genré"


class StudyLevel(enum.Enum):
    null = ""
    bachelor_degree = "Licence"
    master_degree = "Master"


enums_to_module = {"sex": Sex, "study_level": StudyLevel}
enums_values = {k: [v.value for v in module] for k, module in enums_to_module.items()}


class Candidate(Base):
    __tablename__ = "candidate"

    id = Column(Integer, primary_key=True, unique=True)
    firebase_id = Column(String, unique=True)
    username = Column(String, unique=True)
    password = Column(String)
    email = Column(String(100), unique=True)
    country = Column(String)
    zone = Column(String)
    phone_number = Column(String)
    study_level = Column(Enum(StudyLevel))
    sex = Column(Enum(Sex))

    image_id = Column(String)
    resume_id = Column(String)

    job_offers = relationship(
        "JobOffers",
        secondary=job_offer_candidate_association,
        back_populates="candidate",
    )

    def __init__(
        self,
        firebase_id,
        username,
        password,
        email,
        country=None,
        zone=None,
        phone_number=None,
        study_level=StudyLevel.null,
        sex=Sex.null,
        image_id=None,
        resume_id=None,
    ):
        self.firebase_id = firebase_id
        self.username = username
        self.password = password
        self.email = email
        self.country = country
        self.zone = zone
        self.phone_number = phone_number

        self.study_level = study_level
        self.sex = sex

        self.image_id = image_id
        self.resume_id = resume_id
