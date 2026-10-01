"""Grading must be against the user's stated bar, not against "has it been demonstrated in a dog"."""

from canine_dsp import standard_audit as sa


def test_the_growth_bar_is_conservative_not_flattering():
    """The one input that genuinely failed. Its derivation has to show the bar is HARDER than the
    clinical data requires -- a conservative bar cannot manufacture a closure."""
    d = sa.growth_bar_derivation()
    assert d["bar_is_conservative"] is True
    assert d["bar_in_use"] > d["implied_range"][1]
    assert min(d["conservatism_factor"]) > 1.0


def test_the_conclusion_survives_the_plausible_growth_range():
    """If the answer only works at one growth value it is an artefact of that value."""
    s = sa.growth_sensitivity()
    assert len(s) == 3
    for row in s.values():
        # the synthetic-lethal agent must stay far below full systemic exposure at every rate
        assert row["tng908"]["min_access_fraction"] < 0.01


def test_no_input_fails_for_lack_of_a_canine_measurement_alone():
    """Rule 2: 'unmeasured in the dog' is not a gap under the stated bar. Any failing input must
    fail for having NO basis or a circular one -- never merely for lacking a canine measurement."""
    for g in sa.failing():
        assert g.verdict in (sa.Verdict.FAILS_NO_BASIS, sa.Verdict.FAILS_CIRCULAR)
        assert "no basis" in g.why.lower() or "circular" in g.why.lower() \
            or "point prior" in g.why.lower() or "no derivation" in g.why.lower()


def test_items_wrongly_called_gaps_are_recorded_as_such():
    """The rule-2 error itself has to be in the record, or it recurs."""
    wrong = sa.wrongly_reported_as_gaps()
    assert len(wrong) >= 4
    for g in wrong:
        assert g.verdict is sa.Verdict.PASSES


def test_statement_reports_both_counts():
    s = sa.statement()
    assert "PASS" in s
    assert "wrongly reported" in s.lower() or "Wrongly reported" in s
