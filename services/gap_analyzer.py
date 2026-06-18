def analyze_skills(
        required_skills,
        candidate_skills
):

    required = set(
        [s.lower() for s in required_skills]
    )

    candidate = set(
        [s.lower() for s in candidate_skills]
    )

    matched = list(
        required.intersection(candidate)
    )

    missing = list(
        required - candidate
    )

    additional = list(
        candidate - required
    )

    return {

        "matched": matched,

        "missing": missing,

        "additional": additional

    }