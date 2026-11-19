"""Loss-aware adapter from molecular/genetic native contracts to YJ64 wire v1."""
from __future__ import annotations
from typing import Any
from .contracts import CandidateRef, ContributionResponse, DisciplineReview, EnhancementProposal, EvidenceRef, ProposalStatus

CANDIDATE_SCHEMA = "yj64.cross_module.candidate.v1"
EVIDENCE_SCHEMA = "yj64.cross_module.evidence.v1"
REVIEW_SCHEMA = "yj64.cross_module.review.v1"
PROPOSAL_SCHEMA = "yj64.cross_module.enhancement_proposal.v1"
CONTRIBUTION_SCHEMA = "yj64.cross_module.contribution.v1"
SCHEMA_VERSION = "1.0"


def _candidate_ref(value: CandidateRef) -> dict[str, Any]:
    return {"candidate_id": value.candidate_id, "version": value.version,
            "schema_version": value.schema_version, "origin_module": value.origin_module}


def to_wire_candidate(value: CandidateRef) -> dict[str, Any]:
    return {"schema_id": CANDIDATE_SCHEMA, "schema_version": SCHEMA_VERSION,
            **_candidate_ref(value), "intended_scope": [], "input_refs": [], "provenance_refs": []}


def to_wire_evidence(value: EvidenceRef) -> dict[str, Any]:
    return {"schema_id": EVIDENCE_SCHEMA, "schema_version": SCHEMA_VERSION,
            "evidence_id": value.evidence_id, "evidence_type": value.evidence_type,
            "source": value.source, "version": value.version, "limitations": list(value.limitations)}


def to_wire_review(value: DisciplineReview) -> dict[str, Any]:
    return {
        "schema_id": REVIEW_SCHEMA, "schema_version": SCHEMA_VERSION,
        "candidate": _candidate_ref(value.candidate), "reviewer_module": value.reviewer_module,
        "reviewer_version": value.reviewer_version, "status": value.status.value,
        "rationale": value.rationale, "evidence": [to_wire_evidence(x) for x in value.evidence],
        "assumptions": list(value.assumptions), "uncertainty": list(value.uncertainty),
        "interface_checks": list(value.interface_checks), "hazards": list(value.hazards),
        "hard_constraints": list(value.hard_constraints), "conditions": list(value.conditions),
        "unresolved_questions": list(value.unresolved_questions),
    }


def to_wire_proposal(value: EnhancementProposal, *, decision_version: int | None = None) -> dict[str, Any]:
    result = {
        "schema_id": PROPOSAL_SCHEMA, "schema_version": SCHEMA_VERSION,
        "proposal_id": value.proposal_id, "candidate": _candidate_ref(value.candidate),
        "proposing_module": value.proposing_module, "objective": value.objective,
        "improvement": value.improvement, "mechanism": value.mechanism,
        "expected_benefit": value.expected_benefit, "success_criteria": list(value.success_criteria),
        "evidence": [to_wire_evidence(x) for x in value.evidence],
        "assumptions": list(value.assumptions), "tradeoffs": list(value.tradeoffs),
        "risks": list(value.risks), "dependencies": list(value.dependencies),
        "validation_plan": list(value.validation_plan), "status": value.status.value,
    }
    if value.status is not ProposalStatus.PROPOSED:
        if decision_version is None or decision_version < 1:
            raise ValueError("decision_version >= 1 is required for a parent-decided proposal")
        result["decision_rationale"] = value.decision_rationale
        result["decision_version"] = decision_version
    return result


def to_wire_contribution(value: ContributionResponse, *, decision_versions: dict[str, int] | None = None) -> dict[str, Any]:
    result = {"schema_id": CONTRIBUTION_SCHEMA, "schema_version": SCHEMA_VERSION,
              "candidate": _candidate_ref(value.candidate), "module_id": value.module_id,
              "proposals": [to_wire_proposal(p, decision_version=(decision_versions or {}).get(p.proposal_id))
                            for p in value.proposals], "no_proposal": value.no_proposal}
    if value.no_proposal:
        result["rationale"] = value.rationale
    return result
