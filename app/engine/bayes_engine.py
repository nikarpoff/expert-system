from dataclasses import dataclass, field

from app.engine.diagnosis_filter import filter_diagnoses
from app.engine.probability_service import bayes_update
from app.engine.symptom_selector import select_most_informative_symptom


@dataclass
class StepTrace:
    question: str
    answer_yes: bool
    probabilities: dict[str, float]


@dataclass
class EngineState:
    probabilities: dict[int, float]
    active_diagnoses: set[int]
    pending_symptoms: set[int]
    traces: list[StepTrace] = field(default_factory=list)


class BayesEngine:
    def __init__(self, diagnosis_by_id, symptom_by_id, rules_map, exclusion_threshold: float):
        self.diagnosis_by_id = diagnosis_by_id
        self.symptom_by_id = symptom_by_id
        self.rules_map = rules_map
        self.exclusion_threshold = exclusion_threshold

    def initialize(self) -> EngineState:
        probs = {d_id: d.prior_probability for d_id, d in self.diagnosis_by_id.items()}
        all_symptoms = set(self.symptom_by_id.keys())
        return EngineState(probabilities=probs, active_diagnoses=set(probs), pending_symptoms=all_symptoms)

    def choose_next_symptom(self, state: EngineState) -> int | None:
        return select_most_informative_symptom(state.pending_symptoms, state.active_diagnoses, self.rules_map)

    def apply_answer(self, state: EngineState, symptom_id: int, answer_yes: bool) -> None:
        for d_id in list(state.active_diagnoses):
            rule = self.rules_map.get(d_id, {}).get(symptom_id)
            if not rule:
                continue
            state.probabilities[d_id] = bayes_update(
                state.probabilities[d_id],
                rule.p_symptom_if_diagnosis,
                rule.p_symptom_if_not_diagnosis,
                answer_yes,
            )
        state.pending_symptoms.discard(symptom_id)
        state.active_diagnoses = filter_diagnoses(state.probabilities, self.exclusion_threshold)
        state.traces.append(
            StepTrace(
                question=self.symptom_by_id[symptom_id].question,
                answer_yes=answer_yes,
                probabilities={
                    self.diagnosis_by_id[d_id].name: state.probabilities[d_id]
                    for d_id in sorted(state.probabilities)
                },
            )
        )
