"""
Homework 2: The Playlist Shuffler -- starter.

Complete CircularPlaylist below. See HW2_The_Playlist_Shuffler.md,
Part B, for the full requirements.
"""

from typing import List, Optional


class _SongNode:
    __slots__ = ("name", "next")

    def __init__(self, name: str) -> None:
        self.name = name
        self.next: Optional["_SongNode"] = None


class CircularPlaylist:
    def __init__(self) -> None:
        self._current: Optional[_SongNode] = None  # the "currently playing" node
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def add_song(self, name: str) -> None:
        """Insert `name` at the end of the circle (its next wraps back to the head)."""
        # TODO
        raise NotImplementedError

    def skip_next(self) -> str:
        """Advance the currently-playing pointer to the next song and return its name."""
        # TODO
        raise NotImplementedError

    def remove_current(self) -> str:
        """
        Remove the currently-playing song, rewire the circle around it,
        advance to the next song, and return the name of the removed song.
        """
        # TODO
        raise NotImplementedError

    def elimination_shuffle(self, k: int) -> List[str]:
        """
        Repeatedly skip k-1 songs and remove the k-th (the Josephus
        pattern from Part A, Question 3), until one song remains.
        Return the removed songs in removal order, with the survivor
        as the final element of the list.
        """
        # TODO
        raise NotImplementedError
