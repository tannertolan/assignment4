"""
Timed Challenge

Chosen prompt (from timed_challenge.txt):
"Valid Parentheses: Given a string containing only the characters '()[]{}',
determine if the input string is valid. An input string is valid if open brackets
are closed by the same type of brackets and in the correct order."
"""

from typing import Iterable

def is_valid_parentheses(s: str) -> bool:
    """
    Stack solution.
    Push opens. On close, check top. Early exit on mismatch.
    Time O(n), space O(n) in worst case.
    """
    if not isinstance(s, str):
        return False
    pairs = {')': '(', ']': '[', '}': '{'}
    opens = set(pairs.values())
    stack: list[str] = []
    for ch in s:
        if ch in opens:
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
        else:
            # Non-bracket character invalid per prompt scope
            return False
    return not stack


def _run_tests() -> None:
    # Core cases
    assert is_valid_parentheses("()")
    assert is_valid_parentheses("()[]{}")
    assert is_valid_parentheses("{[]}")
    assert not is_valid_parentheses("(]")
    assert not is_valid_parentheses("([)]")
    assert not is_valid_parentheses("(")
    assert not is_valid_parentheses(")")
    # Edge cases
    assert is_valid_parentheses("")            # Empty is valid sequence
    assert not is_valid_parentheses("abc")     # Non-bracket chars not allowed
    assert not is_valid_parentheses(None)      # Wrong type
    # Robustness
    long_ok = "({[]})" * 10_000
    assert is_valid_parentheses(long_ok)
    print("timed_challenge OK")


if __name__ == "__main__":
    _run_tests()

"""
Reflection on the timed task (≈230 words)

I selected a stack because the problem is a textbook last-in first-out validation. Each open bracket must be matched by the most recent unmatched open, which maps directly to stack push/pop semantics. Hash lookups map closers to their matching openers in O(1), so the primary loop is linear and memory is proportional to the depth of nesting. Alternative designs like recursive descent or repeated string replacement introduce overhead or risk worst-case quadratic behavior, which is not competitive for interview constraints.

The 30-minute limit drove a bias to known-good patterns with minimal surface area. I avoided abstractions, classes, or regex since they add cognitive load without performance upside here. I also guarded against non-string input and unexpected characters to avoid silent success on invalid data. Tests included canonical positives, canonical negatives, empty input, wrong types, and a large case to smoke-test asymptotics.

Trade-offs: I rejected accepting non-bracket characters as no-ops. Some variants allow them, but the prompt says the string contains only bracket characters. I chose strict validation and return False upon seeing anything else. I also skipped micro-optimizations like pre-allocating list capacity since Python’s dynamic list growth is amortized O(1) and clarity wins. If performance were extreme, a C extension or PyPy could help, but the algorithmic choice remains a stack with O(n) time and O(n) space. The solution is concise, readable, and interview-ready.
"""
