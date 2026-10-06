#!/usr/bin/env python3
"""FLAY Mandel-Juliet single-toroid reasoning primitive.

Mandel: bound corpus/current state.
Juliet: temporary tangent workspace.
One question = one OPEN -> ANSWER -> CLOSE excursion.
"""

from dataclasses import dataclass, field
from enum import IntEnum
from typing import Iterable, Tuple


class Ternary(IntEnum):
    QUESTION = -1
    ROOT = 0
    CLOSED = 1


@dataclass(frozen=True)
class Fact:
    what: str
    who: str = ""
    when: str = ""
    where: str = ""
    evidence: str = ""


@dataclass(frozen=True)
class Answer:
    text: str
    facts: Tuple[Fact, ...] = ()
    resolved: bool = True


@dataclass
class Mandel:
    """Bound state. Closed Juliet results append here."""

    facts: list[Fact] = field(default_factory=list)
    answers: list[str] = field(default_factory=list)
    revision: int = 0

    def bind(self, answer: Answer) -> None:
        if not answer.resolved:
            raise ValueError("unresolved Juliet result cannot be bound to Mandel")
        self.answers.append(answer.text)
        self.facts.extend(answer.facts)
        self.revision += 1


class Juliet:
    """One-shot tangent excursion bound to one Mandel state."""

    def __init__(self, mandel: Mandel, question: str):
        question = question.strip()
        if not question:
            raise ValueError("question required")
        self.mandel = mandel
        self.question = question
        self.state = Ternary.QUESTION
        self._answer: Answer | None = None
        self._closed = False

    def open(self) -> "Juliet":
        if self._closed:
            raise RuntimeError("closed excursion")
        if self.state != Ternary.QUESTION:
            raise RuntimeError("excursion already opened")
        self.state = Ternary.ROOT
        return self

    def answer(
        self,
        text: str,
        facts: Iterable[Fact] = (),
        *,
        resolved: bool = True,
    ) -> Answer:
        if self.state != Ternary.ROOT or self._closed:
            raise RuntimeError("answer requires one open excursion")
        text = text.strip()
        if not text:
            raise ValueError("answer text required")
        self._answer = Answer(text=text, facts=tuple(facts), resolved=resolved)
        return self._answer

    def close(self) -> Answer:
        if self.state != Ternary.ROOT or self._closed:
            raise RuntimeError("close requires one open excursion")
        if self._answer is None:
            raise RuntimeError("cannot close without an answer")
        if not self._answer.resolved:
            raise RuntimeError("unresolved answer cannot close")

        self.mandel.bind(self._answer)
        self.state = Ternary.CLOSED
        self._closed = True
        return self._answer


def excursion(
    mandel: Mandel,
    question: str,
    answer_text: str,
    facts: Iterable[Fact] = (),
) -> Answer:
    """Convenience API for one full OPEN -> ANSWER -> CLOSE cycle."""
    juliet = Juliet(mandel, question).open()
    juliet.answer(answer_text, facts)
    return juliet.close()


if __name__ == "__main__":
    m = Mandel()
    excursion(
        m,
        "What happened?",
        "A supported event was retained.",
        [Fact(what="supported event", evidence="demo")],
    )
    assert m.revision == 1
    print("0e / FLAY MANDEL-JULIET TOROID v1 PASS")
