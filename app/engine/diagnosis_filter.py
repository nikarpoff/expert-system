def filter_diagnoses(probabilities: dict[int, float], exclusion_threshold: float) -> set[int]:
    return {d_id for d_id, p in probabilities.items() if p >= exclusion_threshold}
