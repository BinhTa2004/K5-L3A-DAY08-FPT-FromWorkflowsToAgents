"""Check that the R4 experiment removes cost without changing refund semantics."""

from pathlib import Path

import pytest

from bonus.swarm_no_peer import run_claim
from lab8.app import prepare_store
from lab8.metrics import check_trace
from lab8.shapes import swarm_reference


@pytest.mark.parametrize("claim_id,seed", [("C-001", 11), ("C-002", 55), ("C-004", 11)])
def test_removing_peer_preserves_outcome_and_restores_reference(tmp_path, monkeypatch, claim_id, seed):
    monkeypatch.chdir(tmp_path)
    baseline_store = tmp_path / "baseline.sqlite"
    variant_store = tmp_path / "variant.sqlite"
    prepare_store(baseline_store)
    prepare_store(variant_store)
    original_complete, original_trace = swarm_reference.complete, swarm_reference._Trace
    baseline = swarm_reference.run_claim(claim_id, seed=seed, store_path=str(baseline_store))
    variant = run_claim(claim_id, seed=seed, store_path=str(variant_store))
    assert swarm_reference.complete is original_complete
    assert swarm_reference._Trace is original_trace
    assert (variant.status, variant.proposal_amount, variant.refund_effects, variant.committed_audit_count) == (
        baseline.status, baseline.proposal_amount, baseline.refund_effects, baseline.committed_audit_count
    )
    assert variant.model_calls == baseline.model_calls - 1
    assert variant.tool_calls == baseline.tool_calls
    assert variant.cost_estimate < baseline.cost_estimate
    assert variant.run_id != baseline.run_id
    assert Path(variant.trace_path).is_file()
    assert check_trace(variant.as_dict()) == (True, "ok")
