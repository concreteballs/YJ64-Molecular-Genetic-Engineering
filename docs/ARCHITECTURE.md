# Molecular & Genetic Engineering — module architecture

## 1. Status and boundary

This is an independent, optional, separately versioned YJ64 module. It is not a submodule of Biological Engineering and is not embedded in YJ64 Engineering Core. It connects through shared versioned task, extension, evidence, hazard and review contracts.

The module owns computational molecular design/analysis and genetic-system representation/design/analysis. It does not own organism deployment, physical integration, wet-lab execution or system-level safety approval.

## 2. Functional scope

1. Evidence-indexed records of characterized proteins, enzymes, receptors, complexes, molecular structures and interactions.
2. Computational molecular structure/function analysis and interaction modelling.
3. Typed representation and computational analysis of genetic systems and their relationships to molecular components and organism-level traits.
4. Phenotype and whole-system effect prediction with explicit uncertainty and model applicability.
5. Genetic/evolutionary stability and unintended-effect assessment.
6. Provenance, evidence maturity, reproducibility and comparison against independently reviewed observations.
7. Biosafety metadata, hazard identification and hand-off to qualified independent review.
8. Generation of evidence-linked enhancement proposals for parent workflows and sibling disciplines.

## 3. Candidate data model

Every candidate is immutable by revision and identifies:
- candidate ID, version, schema version and originating module;
- molecular/genetic entities and exact input references;
- intended computational question, scope and applicability limits;
- model, database and tool versions;
- source provenance and evidence maturity;
- measured, curated, inferred, simulated and speculative elements separately;
- assumptions, uncertainty, limitations and reproducibility references;
- predicted phenotype/system-level effects and unresolved interactions;
- stability considerations, unintended-effect hypotheses and biosafety metadata;
- downstream dependencies and explicit non-claims.

A changed candidate receives a new version. Reviews of affected downstream interfaces become stale and must be repeated.

## 4. Evidence and epistemic status

The module must distinguish at least:
- curated observation;
- experimentally characterized input;
- computational hypothesis;
- model prediction;
- independently benchmarked model;
- controlled experimental evidence supplied as external evidence;
- independently replicated evidence;
- application-qualified evidence.

A sequence prediction, docking score, structure prediction, simulation, model consensus or generated design is not experimental validation. Evidence records include source, version/date where available, method, scope, limitations and confidence. Conflicting evidence is preserved rather than silently averaged.

Model applicability must be explicit. Out-of-distribution inputs, missing reference data, unresolved interactions and uncertainty must be reported. A model's confidence score is not a substitute for calibrated uncertainty or independent validation.

## 5. Computational workflow

The intended workflow is bounded and reviewable:
1. Receive a typed task and scoped computational inputs through the shared task contract.
2. Validate schemas, identifiers, provenance, units and permitted operation.
3. Select declared models/tools whose applicability and versions are recorded.
4. Perform computational analysis only within the module's allowed scope.
5. Separate observations, annotations, inferences, predictions and speculative proposals.
6. Record uncertainty, assumptions, limitations, hazards and missing evidence.
7. Emit a versioned candidate result with evidence references.
8. Request independent reviews and enhancement contributions from every relevant discipline.
9. Return results to the parent coordinator; the module cannot approve its own system-level acceptability.

This repository does not add a scheduler, worker loop, permission engine or autonomous laboratory executor.

## 6. Safety boundary

The module is for bounded computational research and evidence management. It must not provide operational workflows intended to increase pathogenicity, transmissibility, host range, immune evasion, environmental persistence, resistance to containment or uncontrolled propagation. It must not design autonomous release or propagation systems.

It must not autonomously transition from in-silico work to synthesis, transformation, culture, experimentation, release or deployment. Such activities are outside this module's execution boundary and require separately governed, qualified human oversight and institutional biosafety review.

When a request or candidate crosses a prohibited boundary, the module must stop the affected workflow, preserve an audit record and refer the matter to the applicable safety governance process. It must not attempt to route around the boundary through decomposition, alternate labels or another module.

Prefer well-characterised, non-pathogenic reference systems and non-living/computational alternatives where they meet the research objective. Do not infer that a system is safe because it is computationally designed or because no hazard was detected.

## 7. Cross-disciplinary review and enhancement

Every candidate is submitted to all relevant independent disciplines identified from intended use, dependencies, interfaces and foreseeable lifecycle effects. Molecular/genetic review by the originating module is not sufficient for overall acceptance.

Each relevant module must return two distinct outputs:
- **Independent review:** PASS, CONDITIONAL, REJECT or NOT_APPLICABLE with rationale; include evidence, assumptions, uncertainty, interface checks, hazards, hard constraints, conditions and unresolved questions.
- **Enhancement contribution:** one or more evidence-linked proposals to improve the candidate using that discipline's knowledge, methods, materials or models, or an explicit `no_proposal` with rationale.

Missing reviews or contributions are not approval. The parent coordinator accepts, rejects or defers proposals with recorded rationale. A module must not directly apply its own proposal to the candidate. An accepted proposal creates a new candidate revision or child task and triggers all affected downstream reviews again.

Relevant disciplines may include molecular biology, genetics, biochemistry, structural biology, chemistry, physics, computational science, biological engineering, materials, manufacturing, robotics, human factors, biosafety, environmental impact, reliability, cybersecurity and legal/compliance, depending on the candidate.

## 8. Output contract and non-claims

The module may report computational consistency within a declared domain and model envelope. It cannot certify that a molecule or genetic system is functional, safe, stable, clinically useful, environmentally acceptable or suitable for deployment.

Every output includes exact model/tool versions, input digests or references, evidence provenance, uncertainty, limitations, safety metadata, required reviewers and explicit non-claims. No reviewer response, missing module, timeout or model consensus is interpreted as approval.

## 9. Integration

The parent YJ64 coordinator owns task lifecycle, dependency graph, policy enforcement, review routing and acceptance decisions. This module implements specialist semantics only. It must use shared versioned contracts and must not fork the universal task lifecycle or create a parallel registry.

Biological Engineering remains a separate sibling module. Molecular/genetic candidate outputs may be consumed by it, but neither module can certify the other's system-level results. The Engineering Core's mandatory cross-module review protocol applies.

## 10. Implementation sequence

1. Establish typed, versioned candidate/evidence/review/enhancement contracts.
2. Add validation tests for provenance, origin identity, independent review, fail-closed acceptance and stale-review invalidation.
3. Add computational capability manifests with explicit applicability and safety metadata.
4. Add bounded, non-executing adapters for curated datasets and computational tools.
5. Add reproducibility records and benchmark harnesses.
6. Integrate through the existing universal task lifecycle and parent coordinator.
7. Keep wet-lab execution and permission expansion outside this repository's autonomous capabilities.
