def classify_candidate(score):

    if score >= 85:
        return "Excellent Fit"

    elif score >= 70:
        return "Good Fit"

    elif score >= 50:
        return "Average Fit"

    else:
        return "Poor Fit"