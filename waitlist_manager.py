from __future__ import annotations
from typing import Optional, Iterator


class Node:
    """Singly linked node for customer name"""
    __slots__ = ("name", "next")

    def __init__(self, name: str):
        self.name: str = name
        self.next: Optional[Node] = None

    def __repr__(self) -> str:
        return f"Node({self.name!r})"


class LinkedList:
    """Minimal singly linked list to manage waitlist"""
    def __init__(self):
        self.head: Optional[Node] = None

    def add_front(self, name: str) -> None:
        new_node = Node(name)
        new_node.next = self.head
        self.head = new_node

    def add_end(self, name: str) -> str:
        new_node = Node(name)
        if self.head is None:
            self.head = new_node
            return f"{name} added to the end of the waitlist"
        tail = self.head
        while tail.next:
            tail = tail.next
        tail.next = new_node
        return f"{name} added to the end of the waitlist"

    def remove(self, name: str) -> str:
        prev: Optional[Node] = None
        curr: Optional[Node] = self.head
        while curr:
            if curr.name == name:
                if prev is None:
                    # removing head
                    self.head = curr.next
                else:
                    prev.next = curr.next
                return f"Removed {name} from the waitlist"
            prev, curr = curr, curr.next
        return f"{name} not found"

    def print_list(self) -> None:
        if self.head is None:
            print("The waitlist is empty.")
            return
        print("Current waitlist:")
        for n in self:
            print(f"- {n}")

    def __iter__(self) -> Iterator[str]:
        curr = self.head
        while curr:
            yield curr.name
            curr = curr.next

    def __len__(self) -> int:
        count = 0
        curr = self.head
        while curr:
            count += 1
            curr = curr.next
        return count


def waitlist_manager() -> None:
    """Command-line interface"""
    wl = LinkedList()
    MENU = (
        "--- Waitlist Manager ---\n"
        "1. Add customer to front\n"
        "2. Add customer to end\n"
        "3. Remove customer by name\n"
        "4. Print waitlist\n"
        "5. Exit"
    )
    while True:
        print(MENU)
        choice = input("Choose an option (1–5): ").strip()
        if choice == "1":
            name = input("Enter customer name to add to front: ").strip()
            if name:
                wl.add_front(name)
        elif choice == "2":
            name = input("Enter customer name to add to end: ").strip()
            if name:
                msg = wl.add_end(name)
                print(msg)
        elif choice == "3":
            name = input("Enter customer name to remove: ").strip()
            if name:
                print(wl.remove(name))
        elif choice == "4":
            wl.print_list()
        elif choice == "5":
            print("Exiting waitlist manager.")
            break
        else:
            print("Invalid option. Choose 1–5.")


if __name__ == "__main__":
    waitlist_manager()

"""
Design Memo`

How the list works:
This program uses a simple linked list to keep track of a waitlist. Each spot in the list is a Node
that holds a customer’s name and a pointer to the next person. The LinkedList only keeps track of
the head, which is the first person in line. When add_front is called, a new Node becomes the new
head, pushing everyone else back. When add_end is called, the program walks to the last Node and
attaches the new one there. To remove, the program searches through the list and changes pointers
so the removed person is skipped. Printing goes through each Node from the head until the list ends.

Role of head:
The head is the entry point of the list. It is the only direct pointer we store, and everything else
is found by following next links from the head. When the head is None, the list is empty. If the
head gets removed, the next Node takes its place as the new head. Without the head pointer, we
would lose the entire list.

Why a custom list:
Real engineers sometimes build custom lists when built-in types do not give enough control.
Examples include when you need fast insertions at the front, or when memory layout needs to be
very specific. Linked lists also make it easy to add or remove items without shifting a whole
array. In real systems, this can matter for speed or for keeping data structures predictable.
For a waitlist tool like this, it makes sense to place VIPs right at the front and general
customers at the back. A linked list makes those operations clear and direct. For larger systems,
other data structures might be better, but this is a solid fit here.
"""
