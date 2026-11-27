#!/usr/bin/env python3
"""Describe Your Ex in One Word — make.fun micro entry.

The verdict on the ex, in exactly one word: the relationship is a
subscription nobody asked to renew, so the only honest reply is to
cancel it. The program writes that word to the output directory the
harness provides and checks its own work before exiting.
"""

import hashlib
import os
import sys

VERDICT = "unsubscribe"

OUTPUT_NAME = "entry.txt"

GATE_MIN_CHARS = 1
GATE_MAX_CHARS = 111


def output_dir() -> str:
    """Return the directory the harness wants the entry written to."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    return chosen or "/output"


def check_word(word: str) -> None:
    """Fail loudly if the verdict breaks the competition gate."""
    if not word or word != word.strip():
        raise ValueError("entry must not be empty or padded with whitespace")
    if " " in word or "\n" in word or "\t" in word:
        raise ValueError("entry must be exactly one word")
    if not GATE_MIN_CHARS <= len(word) <= GATE_MAX_CHARS:
        raise ValueError("entry must be 1-111 characters long")


def deliver() -> int:
    """Write the verdict and verify the bytes on disk match it."""
    check_word(VERDICT)
    target_dir = output_dir()
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, OUTPUT_NAME)
    payload = VERDICT.encode("utf-8")
    with open(target, "wb") as handle:
        handle.write(payload)
    with open(target, "rb") as handle:
        written = handle.read()
    if written != payload:
        raise RuntimeError("entry on disk does not match the verdict")
    digest = hashlib.sha256(written).hexdigest()
    print(f"wrote {target} ({len(written)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(deliver())
