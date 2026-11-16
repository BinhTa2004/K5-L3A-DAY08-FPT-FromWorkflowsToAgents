"""R4 ablation: remove only the reference swarm's peer acknowledgement call.

The official swarm file remains unchanged. Patches are scoped to one synchronous
run; this experiment adapter must not be used concurrently in the same process.
"""

from unittest.mock import patch

from lab8.schemas import RunResult, make_run_id
from lab8.shapes import swarm_reference
from lab8.trace import Trace


def run_claim(claim_id: str, *, seed: int, store_path: str, crash_at: str | None = None) -> RunResult:
    original_complete = swarm_reference.complete

    def complete_without_peer(budget, *, seed, purpose, prompt):
        if purpose == "peer":
            return ""
        return original_complete(budget, seed=seed, purpose=purpose, prompt=prompt)

    def variant_trace(_run_id):
        return Trace(make_run_id("swarm_no_peer", claim_id, seed))

    with patch.object(swarm_reference, "complete", complete_without_peer), patch.object(
        swarm_reference, "_Trace", variant_trace
    ):
        result = swarm_reference.run_claim(claim_id, seed=seed, store_path=store_path, crash_at=crash_at)
    result.shape = "swarm_no_peer"
    return result
