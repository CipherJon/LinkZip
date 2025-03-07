import string
import random

def generate_short_code(length=6):
    """
    Generate a random URL-safe short code
    Args:
        length (int): Desired code length (default 6, max 20)
    Returns:
        str: Generated short code
    Raises:
        ValueError: If length is invalid
    """
    if not 4 <= length <= 20:
        raise ValueError("Length must be between 4 and 20 characters")
        
    chars = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
    rng = random.SystemRandom()
    return ''.join(rng.choice(chars) for _ in range(length))