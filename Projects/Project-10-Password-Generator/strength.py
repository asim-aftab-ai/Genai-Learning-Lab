import string


def evaluate_strength(password: str) -> str:
    """Return a strength rating: Weak, Medium, or Strong."""
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c in string.digits for c in password)
    has_punct = any(c in string.punctuation for c in password)

    # Count how many criteria are met
    score = sum([has_upper, has_lower, has_digit, has_punct])

    if length >= 12 and score >= 3:
        return "Strong"
    elif length >= 8 and score >= 2:
        return "Medium"
    else:
        return "Weak"