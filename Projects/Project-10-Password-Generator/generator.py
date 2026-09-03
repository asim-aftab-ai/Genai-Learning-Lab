import random
import string


def generate_password(length: int, complexity: str) -> str:
    """Generate a random password based on length and complexity level."""
    # Base pool: letters only
    char_pool = string.ascii_letters

    if complexity in ("numbers", "symbols"):
        char_pool += string.digits

    if complexity == "symbols":
        char_pool += string.punctuation

    # Pick randomly from the compiled character pool
    return "".join(random.choice(char_pool) for _ in range(length))