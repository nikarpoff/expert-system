from sqlalchemy.orm import Session

from app.config import settings
from app.database.repositories import KnowledgeRepository
from app.engine.bayes_engine import BayesEngine, EngineState


class DiagnosisService:
    def __init__(self, session: Session):
        repo = KnowledgeRepository(session)
        diagnoses = repo.load_diagnoses()
        symptoms = repo.load_symptoms()
        rules_map = repo.load_rules_map()
        self.diagnosis_by_id = {d.id: d for d in diagnoses}
        self.symptom_by_id = {s.id: s for s in symptoms}
        self.engine = BayesEngine(
            self.diagnosis_by_id,
            self.symptom_by_id,
            rules_map,
            exclusion_threshold=settings.exclusion_threshold,
        )

    def start(self) -> EngineState:
        return self.engine.initialize()
