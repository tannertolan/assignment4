from collections import Counter, OrderedDict
import heapq
import re


# Problem 1
def two_sum(nums, target):
    """
    Return a tuple of indices (i, j) such that nums[i] + nums[j] == target.
    If none, return None. Prefers the earliest valid pair by left-to-right scan.
    """
    seen = {}  # value -> index
    for j, x in enumerate(nums):
        need = target - x
        if need in seen:
            return (seen[need], j)
        seen[x] = j
    return None

"""
Analysis (Two Sum)
Time:
- Best: O(1) when the second element closes a solution.
- Average: O(n) expected with hash lookups O(1) average.
- Worst: O(n) if no solution or the match is at the end.
Space: O(n) for the hash map.
Optimization: Naive double loop is O(n^2) time, O(1) space; current approach is optimal for expected time.
Trade-offs: Hash map uses extra memory; if inputs are very small, the O(n^2) loop is simpler and fine.
"""


# Problem 2
def contains_duplicate(nums):
    """
    Return True if any value appears at least twice, else False.
    """
    seen = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False

"""
Analysis (Contains Duplicate)
Time:
- Best: O(1) if first two items are equal.
- Average: O(n) with O(1) average membership tests.
- Worst: O(n) when no duplicates.
Space: O(n) in the worst case for the set.
Optimization: Sorting then scanning is O(n log n) time and O(1) extra space (if allowed to reorder).
Trade-offs: Set approach is faster; sort approach uses less extra memory but mutates order.
"""


# Problem 3
def merge_intervals(intervals):
    """
    intervals: list[list[int,int]] like [[s,e], ...]
    Returns merged disjoint intervals sorted by start.
    """
    if not intervals:
        return []
    intervals = sorted(intervals, key=lambda ab: ab[0])
    merged = [intervals[0][:]]
    for s, e in intervals[1:]:
        last = merged[-1]
        if s <= last[1]:  # overlap
            last[1] = max(last[1], e)
        else:
            merged.append([s, e])
    return merged

"""
Analysis (Merge Intervals)
Time:
- Best: O(n log n) due to required sort, even if no overlaps.
- Average: O(n log n).
- Worst: O(n log n).
Space: O(n) to hold output; O(1) extra beyond output if sorting in place is allowed.
Optimization: If input guaranteed sorted by start, merge is O(n).
Trade-offs: Sorting cost dominates; any alternative still must order by start to merge correctly.
"""


# Problem 4
_WORD_RE = re.compile(r"[A-Za-z0-9']+")

def tokenize(text: str):
    # normalize to lowercase so "TIE" and "tie" are the same word
    return [w.lower() for w in _WORD_RE.findall(text)]

# v1  — full sort
def top_k_words_v1(text: str, k: int):
    """
    Returns list of (word, count), ordered by count desc then word asc.
    Baseline: full sort of all unique tokens. O(m log m) where m = unique words.
    """
    counts = Counter(tokenize(text))
    items = list(counts.items())
    items.sort(key=lambda t: (-t[1], t[0]))
    return items[:max(0, k)]

# v2 — selection via heapq.nsmallest with a key
def top_k_words(text: str, k: int):
    """
    Returns list of (word, count) ordered by count desc, then word asc.
    Uses heapq.nsmallest with key=(-count, word) to select top-k correctly.
    """
    counts = Counter(tokenize(text))
    if k <= 0 or not counts:
        return []
    k = min(k, len(counts))
    items = heapq.nsmallest(k, counts.items(), key=lambda t: (-t[1], t[0]))
    return [(w, c) for (w, c) in items]

"""
Analysis (Top-K Words)
v1 Baseline:
- Time: build counts O(n), sort O(m log m), total O(n + m log m), n = tokens, m = unique tokens.
- Space: O(m).
v2 Optimized (chosen solution):
- Time: O(n) to count + O(m log k) selection → O(n + m log k).
- Space: O(m) counts + O(k) internal heap.
Best/Average/Worst:
- If k >= m, v2 ≈ v1; when k ≪ m, v2 wins.
Trade-offs:
- v2 is simpler and correct for ties; v1 is fine for small m or k ≈ m.
"""


# Problem 5
class LRUCache:
    """
    Fixed-capacity LRU using OrderedDict.
    get(key) -> value or -1
    put(key, value) inserts/updates and evicts least recently used on overflow.
    """
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.cap = capacity
        self.od = OrderedDict()

    def get(self, key):
        if key not in self.od:
            return -1
        self.od.move_to_end(key, last=True)  # mark as most recent
        return self.od[key]

    def put(self, key, value):
        if key in self.od:
            self.od.move_to_end(key, last=True)
        self.od[key] = value
        if len(self.od) > self.cap:
            self.od.popitem(last=False)  # evict LRU

"""
Analysis (LRU Cache)
Time:
- Best/Average/Worst: get/put are O(1) amortized due to hash + doubly-linked list in OrderedDict.
Space:
- O(capacity) for stored entries.
Optimization:
- A manual HashMap + DoublyLinkedList gives identical asymptotics with more code; OrderedDict is production-grade.
Trade-offs:
- OrderedDict is concise and reliable; custom implementation allows tighter control and potential micro-optimizations.
Amortized Time:
- move_to_end/popitem are O(1) amortized operations per CPython guarantees.
"""


# Minimal Tests
def _run_tests():
    # Two Sum
    assert two_sum([2, 7, 11, 15], 9) == (0, 1)
    assert two_sum([1, 3, 2, 4], 6) == (2, 3)
    assert two_sum([], 5) is None
    assert two_sum([3], 3) is None
    assert two_sum([3, 3], 6) == (0, 1)

    # Contains Duplicate
    assert contains_duplicate([1, 2, 3, 1]) is True
    assert contains_duplicate([1, 2, 3, 4]) is False
    assert contains_duplicate([]) is False
    assert contains_duplicate([0, 0]) is True

    # Merge Intervals
    assert merge_intervals([[1,3],[2,6],[8,10],[15,18]]) == [[1,6],[8,10],[15,18]]
    assert merge_intervals([[1,4],[4,5]]) == [[1,5]]
    assert merge_intervals([]) == []
    assert merge_intervals([[1,2]]) == [[1,2]]
    assert merge_intervals([[5,7],[1,3],[2,4]]) == [[1,4],[5,7]]

    # Top-K Words (lowercased aggregation)
    s = "a A b a c b b"
    assert top_k_words_v1(s, 2) == [("a", 3), ("b", 3)]
    assert top_k_words(s, 2) == [("a", 3), ("b", 3)]
    assert top_k_words("", 3) == []
    assert top_k_words("x y z", 5) == [("x",1),("y",1),("z",1)]
    assert top_k_words("tie tie TIE a a", 2) == [("tie", 3), ("a", 2)]

    # LRU Cache
    cache = LRUCache(2)
    assert cache.get(1) == -1
    cache.put(1, 1)  # {1}
    cache.put(2, 2)  # {1,2}
    assert cache.get(1) == 1    # {2,1}
    cache.put(3, 3)             # evicts 2 -> {1,3}
    assert cache.get(2) == -1
    cache.put(4, 4)             # evicts 1 -> {3,4}
    assert cache.get(1) == -1
    assert cache.get(3) == 3
    assert cache.get(4) == 4

    print("All tests passed.")


if __name__ == "__main__":
    _run_tests()
