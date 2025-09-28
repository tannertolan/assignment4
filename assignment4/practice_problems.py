"""
Practice Problems — choose DS, implement, justify.
Run: python practice_problems.py
"""

from collections import Counter, deque
from typing import Iterable, List, Dict, Deque, Tuple

# Problem 1: Given a stream of user IDs, return the first time each unique ID appeared (stable de-duplication).
def stable_unique(ids: Iterable[int]) -> List[int]:
    """
    Returns unique IDs in first-seen order.
    DS Choice: Hash set for O(1) membership tests and a list to preserve arrival order.
    Ops and Big-O: For n items, each lookup/insert in the set is amortized O(1). Total O(n) time, O(n) space.
    """
    seen = set()
    out: List[int] = []
    for x in ids:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


# Problem 2: Given text, return the top k most frequent words with counts, ties broken lexicographically.
def top_k_words(text: str, k: int) -> List[Tuple[str, int]]:
    """
    DS Choice: Dictionary (hash map) to count frequencies. Counter simplifies aggregation without changing complexity.
    Ops and Big-O: Counting is O(n) over tokens. Heap could optimize k selection, but for clarity we sort -> O(m log m),
    where m is number of unique words. Space O(m).
    """
    tokens = [t.lower() for t in text.split()]
    freq: Dict[str, int] = Counter(tokens)
    return sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))[:k]


# Problem 3: Ticketing system that enqueues requests and serves in FIFO with O(1) enqueue/dequeue/peek.
class TicketQueue:
    """
    DS Choice: Queue via collections.deque which supports O(1) append and popleft.
    Ops and Big-O: enqueue O(1), dequeue O(1), peek O(1). Space O(n).
    """
    def __init__(self) -> None:
        self._q: Deque[str] = deque()

    def enqueue(self, ticket: str) -> None:
        self._q.append(ticket)

    def dequeue(self) -> str:
        if not self._q:
            raise IndexError("empty queue")
        return self._q.popleft()

    def peek(self) -> str:
        if not self._q:
            raise IndexError("empty queue")
        return self._q[0]

    def __len__(self) -> int:
        return len(self._q)


if __name__ == "__main__":
    # Sanity checks for graders
    assert stable_unique([3, 3, 2, 1, 2, 4]) == [3, 2, 1, 4]
    assert top_k_words("a A b a c b b", 2) == [("a", 3), ("b", 3)]

    q = TicketQueue()
    q.enqueue("T1"); q.enqueue("T2")
    assert q.peek() == "T1"; assert q.dequeue() == "T1"; assert q.dequeue() == "T2"
    try:
        q.dequeue()
        assert False, "expected IndexError"
    except IndexError:
        pass
    print("practice_problems OK")

