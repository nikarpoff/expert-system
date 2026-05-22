from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Diagnosis(Base):
    __tablename__ = 'diagnoses'
    id: Mapped[str] = mapped_column(String(3), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    prior_probability: Mapped[float] = mapped_column(Float, nullable=False)


class Symptom(Base):
    __tablename__ = 'symptoms'
    id: Mapped[str] = mapped_column(String(3), primary_key=True)
    question: Mapped[str] = mapped_column(String(512), nullable=False)


class Rule(Base):
    __tablename__ = 'diagnosis_symptom'
    diagnosis_id: Mapped[str] = mapped_column(ForeignKey('diagnoses.id'), primary_key=True)
    symptom_id: Mapped[str] = mapped_column(ForeignKey('symptoms.id'), primary_key=True)
    p_symptom_if_diagnosis: Mapped[float] = mapped_column('p_s_given_d', Float, nullable=False)
    p_symptom_if_not_diagnosis: Mapped[float] = mapped_column('p_s_given_not_d', Float, nullable=False)

    diagnosis: Mapped[Diagnosis] = relationship()
    symptom: Mapped[Symptom] = relationship()
