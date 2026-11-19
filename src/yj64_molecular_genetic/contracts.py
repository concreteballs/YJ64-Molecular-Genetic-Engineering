"""Versioned, fail-closed cross-disciplinary contracts.

These data structures describe computational candidate review. They do not
execute laboratory actions or grant permissions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable


class ReviewStatus(str, Enum):
    PASS = "pass"
    CONDITIONAL = "conditional"
    REJECT = "reject"
    NOT_APPLICABLE = "not_applicable"
    NOT_REVIEWED = "not_reviewed"


class ProposalStatus(str, Enum):
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    DEFERRED = "deferred"


@dataclass(frozen=True)
class CandidateRef:
    candidate_id: str
    version: int
    schema_version: str
    origin_module: str

    def __post_init__(self) -> None:
        if not self.candidate_id.strip():
            raise ValueError("candidate_id is required")
        if self.version < 1:
            raise ValueError("version must be >= 1")
        if not self.schema_version.strip():
            raise ValueError("schema_version is required")
        if not self.origin_module.strip():
            raise ValueError("origin_module is required")


@dataclass(frozen=True)
class EvidenceRef:
    evidence_id: str
    evidence_type: str
    source: str
    version: str = ""
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.evidence_id.strip() or not self.evidence_type.strip():
            raise ValueError("evidence identity and type are required")
        if not self.source.strip():
            raise ValueError("evidence source is required")


@dataclass(frozen=True)
class DisciplineReview:
    candidate: CandidateRef
    reviewer_module: str
    reviewer_version: str
    status: ReviewStatus
    rationale: str
    evidence: tuple[EvidenceRef, ...] = ()
    assumptions: tuple[str, ...] = ()
    uncertainty: tuple[str, ...] = ()
    interface_checks: tuple[str, ...] = ()
    hazards: tuple[str, ...] = ()
    hard_constraints: tuple[str, ...] = ()
    conditions: tuple[str, ...] = ()
    unresolved_questions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.reviewer_module.strip() or not self.reviewer_version.strip():
            raise ValueError("reviewer identity and version are required")
        if not self.rationale.strip():
            raise ValueError("review rationale is required")
        if self.status is ReviewStatus.NOT_APPLICABLE and not self.rationale.strip():
            raise ValueError("not_applicable requires a rationale")
        if self.status is ReviewStatus.CONDITIONAL and not self.conditions:
            raise ValueError("conditional review must state conditions")


@dataclass(frozen=True)
class EnhancementProposal:
    proposal_id: str
    candidate: CandidateRef
    proposing_module: str
    objective: str
    improvement: str
    mechanism: str
    expected_benefit: str
    success_criteria: tuple[str, ...]
    evidence: tuple[EvidenceRef, ...]
    assumptions: tuple[str, ...] = ()
    tradeoffs: tuple[str, ...] = ()
    risks: tuple[str, ...] = ()
    dependencies: tuple[str, ...] = ()
    validation_plan: tuple[str, ...] = ()
    status: ProposalStatus = ProposalStatus.PROPOSED
    decision_rationale: str = ""

    def __post_init__(self) -> None:
        required = (
            self.proposal_id, self.proposing_module, self.objective,
            self.improvement, self.mechanism, self.expected_benefit,
        )
        if any(not value.strip() for value in required):
            raise ValueError("proposal identity and core description fields are required")
        if not self.success_criteria:
            raise ValueError("measurable success criteria are required")
        if not self.evidence:
            raise ValueError("enhancement proposals require evidence references")
        if self.status is not ProposalStatus.PROPOSED and not self.decision_rationale.strip():
            raise ValueError("decided proposals require decision_rationale")


@dataclass(frozen=True)
class ContributionResponse:
    candidate: CandidateRef
    module_id: str
    proposals: tuple[EnhancementProposal, ...] = ()
    no_proposal: bool = False
    rationale: str = ""

    def __post_init__(self) -> None:
        if not self.module_id.strip():
            raise ValueError("module_id is required")
        if self.no_proposal == bool(self.proposals):
            raise ValueError("provide proposals OR explicit no_proposal, not both/neither")
        if self.no_proposal and not self.rationale.strip():
            raise ValueError("no_proposal requires a rationale")
        if any(p.candidate != self.candidate or p.proposing_module != self.module_id
               for p in self.proposals):
            raise ValueError("proposal candidate and proposing module must match response")


@dataclass(frozen=True)
class Assessment:
    candidate: CandidateRef
    relevant_modules: frozenset[str]
    reviews: tuple[DisciplineReview, ...] = ()
    contributions: tuple[ContributionResponse, ...] = ()

    def __post_init__(self) -> None:
        if self.candidate.origin_module not in self.relevant_modules:
            raise ValueError("origin_module must be included in relevant_modules")

    def missing_reviews(self) -> frozenset[str]:
        received = {
            r.reviewer_module for r in self.reviews
            if r.candidate == self.candidate
        }
        return self.relevant_modules - received

    def missing_contributions(self) -> frozenset[str]:
        received = {
            c.module_id for c in self.contributions
            if c.candidate == self.candidate
        }
        return self.relevant_modules - received

    def blocking_reviews(self) -> tuple[DisciplineReview, ...]:
        return tuple(
            r for r in self.reviews
            if r.candidate == self.candidate
            and (
                r.status in (ReviewStatus.REJECT, ReviewStatus.NOT_REVIEWED)
                or bool(r.hard_constraints)
                or (r.status is ReviewStatus.CONDITIONAL and bool(r.conditions))
            )
        )

    def may_accept(self) -> bool:
        """Fail closed: all relevant modules review and contribute independently."""
        if self.missing_reviews() or self.missing_contributions() or self.blocking_reviews():
            return False
        independent = {
            r.reviewer_module for r in self.reviews
            if r.candidate == self.candidate
            and r.reviewer_module != self.candidate.origin_module
            and r.status in (ReviewStatus.PASS, ReviewStatus.NOT_APPLICABLE)
        }
        return bool(independent)


def affected_reviews_to_invalidate(
    changed_module: str,
    dependency_graph: dict[str, Iterable[str]],
) -> frozenset[str]:
    """Return transitive downstream modules whose prior reviews are stale."""
    visited: set[str] = set()
    frontier = list(dependency_graph.get(changed_module, ()))
    while frontier:
        module = frontier.pop()
        if module in visited:
            continue
        visited.add(module)
        frontier.extend(dependency_graph.get(module, ()))
    return frozenset(visited)
