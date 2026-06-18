def calculate_match_score(
    required_skills,
    candidate_skills
):

    required = set(
        skill.lower()
        for skill in required_skills
    )

    candidate = set(
        skill.lower()
        for skill in candidate_skills
    )

    matched = required.intersection(
        candidate
    )

    if len(required) == 0:
        return 0

    return round(
        len(matched) /
        len(required) * 100,
        2
    )