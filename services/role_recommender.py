def recommend_role(skills):

    skills = skills.lower()

    if (
        "iscala" in skills and
        "infor" in skills
    ):
        return "Infor iScala Functional Consultant"

    elif (
        "procurement" in skills and
        "finance" in skills
    ):
        return "Procurement & Finance Manager"

    elif (
        "react" in skills and
        "api" in skills
    ):
        return "Software Developer"

    elif (
        "supply chain" in skills
    ):
        return "Supply Chain Consultant"

    return "General Consultant"