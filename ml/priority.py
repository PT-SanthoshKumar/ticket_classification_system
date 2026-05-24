HIGH_KEYWORDS = {
    "urgent", "immediately", "down", "crash", "crashes", "blocked", "security",
    "breach", "fraud", "deducted", "charged twice", "private", "access",
    "cannot access", "failed twice", "damaged", "suspicious", "compromised",
    "without approval", "without my approval"
}

MEDIUM_KEYWORDS = {
    "not working", "slow", "missing", "incorrect", "refund", "cancel",
    "tracking", "change", "invite", "reset", "harder"
}


def infer_priority(ticket_text, predicted_category=None):
    """Assign a priority with transparent support-team rules."""
    text = str(ticket_text).lower()

    if any(keyword in text for keyword in HIGH_KEYWORDS):
        return "High"

    if predicted_category == "Security":
        return "High"

    if any(keyword in text for keyword in MEDIUM_KEYWORDS):
        return "Medium"

    if len(text.split()) > 22:
        return "Medium"

    return "Low"
