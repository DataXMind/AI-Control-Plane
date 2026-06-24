"""Analyze — Milestone C+ : Argos Detect→Repair→Review→Mutate protocol."""

from __future__ import annotations

from typing import Any

from ai_control_plane.core.models import (
    AnalyzeFinding,
    MutateResult,
    RepairProposal,
    ReviewDecision,
)
from ai_control_plane.core.policies import ApprovalGate


class AnalyzeAdapter:
    """SAPAL Analyze stage — 4-stage Argos protocol (ADR-3 / C+-3)."""

    def __init__(
        self,
        config: dict[str, Any],
        *,
        approval_gate: ApprovalGate | None = None,
    ) -> None:
        self._config = config
        self._approval_gate = approval_gate

    def _detect(self, sense_output: dict[str, Any]) -> AnalyzeFinding:
        threshold = int(self._config.get("anomaly_event_threshold", 50))
        event_count = int(sense_output.get("event_count", 0))
        z_anomaly = bool(sense_output.get("z_score_anomaly"))
        iforest = sense_output.get("isolation_forest_anomaly")
        anomaly = event_count > threshold or z_anomaly or iforest is True
        return AnalyzeFinding(
            anomaly_detected=anomaly,
            event_count=event_count,
            z_score_anomaly=z_anomaly,
            details={"isolation_forest_anomaly": iforest},
        )

    def _repair(self, finding: AnalyzeFinding) -> RepairProposal | None:
        if not finding.anomaly_detected:
            return None
        return RepairProposal(
            action="reduce_rate",
            target="token_usage",
            rationale=f"event_count={finding.event_count} above threshold",
        )

    def _review(self, repair: RepairProposal | None) -> ReviewDecision:
        if repair is None:
            return ReviewDecision(approved=True, requires_approval=False)
        if self._approval_gate is None:
            return ReviewDecision(approved=False, requires_approval=True)
        approval = self._approval_gate.request(
            "sapal_mutate",
            {"repair": repair.model_dump(mode="json")},
        )
        return ReviewDecision(
            approved=False,
            requires_approval=True,
            approval_id=str(approval.id),
        )

    def _mutate(self, repair: RepairProposal | None, review: ReviewDecision) -> MutateResult:
        if repair is None:
            return MutateResult(applied=False, proposal={})
        if not review.approved and review.requires_approval:
            return MutateResult(
                applied=False,
                proposal={"repair": repair.model_dump(mode="json"), "pending_approval": True},
            )
        return MutateResult(
            applied=False,
            proposal={"repair": repair.model_dump(mode="json"), "note": "proposal only"},
        )

    def analyze(self, sense_output: dict[str, Any]) -> dict[str, Any]:
        """Run Detect→Repair→Review→Mutate; fail-closed per stage."""
        try:
            finding = self._detect(sense_output)
            repair = self._repair(finding)
            review = self._review(repair)
            mutate = self._mutate(repair, review)
        except Exception as exc:
            return {
                "status": "failed",
                "stage": "analyze",
                "reason": str(exc),
                "anomaly_detected": False,
            }

        return {
            "anomaly_detected": finding.anomaly_detected,
            "event_count": finding.event_count,
            "threshold": int(self._config.get("anomaly_event_threshold", 50)),
            "detect": finding.model_dump(mode="json"),
            "repair": repair.model_dump(mode="json") if repair else None,
            "review": review.model_dump(mode="json"),
            "mutate": mutate.model_dump(mode="json"),
            "status": "ok",
        }
