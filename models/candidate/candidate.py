import enum

from sqlalchemy import Column, Enum, String
from sqlalchemy.orm import relationship

from models.associations.associations import job_offer_candidate_association
from models.user.user import UserBase


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


class Candidate(UserBase):
    __tablename__ = "candidate"

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
        study_level=StudyLevel.null,
        sex=Sex.null,
        image_id=None,
        resume_id=None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.study_level = study_level
        self.sex = sex

        self.image_id = image_id
        self.resume_id = resume_id
