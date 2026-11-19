import pytest
from yj64_molecular_genetic.contracts import CandidateRef, ContributionResponse, DisciplineReview, EvidenceRef, ReviewStatus, EnhancementProposal, ProposalStatus
from yj64_molecular_genetic.wire import to_wire_candidate, to_wire_contribution, to_wire_evidence, to_wire_proposal, to_wire_review

def candidate():
    return CandidateRef("mol-1", 3, "1.0", "molecular_genetic")

def evidence():
    return EvidenceRef("ev-1", "model_prediction", "model:run-42", version="v2",
                       limitations=("not experimentally validated",))

def test_candidate_and_evidence_mapping():
    c, e = to_wire_candidate(candidate()), to_wire_evidence(evidence())
    assert c["schema_id"] == "yj64.cross_module.candidate.v1"
    assert c["candidate_id"] == "mol-1" and c["version"] == 3
    assert e["evidence_id"] == "ev-1" and e["version"] == "v2"
    assert e["limitations"] == ["not experimentally validated"]

def test_review_maps_shared_fields():
    review = DisciplineReview(candidate(), "chemistry", "1.2.0", ReviewStatus.PASS,
                              "Reviewed", evidence=(evidence(),), interface_checks=("binding",))
    wire = to_wire_review(review)
    assert wire["reviewer_version"] == "1.2.0" and wire["interface_checks"] == ["binding"]
    assert wire["evidence"][0]["evidence_id"] == "ev-1"

def test_proposal_and_contribution_mapping():
    proposal = EnhancementProposal("p1", candidate(), "chemistry", "Improve stability", "Refine interaction",
                                   "Model comparison", "Lower uncertainty", ("lower error",), (evidence(),))
    wire = to_wire_contribution(ContributionResponse(candidate(), "chemistry", proposals=(proposal,)))
    assert wire["proposals"][0]["objective"] == "Improve stability" and wire["no_proposal"] is False

def test_decided_proposal_requires_parent_decision_version():
    proposal = EnhancementProposal("p2", candidate(), "chemistry", "Improve stability", "Refine interaction",
                                   "Model comparison", "Lower uncertainty", ("lower error",), (evidence(),),
                                   status=ProposalStatus.ACCEPTED, decision_rationale="Parent approved")
    with pytest.raises(ValueError):
        to_wire_proposal(proposal)
    assert to_wire_proposal(proposal, decision_version=4)["decision_version"] == 4

def test_no_proposal_rationale_mapping():
    response = ContributionResponse(candidate(), "chemistry", no_proposal=True, rationale="No improvement identified")
    assert to_wire_contribution(response)["rationale"] == "No improvement identified"
