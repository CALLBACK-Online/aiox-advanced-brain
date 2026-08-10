# Benchmark Runtime

```yaml
id: benchmark-runtime
name: "Benchmark Runtime"
role: "Worker for deterministic preparation, local_docs setup and report publication"
tier: worker
specialty: "Filesystem preparation, normalization, artifact persistence"
executor_type: Worker
human_in_the_loop: true
```

## Purpose

The Benchmark Runtime is the **Worker executor** in the AIOX Four-Executor model for the spy squad. Handles deterministic, non-cognitive operations: local_docs preparation, file normalization, artifact persistence, and report publishing.

## Responsibilities

- Prepare benchmark local_docs (directory creation, cleanup)
- Normalize subject slugs and file names
- Persist artifacts to correct output paths
- Execute shell scripts for filesystem operations
- Clean up temporary clones after codebase benchmarks

## Activation

This agent activates when:
- `bench-report-publish` needs to persist artifacts deterministically
- `prepare-benchmark-environment.sh` is called for benchmark environment setup
- `publish-benchmark-report.sh` is called for report publication
- Post-pipeline cleanup is required

## Executor Profile

| Field | Value |
|-------|-------|
| AIOX Type | Worker |
| Human-in-the-Loop | true |
| Output Schema | runtime-execution-report |
| Can Execute | true (deterministic only) |
| Can Review | false |

## Scripts

- `scripts/prepare-benchmark-environment.sh` — benchmark environment setup
- `scripts/publish-benchmark-report.sh` — report publication

## AIOX Mandamentos Compliance

- M1 (One Executor per Task): Worker handles deterministic publishing tasks
- M4 (No Invention): Worker only persists what was produced, never generates content

_benchmark-runtime v1.0.0 | spy squad_
