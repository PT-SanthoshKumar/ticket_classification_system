CATEGORY_KEYWORDS = {
    "Billing": {
        "payment", "charged", "charge", "invoice", "receipt", "refund", "billing",
        "bank", "card", "checkout", "tax", "purchase order", "unpaid"
    },
    "Technical": {
        "app", "crash", "crashes", "down", "error", "500", "server", "upload",
        "slow", "freeze", "loading", "api", "integration", "dashboard", "bug"
    },
    "Account": {
        "password", "login", "account", "profile", "admin", "workspace", "user",
        "invite", "verification", "ownership", "reactivate", "display name"
    },
    "Shipping": {
        "shipping", "shipment", "delivery", "package", "courier", "tracking",
        "order", "replacement", "return label", "delivered", "address"
    },
    "Feedback": {
        "suggestion", "feature", "please add", "would be useful", "layout",
        "colors", "harder", "helpful", "typo", "keyboard shortcuts", "dark mode"
    },
    "Security": {
        "security", "suspicious", "private", "access", "compromised", "unknown ip",
        "api keys", "encrypted", "single sign on", "audit", "soc 2", "breach"
    },
}

SECURITY_STRONG_KEYWORDS = {
    "suspicious", "compromised", "unknown ip", "breach", "private workspace",
    "without my approval", "without approval", "api keys", "soc 2", "audit",
    "encrypted", "single sign on"
}


def rule_based_category(ticket_text):
    text = str(ticket_text).lower()
    if any(keyword in text for keyword in SECURITY_STRONG_KEYWORDS):
        return "Security"

    scores = {
        category: sum(1 for keyword in keywords if keyword in text)
        for category, keywords in CATEGORY_KEYWORDS.items()
    }
    best_category, best_score = max(scores.items(), key=lambda item: item[1])
    return best_category if best_score > 0 else None
