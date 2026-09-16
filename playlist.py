from typing import List, Optional


class Node:
    """Represents a single track in the circular playlist."""
    def __init__(self, name: str):
        self.name: str = name
        self.next: Optional['Node'] = None


class CircularPlaylist:
    """A circular singly linked list representing a looping radio queue."""
    def __init__(self):
        self.head: Optional[Node] = None
        self.current: Optional[Node] = None
        self.size: int = 0

    def __len__(self) -> int:
        """Returns the number of songs in the playlist."""
        return self.size

    def is_empty(self) -> bool:
        """Returns True if the playlist contains no songs."""
        return self.head is None

    def add_song(self, name: str) -> None:
        """Inserts a new song at the end of the circle."""
        new_node = Node(name)
        if self.is_empty():
            self.head = new_node
            new_node.next = self.head
            self.current = self.head
        else:
            # Find the last node (the node pointing to self.head)
            tail = self.head
            while tail.next != self.head:
                tail = tail.next
            
            tail.next = new_node
            new_node.next = self.head
            
        self.size += 1

    def skip_next(self) -> str:
        """Advances the currently playing pointer and returns the new song name."""
        if self.is_empty() or self.current is None:
            raise IndexError("Cannot skip in an empty playlist.")
        
        self.current = self.current.next
        return self.current.name

    def remove_current(self) -> str:
        """Removes current song, advances to next, and returns removed name."""
        if self.is_empty() or self.current is None:
            raise IndexError("Cannot remove from an empty playlist.")

        removed_name = self.current.name

        # Case 1: Only 1 song in the list
        if self.size == 1:
            self.head = None
            self.current = None
            self.size = 0
            return removed_name

        # Case 2: Multiple songs - find the predecessor of self.current
        prev = self.current
        while prev.next != self.current:
            prev = prev.next

        next_node = self.current.next
        prev.next = next_node

        # Update head reference if head was the removed node
        if self.current == self.head:
            self.head = next_node

        self.current = next_node
        self.size -= 1
        return removed_name

    def elimination_shuffle(self, k: int) -> List[str]:
        """Plays Josephus game: repeatedly skips k - 1 songs and removes the k-th."""
        if self.is_empty() or k < 1:
            return []

        removed_songs: List[str] = []

        while self.size > 1:
            # Advance k - 1 steps forward
            for _ in range(k - 1):
                self.skip_next()
            # Remove the k-th song
            removed_songs.append(self.remove_current())

        # Append the surviving song
        if self.current is not None:
            removed_songs.append(self.current.name)

        return removed_songs