def filter_diagnoses(probabilities: dict[str, float], exclusion_threshold: float) -> set[str]:
    return {d_id for d_id, p in probabilities.items() if p >= exclusion_threshold}
