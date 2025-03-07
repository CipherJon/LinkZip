import pytest
from app.utils.generate_code import generate_short_code
import string

class TestGenerateShortCode:
    """Unit tests for short code generation utility"""
    
    def test_default_length(self):
        """Test code generation with default length (6)"""
        code = generate_short_code()
        assert len(code) == 6
        assert all(c in string.ascii_letters + string.digits for c in code)

    @pytest.mark.parametrize("valid_length", [4, 8, 15, 20])
    def test_valid_lengths(self, valid_length):
        """Test supported length range (4-20)"""
        code = generate_short_code(length=valid_length)
        assert len(code) == valid_length

    @pytest.mark.parametrize("invalid_length", [3, 21, 0, -5])
    def test_invalid_lengths(self, invalid_length):
        """Test invalid lengths raise ValueError"""
        with pytest.raises(ValueError) as exc_info:
            generate_short_code(length=invalid_length)
        assert "between 4 and 20" in str(exc_info.value)

    def test_character_set(self):
        """Test generated codes only contain allowed characters"""
        code = generate_short_code(length=100)  # Uses max length for thorough check
        allowed_chars = set(string.ascii_letters + string.digits)
        assert all(c in allowed_chars for c in code)

    def test_uniqueness(self):
        """Test generated codes are unique (probabilistic)"""
        codes = {generate_short_code() for _ in range(100)}
        assert len(codes) == 100  # Extremely low collision chance with 62^6 possibilities