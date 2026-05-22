from collections import defaultdict

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import Diagnosis, Rule, Symptom


class KnowledgeRepository:
    def __init__(self, session: Session):
        self.session = session

    def load_diagnoses(self) -> list[Diagnosis]:
        return list(self.session.scalars(select(Diagnosis)))

    def load_symptoms(self) -> list[Symptom]:
        return list(self.session.scalars(select(Symptom)))

    def load_rules_map(self) -> dict[int, dict[int, Rule]]:
        rules = self.session.scalars(select(Rule)).all()
        data: dict[int, dict[int, Rule]] = defaultdict(dict)
        for rule in rules:
            data[rule.diagnosis_id][rule.symptom_id] = rule
        return dict(data)
