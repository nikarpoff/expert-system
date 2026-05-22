def select_most_informative_symptom(
    pending_symptoms: set[int],
    active_diagnoses: set[int],
    rules_map: dict[int, dict[int, object]],
) -> int | None:
    best_symptom = None
    best_score = -1
    for symptom_id in pending_symptoms:
        score = sum(1 for d in active_diagnoses if symptom_id in rules_map.get(d, {}))
        if score > best_score:
            best_score = score
            best_symptom = symptom_id
    return best_symptom
