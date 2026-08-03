import json

import pytest

from canine_dsp.osteosarcoma_design import CargoConstraints, Species, SpeciesScenario
from canine_dsp.osteosarcoma_spec import (
    DesignSpecification,
    illustrative_canine_design_spec,
    load_design_spec,
)


def write_spec(tmp_path, payload, name="design.json"):
    path = tmp_path / name
    path.write_text(json.dumps(payload))
    return path


def test_custom_canine_dla_and_clone_labels_round_trip_with_all_defaults(tmp_path):
    payload = {
        "schema_version": 1,
        "constraints": {
            "species": "canine",
            "min_antigens": 2,
            "max_antigens": 5,
            "required_subclones": ["founder", "pulmonary_clone_7"],
            "required_class_i_alleles": ["DLA-88*034:01"],
            "required_class_ii_alleles": ["DLA-DRB1*001:01"],
            "required_source_classes": ["fusion"],
            "min_normal_proteome_safety": 0.91,
        },
        "scenarios": [
            {"name": "nominal", "species": "dog"},
            {
                "name": "patient_dla_loss",
                "species": "canine",
                "lost_class_i_alleles": ["DLA-88*034:01"],
                "candidate_effect_scale": {"fusion_17": 0.4},
            },
        ],
    }
    loaded = load_design_spec(write_spec(tmp_path, payload))
    assert loaded.constraints.required_subclones == {"founder", "pulmonary_clone_7"}
    assert loaded.constraints.required_class_i_alleles == {"DLA-88*034:01"}
    assert loaded.constraints.species == Species.CANINE

    manifest = loaded.to_dict()
    assert manifest["constraints"]["class_i_cutoff"] == 0.5
    assert manifest["constraints"]["max_escape_risk"] == 1.0
    assert manifest["scenarios"][0]["interaction_scale"] == 1.0
    assert manifest["scenarios"][1]["candidate_effect_scale"] == {"fusion_17": 0.4}
    json.dumps(manifest)

    reloaded = load_design_spec(write_spec(tmp_path, manifest, "round_trip.json"))
    assert reloaded == loaded
    assert reloaded.to_dict() == manifest


def test_human_hla_spec_is_accepted_at_module_level(tmp_path):
    payload = {
        "schema_version": 1,
        "constraints": {
            "species": "human",
            "required_subclones": ["trunk", "metastatic_subclone"],
            "required_class_i_alleles": ["HLA-A*02:01"],
            "required_class_ii_alleles": ["HLA-DRB1*04:01"],
        },
        "scenarios": [
            {"name": "nominal", "species": "human"},
            {
                "name": "hla_a_loss",
                "species": "human",
                "lost_class_i_alleles": ["HLA-A*02:01"],
            },
        ],
    }
    specification = load_design_spec(write_spec(tmp_path, payload))
    assert specification.constraints.species == Species.HUMAN
    assert specification.scenarios[1].lost_class_i_alleles == {"HLA-A*02:01"}


def test_constraint_and_scenario_species_must_match():
    with pytest.raises(ValueError, match="species must match"):
        DesignSpecification(
            constraints=CargoConstraints("human"),
            scenarios=(SpeciesScenario("wrong_species", "canine"),),
        )


@pytest.mark.parametrize(
    "payload, message",
    [
        ({"constraints": {}, "scenarios": []}, "missing keys"),
        ({"schema_version": 2, "constraints": {}, "scenarios": [{}]}, "schema_version"),
        (
            {"schema_version": 1, "constraints": {}, "scenarios": [{}], "extra": True},
            "unknown keys",
        ),
        ({"schema_version": 1, "constraints": {}, "scenarios": []}, "nonempty JSON list"),
    ],
)
def test_schema_version_shape_and_top_level_keys_fail_closed(tmp_path, payload, message):
    with pytest.raises(ValueError, match=message):
        load_design_spec(write_spec(tmp_path, payload))


def test_illustrative_spec_exactly_tracks_current_canine_assumptions():
    specification = illustrative_canine_design_spec("ILLUSTRATIVE_DOG_07")
    constraints = specification.constraints
    assert constraints.species == Species.CANINE
    assert (constraints.min_antigens, constraints.max_antigens) == (4, 7)
    assert (constraints.min_class_i_antigens, constraints.min_class_ii_antigens) == (2, 2)
    assert constraints.min_truncal_antigens == 2
    assert constraints.required_subclones == {"trunk", "lung_A", "lung_B", "lung_C"}
    assert constraints.required_class_i_alleles == {
        "DLA-88*001:01", "DLA-88*508:01"
    }
    assert constraints.required_class_ii_alleles == {
        "DLA-DRB1*015:01", "DLA-DQA1*001:01"
    }
    assert {source.value for source in constraints.required_source_classes} == {
        "structural_variant", "fusion"
    }
    assert constraints.min_expression == .50
    assert constraints.min_clonality == .55
    assert constraints.min_normal_proteome_safety == .75
    assert constraints.min_presentation_retention == .65
    assert constraints.max_escape_risk == .35
    assert constraints.min_manufacturability == .65
    assert [scenario.name for scenario in specification.scenarios] == [
        "nominal",
        "DLA_88_001_loss",
        "DLA_DRB1_015_loss",
        "low_expression_and_retention",
        "single_antigen_loss",
    ]
    assert specification.scenarios[-1].escaped_antigens == {"ILLUSTRATIVE_DOG_07"}
    json.dumps(specification.to_dict())
