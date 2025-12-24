def explain_diagnosis(disease: str, confidence: float, region: str) -> str:
    return (
        f"The AI system detected signs consistent with {disease} "
        f"with a confidence of {confidence * 100:.1f}%. "
        f"The affected area appears to be {region}. "
        "This result must be reviewed by a qualified medical professional."
    )
