# YJ64 Molecular & Genetic Engineering

Independent computational module for molecular and genetic engineering research within the YJ64 ecosystem.

## Scope
- Evidence-indexed molecular components, structures and interactions.
- Computational molecular structure/function and interaction analysis.
- Typed representation and analysis of genetic systems.
- Phenotype, stability and unintended-effect prediction with explicit uncertainty.
- Provenance, reproducibility, evidence maturity and biosafety metadata.
- Independent cross-disciplinary review and enhancement contributions.

## Boundaries
This repository does not implement autonomous wet-lab execution, synthesis, transformation, culturing, release or deployment. Computational predictions are not proof of function, safety or stability. Requests involving increased pathogenicity, transmissibility, host range, immune evasion, uncontrolled persistence or resistance to containment are outside scope and must be stopped and referred to qualified governance.

## Architecture
- `src/yj64_molecular_genetic/contracts.py`: versioned candidate, evidence, review and enhancement contracts.
- `docs/ARCHITECTURE.md`: module boundary, evidence model, safety gates and integration.
- `tests/`: contract validation tests.

The module is independent from Biological Engineering and YJ64 Engineering Core. It integrates through shared versioned contracts; it does not create a parallel task lifecycle or certify system-level acceptability.

## Development
Python 3.11+. Install development dependencies with `pip install -e ".[dev]"` and run `pytest`.

No wet-lab automation or execution capability is provided by this package.
