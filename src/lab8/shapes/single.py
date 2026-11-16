"""Shape B — one ReAct agent. Student work.

Use `lab8.runtime.run_react` with max_steps=8. `decide` may pick a read tool.
It must not call `issue_refund`. After the loop, the host validates the quote
and is the only writer.

A decide() that trusts ticket text over the order row will fail hidden claims
where the customer overstates the delay or cites a superseded clause.

Per-order cap: an order may already have been refunded by an earlier claim.
The read tool `lookup_refund_history` shows how much. The host still enforces
the cap, so pass the full quote to `durability.issue_refund`, not a net amount.

Caps: stop at 8 steps. Count model calls in the Budget so cost stays comparable.

Trace contract v1 (docs/contracts.md): return a trace_path to a JSON file written in this run,
{"run_id": <same run_id>, "events": [...]}, on every return path including early
ones. `lab8.trace.Trace` does this; your own tracer is fine if it matches.
"""

from __future__ import annotations

from typing import Any

from lab8.db import connect
from lab8.durability import issue_refund
from lab8.mock_llm import complete
from lab8.runtime import run_react
from lab8.schemas import Budget, RunResult, make_run_id
from lab8.shapes.common import finish
from lab8.trace import Trace


def run_claim(
    claim_id: str,
    *,
    seed: int,
    store_path: str,
    crash_at: str | None = None,
) -> RunResult:
    conn = connect(store_path)
    budget = Budget()
    trace = Trace(make_run_id("single", claim_id, seed))
    facts: dict[str, Any] = {}

    def result(status: str, proposal: int = 0, reason: str | None = None) -> RunResult:
        trace.add("decision", {"status": status, "reason": reason})
        return finish(
            conn,
            shape="single",
            claim_id=claim_id,
            seed=seed,
            status=status,
            proposal_amount=proposal,
            budget=budget,
            trace=trace,
            error_reason=reason,
        )

    def decide(observation: dict[str, Any]) -> dict[str, Any]:
        last_tool = observation.get("last_tool")
        if last_tool:
            facts[last_tool] = observation["last_result"]
        complete(budget, seed=seed, purpose="decide", prompt=f"last_tool={last_tool or 'start'}")

        if "get_claim_view" not in facts:
            action = {"tool": "get_claim_view", "args": {"claim_id": claim_id}}
        else:
            claim = facts["get_claim_view"]
            if not claim["found"]:
                action = {"final": {"status": "failed", "error_reason": "unknown_claim"}}
            elif not claim.get("order_id"):
                action = {"final": {"status": "needs_info", "error_reason": "missing_order_id"}}
            elif "lookup_order" not in facts:
                action = {
                    "tool": "lookup_order",
                    "args": {"order_id": claim["order_id"], "principal_id": claim["principal_id"]},
                }
            elif not facts["lookup_order"]["visible"]:
                action = {"final": {"status": "escalated", "error_reason": facts["lookup_order"]["reason"]}}
            elif "lookup_refund_history" not in facts:
                action = {
                    "tool": "lookup_refund_history",
                    "args": {"order_id": claim["order_id"], "principal_id": claim["principal_id"]},
                }
            elif "compute_compensation" not in facts:
                action = {"tool": "compute_compensation", "args": {"order": facts["lookup_order"]["order"]}}
            else:
                action = {"final": {"status": "quoted"}}

        trace.add("agent_action", {"tool": action["tool"]} if "tool" in action else action["final"])
        return action

    try:
        outcome = run_react(
            conn,
            budget,
            observation={},
            decide=decide,
            max_steps=8,
            worker=True,
        )
        final = outcome["final"]
        if final["status"] != "quoted":
            return result(final["status"], reason=final.get("error_reason"))

        quote = facts["compute_compensation"]
        proposal = int(quote["amount_vnd"])
        trace.add("quote", quote)
        if proposal <= 0:
            return result("denied", reason=quote["reason"])

        trace.add("refund_request", {"proposal_amount": proposal})
        refund = issue_refund(conn, claim_id, proposal, crash_at=crash_at)
        trace.add("refund_outcome", {"ok": refund["ok"], "reason": refund["reason"]})
        if not refund["ok"]:
            return result("failed" if refund["conflict"] else "denied", proposal, refund["reason"])
        return result("resolved", proposal)
    finally:
        try:
            trace.write()
        finally:
            conn.close()
