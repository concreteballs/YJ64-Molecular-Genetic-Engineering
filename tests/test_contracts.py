import pytest

from yj64_molecular_genetic.contracts import (
    Assessment,
    CandidateRef,
    ContributionResponse,
    DisciplineReview,
    EvidenceRef,
    ReviewStatus,
    affected_reviews_to_invalidate,
)


@pytest.fixture
def candidate():
    return CandidateRef("mol-candidate-1", 1, "1.0", "molecular_genetic")


def review(candidate, module, status=ReviewStatus.PASS, **kwargs):
    return DisciplineReview(
        candidate=candidate,
        reviewer_module=module,
        reviewer_version="1.0",
        status=status,
        rationale="Reviewed within declared scope.",
        **kwargs,
    )


def contribution(candidate, module):
    return ContributionResponse(
        candidate=candidate, module_id=module, no_proposal=True,
        rationale="No evidence-backed improvement identified in this review.",
    )


def test_candidate_requires_origin(candidate):
    assert candidate.origin_module == "molecular_genetic"
    with pytest.raises(ValueError):
        CandidateRef("x", 0, "1.0", "molecular_genetic")


def test_contribution_requires_proposal_or_explicit_no_proposal(candidate):
    with pytest.raises(ValueError):
        ContributionResponse(candidate, "chemistry")
    with pytest.raises(ValueError):
        ContributionResponse(candidate, "chemistry", no_proposal=True)


def test_enhancement_proposal_requires_evidence_and_success_criteria(candidate):
    from yj64_molecular_genetic.contracts import EnhancementProposal

    with pytest.raises(ValueError):
        EnhancementProposal(
            proposal_id="p1", candidate=candidate, proposing_module="chemistry",
            objective="Improve candidate", improvement="Improve interaction model",
            mechanism="Use independent evidence", expected_benefit="Reduce uncertainty",
            success_criteria=("Reduce prediction error",), evidence=(),
        )


def test_missing_review_or_contribution_fails_closed(candidate):
    assessment = Assessment(candidate, frozenset({
        "molecular_genetic", "chemistry", "biological_engineering"
    }))
    assert not assessment.may_accept()
    assert assessment.missing_reviews() == frozenset({
        "molecular_genetic", "chemistry", "biological_engineering"
    })


def test_origin_cannot_self_certify(candidate):
    assessment = Assessment(
        candidate,
        frozenset({"molecular_genetic"}),
        reviews=(review(candidate, "molecular_genetic"),),
        contributions=(contribution(candidate, "molecular_genetic"),),
    )
    assert not assessment.may_accept()


def test_independent_review_and_all_contributions_required(candidate):
    modules = frozenset({"molecular_genetic", "chemistry"})
    assessment = Assessment(
        candidate, modules,
        reviews=(review(candidate, "molecular_genetic"), review(candidate, "chemistry")),
        contributions=(contribution(candidate, "molecular_genetic"),),
    )
    assert not assessment.may_accept()


def test_complete_independent_assessment_can_pass(candidate):
    modules = frozenset({"molecular_genetic", "chemistry"})
    assessment = Assessment(
        candidate, modules,
        reviews=(review(candidate, "molecular_genetic"), review(candidate, "chemistry")),
        contributions=(contribution(candidate, "molecular_genetic"),
                       contribution(candidate, "chemistry")),
    )
    assert assessment.may_accept()


def test_reject_and_hard_constraints_block(candidate):
    modules = frozenset({"molecular_genetic", "chemistry"})
    rejected = Assessment(
        candidate, modules,
        reviews=(review(candidate, "molecular_genetic"),
                 review(candidate, "chemistry", ReviewStatus.REJECT)),
        contributions=(contribution(candidate, "molecular_genetic"),
                       contribution(candidate, "chemistry")),
    )
    assert not rejected.may_accept()

    constrained = Assessment(
        candidate, modules,
        reviews=(review(candidate, "molecular_genetic"),
                 review(candidate, "chemistry", hard_constraints=("unresolved hazard",))),
        contributions=(contribution(candidate, "molecular_genetic"),
                       contribution(candidate, "chemistry")),
    )
    assert not constrained.may_accept()


def test_conditional_review_must_state_conditions(candidate):
    with pytest.raises(ValueError):
        review(candidate, "chemistry", ReviewStatus.CONDITIONAL)


def test_downstream_review_invalidation_is_transitive():
    graph = {
        "molecular_genetic": ("biological_engineering", "chemistry"),
        "chemistry": ("materials",),
        "biological_engineering": ("robotics",),
    }
    assert affected_reviews_to_invalidate("molecular_genetic", graph) == frozenset({
        "biological_engineering", "chemistry", "materials", "robotics"
    })


def test_evidence_requires_provenance():
    with pytest.raises(ValueError):
        EvidenceRef("e1", "model_prediction", "")
