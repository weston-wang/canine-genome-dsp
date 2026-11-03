"""The delivery requirement is access ~0.196, not 1.0 -- and molecules, not devices, supply it."""

from canine_dsp import delivery_answer as da
from canine_dsp.core import catalogue as cat


def test_the_requirement_is_not_full_access():
    """The previous answer set access AND duty to 1.0 at once, which overstated the requirement and
    reopened the schedule-coherence defect."""
    need = da.required_access()
    assert need[cat.PARENCHYMA] < 0.25
    assert need[cat.LEPTOMENINGEAL] < 0.02
    for v in need.values():
        assert v > 0


def test_molecular_selection_closes_every_route_at_both_compartments():
    """The decisive claim: no implant, no catheter, no sonication."""
    c = da.closes_with_molecular_selection()
    for comp in (cat.PARENCHYMA, cat.LEPTOMENINGEAL):
        assert c[comp]["all_routes_closed"] is True, comp
        assert c[comp]["worst_margin"] > 0, comp
    assert c["tolerable"] is True
    assert c["schedule_coherent"] is True


def test_the_closing_regimen_contains_no_procedure():
    """Access and duty must come from one schedule; a procedure in the regimen breaks that."""
    names = " ".join(da.closes_with_molecular_selection()["regimen"]).lower()
    for procedure in ("ultrasound", "convection", "intrathecal", "implant", "radiation",
                      "intra-arterial"):
        assert procedure not in names, procedure


def test_the_best_device_falls_short_for_a_generic_small_molecule():
    """Stated honestly: the measured 5.9x does NOT rescue access 0.021 in parenchyma."""
    r = da.rescued_by_device(cat.SMALL_MOLECULE_ACCESS[cat.PARENCHYMA])
    assert r["clears_alone"] is False
    assert r["clears_with_device"] is False


def test_the_device_rescues_an_agent_that_is_partly_penetrant():
    """And where it DOES help is quantified, which is how the CDK4/6 arm should be stated."""
    assert da.rescued_by_device(0.11)["clears_with_device"] is True
    assert da.rescued_by_device(0.03)["clears_with_device"] is False
    assert da.rescued_by_device(0.11)["minimum_kp_uu_the_device_rescues"] < 0.05


def test_every_option_records_provenance_and_a_verdict():
    for o in da.OPTIONS:
        assert len(o.verdict) > 40, o.name
        assert len(o.evidence) > 40, o.name


def test_options_that_fail_on_duration_are_marked_as_such():
    """CED has the best canine evidence of any device and the schedule still defeats it."""
    ced = next(o for o in da.OPTIONS if "convection" in o.name)
    assert ced.duty < 0.01
    assert "DURATION" in ced.verdict.upper()


def test_answer_names_the_mechanism_and_the_residual():
    s = da.answer()
    assert "MOLECULAR SELECTION" in s
    assert "kill rate" in s.lower()
