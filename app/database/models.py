from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Diagnosis(Base):
    __tablename__ = 'diagnoses'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    recommendation: Mapped[str] = mapped_column(String(1024), default='')
    prior_probability: Mapped[float] = mapped_column(Float, nullable=False)


class Symptom(Base):
    __tablename__ = 'symptoms'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question: Mapped[str] = mapped_column(String(512), nullable=False)


class Rule(Base):
    __tablename__ = 'rules'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    diagnosis_id: Mapped[int] = mapped_column(ForeignKey('diagnoses.id'), nullable=False)
    symptom_id: Mapped[int] = mapped_column(ForeignKey('symptoms.id'), nullable=False)
    p_symptom_if_diagnosis: Mapped[float] = mapped_column(Float, nullable=False)
    p_symptom_if_not_diagnosis: Mapped[float] = mapped_column(Float, nullable=False)

    diagnosis: Mapped[Diagnosis] = relationship()
    symptom: Mapped[Symptom] = relationship()
