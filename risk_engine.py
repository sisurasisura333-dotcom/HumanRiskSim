def calculate_risk(score):
    """Convert numeric risk score to Low / Medium / High"""
    if score <= 30:
        return "LOW"
    elif score <= 60:
        return "MEDIUM"
    else:
        return "HIGH"
