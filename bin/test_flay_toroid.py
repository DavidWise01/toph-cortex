#!/usr/bin/env python3
from flay_toroid import Answer, Fact, Juliet, Mandel, Ternary, excursion


def expect_raises(exc, fn):
    try:
        fn()
    except exc:
        return
    raise AssertionError(f"expected {exc.__name__}")


def main():
    m = Mandel()
    j = Juliet(m, "What happened?")

    assert j.state == Ternary.QUESTION
    assert m.revision == 0

    j.open()
    assert j.state == Ternary.ROOT

    f = Fact(
        what="idea entered the surviving corpus",
        who="named source",
        when="t0",
        where="public record",
        evidence="source-1",
    )
    j.answer("Supported answer.", [f])
    out = j.close()

    assert out.text == "Supported answer."
    assert j.state == Ternary.CLOSED
    assert m.revision == 1
    assert m.answers == ["Supported answer."]
    assert m.facts == [f]

    # One full open-answer-close only.
    expect_raises(RuntimeError, j.open)
    expect_raises(RuntimeError, j.close)
    expect_raises(RuntimeError, lambda: j.answer("rewrite"))

    # Cannot close unanswered or unresolved branches.
    j2 = Juliet(m, "Why?").open()
    expect_raises(RuntimeError, j2.close)
    j2.answer("unknown", resolved=False)
    expect_raises(RuntimeError, j2.close)
    assert m.revision == 1

    # Convenience path is also append-only.
    excursion(
        m,
        "What happened next?",
        "Second supported answer.",
        [Fact(what="second event", evidence="source-2")],
    )
    assert m.revision == 2
    assert len(m.answers) == 2
    assert len(m.facts) == 2

    # Input guards.
    expect_raises(ValueError, lambda: Juliet(m, "   "))
    j3 = Juliet(m, "?").open()
    expect_raises(ValueError, lambda: j3.answer("   "))

    print("0e / FLAY MANDEL-JULIET TOROID v1 TEST PASS")


if __name__ == "__main__":
    main()
