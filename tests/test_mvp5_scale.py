from __future__ import annotations

from awg_mvp5.scale import ScaleKernel, compare_branches


def test_population_records_are_separate_from_active_cognition() -> None:
    kernel = ScaleKernel()
    kernel.run_profile()
    assert kernel.totals()["population_records"] == 1000
    assert len(kernel.active) == 50
    assert set(kernel.active).issubset(kernel.population)


def test_promotion_and_demotion_conserve_tokens_and_beliefs() -> None:
    kernel = ScaleKernel()
    record = kernel.population["person:0050"]
    before = (record["tokens"], dict(record["beliefs"]))
    kernel.promote("person:0050")
    assert kernel.active["person:0050"]["tokens"] == before[0]
    assert kernel.active["person:0050"]["beliefs"] == before[1]
    kernel.active["person:0050"]["tokens"] = before[0]
    kernel.demote("person:0050")
    assert kernel.population["person:0050"]["tokens"] == before[0]
    assert kernel.population["person:0050"]["beliefs"] == before[1]
    assert "person:0050" not in kernel.active


def test_branch_comparison_separates_intervention_from_seed() -> None:
    comparison = compare_branches(seed=11)
    assert comparison["same_seed"] is True
    assert comparison["effect_is_not_seed_noise"] is True
    assert comparison["tokens_conserved"] is True
