"""Unit tests for Task 2: String Character Frequency"""

from tasks.task2_character_frequency import count_character_frequency, format_character_frequency


class TestCountCharacterFrequency:
    """Test cases for count_character_frequency function"""

    def test_basic_example(self) -> None:
        """Test the example from the assignment"""
        result = count_character_frequency("hello world")
        expected = {"h": 1, "e": 1, "l": 3, "o": 2, " ": 1, "w": 1, "r": 1, "d": 1}
        assert dict(result) == expected
        # Verify order of first appearance
        assert list(result.keys()) == ["h", "e", "l", "o", " ", "w", "r", "d"]

    def test_case_sensitivity(self) -> None:
        """Test that case is preserved (case-sensitive)"""
        result = count_character_frequency("Hello")
        assert dict(result) == {"H": 1, "e": 1, "l": 2, "o": 1}
        assert list(result.keys()) == ["H", "e", "l", "o"]

    def test_empty_string(self) -> None:
        """Test edge case: empty string"""
        result = count_character_frequency("")
        assert dict(result) == {}
        assert len(result) == 0

    def test_single_character(self) -> None:
        """Test edge case: single character"""
        result = count_character_frequency("a")
        assert dict(result) == {"a": 1}

    def test_repeated_characters(self) -> None:
        """Test string with repeated characters"""
        result = count_character_frequency("aaa")
        assert dict(result) == {"a": 3}

    def test_whitespace_included(self) -> None:
        """Test that whitespace characters are counted"""
        result = count_character_frequency("a b")
        assert dict(result) == {"a": 1, " ": 1, "b": 1}
        assert list(result.keys()) == ["a", " ", "b"]

    def test_tabs_and_newlines(self) -> None:
        """Test that tabs and newlines are counted"""
        result = count_character_frequency("a\tb\nc")
        assert dict(result) == {"a": 1, "\t": 1, "b": 1, "\n": 1, "c": 1}
        assert list(result.keys()) == ["a", "\t", "b", "\n", "c"]

    def test_special_characters(self) -> None:
        """Test that special characters are counted"""
        result = count_character_frequency("!@#$%")
        assert dict(result) == {"!": 1, "@": 1, "#": 1, "$": 1, "%": 1}
        assert list(result.keys()) == ["!", "@", "#", "$", "%"]

    def test_numbers(self) -> None:
        """Test that numbers are counted"""
        result = count_character_frequency("12321")
        assert dict(result) == {"1": 2, "2": 2, "3": 1}
        assert list(result.keys()) == ["1", "2", "3"]

    def test_mixed_content(self) -> None:
        """Test string with mixed content"""
        result = count_character_frequency("Hello, World!")
        assert dict(result) == {
            "H": 1,
            "e": 1,
            "l": 3,
            "o": 2,
            ",": 1,
            " ": 1,
            "W": 1,
            "r": 1,
            "d": 1,
            "!": 1,
        }
        assert list(result.keys()) == ["H", "e", "l", "o", ",", " ", "W", "r", "d", "!"]

    def test_unicode_characters(self) -> None:
        """Test that Unicode characters are handled correctly"""
        result = count_character_frequency("café")
        assert dict(result) == {"c": 1, "a": 1, "f": 1, "é": 1}
        assert list(result.keys()) == ["c", "a", "f", "é"]

    def test_order_preservation(self) -> None:
        """Test that order of first appearance is preserved"""
        result = count_character_frequency("abacaba")
        # First appearance: a, b, a (already seen), c, a (already seen), b (already seen), a (already seen)
        assert list(result.keys()) == ["a", "b", "c"]
        assert dict(result) == {"a": 4, "b": 2, "c": 1}


class TestFormatCharacterFrequency:
    """Test cases for format_character_frequency function"""

    def test_basic_example(self) -> None:
        """Test the example from the assignment"""
        result = format_character_frequency("hello world")
        # Note: space character will be visible in output
        assert result == "h:1, e:1, l:3, o:2,  :1, w:1, r:1, d:1"

    def test_empty_string(self) -> None:
        """Test edge case: empty string"""
        result = format_character_frequency("")
        assert result == ""

    def test_single_character(self) -> None:
        """Test edge case: single character"""
        result = format_character_frequency("a")
        assert result == "a:1"

    def test_case_sensitivity_formatting(self) -> None:
        """Test that case is preserved in formatting"""
        result = format_character_frequency("Hello")
        assert result == "H:1, e:1, l:2, o:1"

    def test_special_characters_formatting(self) -> None:
        """Test formatting with special characters"""
        result = format_character_frequency("!@#")
        assert result == "!:1, @:1, #:1"

    def test_whitespace_formatting(self) -> None:
        """Test formatting with whitespace"""
        result = format_character_frequency("a b")
        assert result == "a:1,  :1, b:1"
