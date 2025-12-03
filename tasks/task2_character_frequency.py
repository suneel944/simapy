"""Task 2: String Character Frequency

Write a program that counts character occurrences in a string and outputs them
in order of first appearance.

Example:
    Input: "hello world"
    Output: h:1, e:1, l:3, o:2, w:1, r:1, d:1

Assumptions:
    - Case sensitive: 'A' and 'a' are counted separately
    - Whitespace is included: spaces, tabs, newlines are counted as characters
    - Special characters are included: punctuation, symbols are counted
    - Empty string returns empty output
    - Order is based on first appearance in the string
"""

from collections import OrderedDict


def count_character_frequency(text: str) -> dict[str, int]:
    if not text:
        return OrderedDict()

    frequency: dict[str, int] = OrderedDict()

    for char in text:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1

    return frequency


def format_character_frequency(text: str) -> str:
    frequency = count_character_frequency(text)
    if not frequency:
        return ""

    return ", ".join(f"{char}:{count}" for char, count in frequency.items())


def main() -> None:
    """Main function to demonstrate character frequency counting."""
    test_cases = [
        "hello world",
        "Hello World",
        "aabbcc",
        "",
        "!@#$%",
        "test\nwith\ttabs",
        "  spaces  ",
    ]

    print("Character Frequency Counter")
    print("=" * 50)

    for test_input in test_cases:
        result = format_character_frequency(test_input)
        print(f"Input:  {repr(test_input)}")
        print(f"Output: {result}")
        print()


if __name__ == "__main__":
    main()
