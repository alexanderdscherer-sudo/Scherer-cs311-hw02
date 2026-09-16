"""
Homework 2: The Playlist Shuffler -- verification suite.

Run: python test_playlist.py
Prints the Success Token only if every check below passes.
"""

import base64
import hashlib
import random
import sys

from playlist import CircularPlaylist

ASSIGNMENT_ID = "HW02"


def get_student_id() -> str:
    """Prompt for the student's USI username; baked into the Success Token
    so a copied/shared token decodes to someone else's name, not yours."""
    student_id = input("Enter your USI username (e.g. cwill): ").strip()
    while not student_id:
        student_id = input("Username cannot be blank. Enter your USI username: ").strip()
    return student_id


def generate_token(assignment_id: str, student_id: str) -> str:
    digest = hashlib.sha256(f"CS311-{assignment_id}-{student_id}-VERIFIED".encode()).hexdigest()[:16]
    raw = f"CS311|{assignment_id}|{student_id}|PASS|{digest}"
    return base64.b64encode(raw.encode()).decode()


def print_success_banner(assignment_id: str) -> None:
    student_id = get_student_id()
    token = generate_token(assignment_id, student_id)
    print("\n" + "=" * 60)
    print(f"  ALL CHECKS PASSED -- {assignment_id}")
    print(f"  STUDENT: {student_id}")
    print("  SUCCESS TOKEN (paste this into Blackboard):")
    print(f"  {token}")
    print("=" * 60 + "\n")


def check(label: str, condition: bool, failures: list) -> None:
    status = "PASS" if condition else "FAIL"
    print(f"  [{status}] {label}")
    if not condition:
        failures.append(label)


def build_playlist(songs) -> CircularPlaylist:
    pl = CircularPlaylist()
    for s in songs:
        pl.add_song(s)
    return pl


def basic_correctness(failures: list) -> None:
    pl = build_playlist(["A", "B", "C"])
    check("playlist has 3 songs after adding 3", len(pl) == 3, failures)
    nxt = pl.skip_next()
    check("skip_next advances to the next song (B)", nxt == "B", failures)
    removed = pl.remove_current()
    check("remove_current removes the currently-playing song (B)", removed == "B", failures)
    check("playlist has 2 songs after removal", len(pl) == 2, failures)
    check("skip_next still cycles correctly after a removal", pl.skip_next() in ("A", "C"), failures)

    single = build_playlist(["Solo"])
    check("single-song playlist: skip_next returns the same song", single.skip_next() == "Solo", failures)
    check("single-song playlist: remove_current works without error", single.remove_current() == "Solo", failures)
    check("single-song playlist is empty after removing its only song", len(single) == 0, failures)


def elimination_shuffle_known_case(failures: list) -> None:
    pl = build_playlist(["A", "B", "C", "D", "E", "F"])
    result = pl.elimination_shuffle(k=3)
    check(
        "elimination_shuffle(k=3) on [A..F] matches Part A, Q3: removed C,F,D,B,E, survivor A",
        result == ["C", "F", "D", "B", "E", "A"],
        failures,
    )


def elimination_shuffle_stress_test(failures: list) -> None:
    rng = random.Random(311)
    for trial in range(30):
        n = rng.randint(2, 15)
        k = rng.randint(1, 10)
        songs = [f"song-{i}" for i in range(n)]
        pl = build_playlist(songs)
        result = pl.elimination_shuffle(k)
        if sorted(result) != sorted(songs):
            failures.append(f"trial {trial} (n={n}, k={k}): removal list doesn't contain exactly the original songs")
            return
        if len(set(result)) != len(songs):
            failures.append(f"trial {trial} (n={n}, k={k}): a song was removed more than once")
            return
    check(f"elimination_shuffle stress test: 30 random (n, k) trials all removed every song exactly once", True, failures)


def main() -> int:
    failures: list = []

    print("Running basic correctness checks...\n")
    basic_correctness(failures)
    if failures:
        print(f"\n{len(failures)} check(s) failed. No token issued.")
        return 1

    print("\nReplaying the Part A, Question 3 scenario...\n")
    elimination_shuffle_known_case(failures)
    if failures:
        print(f"\n{len(failures)} check(s) failed. No token issued.")
        return 1

    print("\nRunning elimination_shuffle stress test (30 random trials)...\n")
    elimination_shuffle_stress_test(failures)

    print()
    if failures:
        print(f"{len(failures)} check(s) failed. No token issued.")
        return 1

    print_success_banner(ASSIGNMENT_ID)
    return 0


if __name__ == "__main__":
    sys.exit(main())
