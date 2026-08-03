import pytest

from canine_dsp.osteosarcoma_design import (
    AntigenCandidate,
    CargoConstraints,
    DesignWeights,
    InfeasibleCargoError,
    ScheduleCandidate,
    Species,
    SpeciesScenario,
    design_vaccine_cargo,
)


def candidate(candidate_id, *, species="human", class_i=.8, class_ii=.7,
              class_i_alleles=("HLA-A*02:01",), class_ii_alleles=("HLA-DRB1*04:01",),
              subclones=("trunk",), expression=.8, clonality=.8, truncality=.9,
              safety=.95, retention=.9, escape=.1, manufacturability=.9,
              source="snv", synergy=(0.0,), competition=(0.0,)):
    if species in {"dog", "canine"}:
        if class_i_alleles == ("HLA-A*02:01",):
            class_i_alleles = ("DLA-88*001:01",)
        if class_ii_alleles == ("HLA-DRB1*04:01",):
            class_ii_alleles = ("DLA-DRB1*015:01",)
    return AntigenCandidate(
        candidate_id=candidate_id,
        species=species,
        source_class=source,
        expression=expression,
        clonality=clonality,
        truncality=truncality,
        mhc_i_presentation=class_i,
        mhc_ii_presentation=class_ii,
        normal_proteome_safety=safety,
        presentation_retention=retention,
        escape_risk=escape,
        manufacturability=manufacturability,
        subclones=subclones,
        class_i_alleles=class_i_alleles if class_i else (),
        class_ii_alleles=class_ii_alleles if class_ii else (),
        synergy_loadings=synergy,
        competition_loadings=competition,
    )


def test_candidates_validate_species_alleles_and_safety_direction():
    canine = candidate("dog-fusion", species="dog", source="fusion")
    assert canine.species == Species.CANINE
    assert canine.source_class.value == "fusion"
    with pytest.raises(ValueError, match="DLA-"):
        candidate("bad-dog", species="dog", class_i_alleles=("HLA-B*07:02",))
    with pytest.raises(ValueError, match="normal_proteome_safety"):
        candidate("unsafe-range", safety=1.01)
    with pytest.raises(ValueError, match="requires at least one class-I allele"):
        candidate("missing-hla", class_i=.8, class_i_alleles=())


def test_robust_hla_loss_and_subclone_constraints_determine_cargo():
    candidates = [
        candidate(
            "a-high-but-lost",
            class_i=.99,
            class_ii=0,
            class_i_alleles=("HLA-A*02:01",),
            subclones=("trunk",),
            expression=.99,
        ),
        candidate(
            "b-escape-clone",
            class_i=0,
            class_ii=.9,
            class_ii_alleles=("HLA-DRB1*04:01",),
            subclones=("clone-b",),
        ),
        candidate(
            "c-retained",
            class_i=.82,
            class_ii=.75,
            class_i_alleles=("HLA-B*07:02",),
            class_ii_alleles=("HLA-DPB1*04:01",),
            subclones=("trunk", "clone-b"),
            expression=.72,
        ),
    ]
    constraints = CargoConstraints(
        "human",
        min_antigens=2,
        max_antigens=2,
        min_class_i_antigens=1,
        min_class_ii_antigens=1,
        required_subclones={"trunk", "clone-b"},
    )
    scenarios = [
        SpeciesScenario("nominal", "human"),
        SpeciesScenario("hla-a-loss", "human", lost_class_i_alleles={"HLA-A*02:01"}),
    ]
    result = design_vaccine_cargo(candidates, constraints, scenarios=scenarios)
    assert set(result.selected.candidate_ids) == {"b-escape-clone", "c-retained"}
    assert result.selected.worst_scenario == "hla-a-loss"
    assert result.selected.covered_subclones == {"trunk", "clone-b"}
    assert result.search_mode == "exact"
    assert not result.clinical_use


def test_low_rank_second_order_synergy_and_competition_affect_selection():
    candidates = [
        candidate("a", synergy=(1.0,), competition=(0.0,)),
        candidate("b", synergy=(1.0,), competition=(0.0,), expression=.79),
        candidate("c", synergy=(0.0,), competition=(1.0,), expression=.81),
        candidate("d", synergy=(0.0,), competition=(1.0,), expression=.80),
    ]
    constraints = CargoConstraints("human", min_antigens=2, max_antigens=2)
    weights = DesignWeights(synergy=2.0, competition=2.0)
    result = design_vaccine_cargo(candidates, constraints, weights=weights)
    assert set(result.selected.candidate_ids) == {"a", "b"}
    assert result.selected.interaction_score_by_scenario["nominal"] > 0
    assert all(len(ranking.candidate_ids) == 2 for ranking in result.rankings)


def test_filters_are_auditable_and_infeasible_constraints_fail_closed():
    candidates = [
        candidate("eligible", class_ii=0),
        candidate("off-target-risk", class_ii=0, safety=.2),
    ]
    constraints = CargoConstraints(
        "human",
        min_antigens=1,
        max_antigens=2,
        min_class_i_antigens=1,
        min_class_ii_antigens=1,
        min_normal_proteome_safety=.8,
    )
    with pytest.raises(InfeasibleCargoError, match="class-II") as caught:
        design_vaccine_cargo(candidates, constraints)
    assert "insufficient class-II-presented candidates" in caught.value.reasons


def test_canine_design_is_deterministic_in_forced_beam_mode_and_ranks_schedules():
    candidates = [
        candidate(
            f"dog-{index:02d}",
            species="canine",
            subclones=("trunk", f"clone-{index % 3}"),
            expression=.55 + .02 * index,
            source="fusion" if index == 0 else "snv",
        )
        for index in range(12)
    ]
    constraints = CargoConstraints(
        "canine",
        min_antigens=3,
        max_antigens=5,
        required_subclones={"trunk", "clone-0", "clone-1", "clone-2"},
        required_source_classes={"fusion"},
    )
    schedules = [
        ScheduleCandidate("conservative", (0, 21, 42), (1, 1, 1)),
        ScheduleCandidate(
            "hypothesis-b",
            (0, 14, 35),
            (1, .8, .8),
            first_order_scale=1.05,
            objective_penalty=.02,
        ),
    ]
    kwargs = dict(
        scenarios=[SpeciesScenario("canine-nominal", "dog")],
        schedules=schedules,
        exact_enumeration_limit=10,
        beam_width=64,
    )
    first = design_vaccine_cargo(candidates, constraints, **kwargs)
    second = design_vaccine_cargo(candidates, constraints, **kwargs)
    assert first.search_mode == "beam"
    assert first.selected == second.selected
    assert first.selected.schedule_name == "hypothesis-b"
    assert "dog-00" in first.selected.candidate_ids
    assert first.feasible_designs_evaluated > 0


def test_scenario_references_and_interaction_ranks_are_validated():
    with pytest.raises(ValueError, match="same synergy-loading rank"):
        design_vaccine_cargo(
            [candidate("a", synergy=(1.0,)), candidate("b", synergy=(1.0, 0.0))],
            CargoConstraints("human", min_antigens=1, max_antigens=2),
        )
    with pytest.raises(ValueError, match="unknown candidates"):
        design_vaccine_cargo(
            [candidate("a")],
            CargoConstraints("human", min_antigens=1, max_antigens=1),
            scenarios=[SpeciesScenario("bad", "human", escaped_antigens={"missing"})],
        )
