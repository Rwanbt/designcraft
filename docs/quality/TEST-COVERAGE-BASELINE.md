# Test and coverage baseline — DesignCraft fork

Measurement date: 2026-10-12 (Europe/Paris).
Repository: `Rwanbt/designcraft`; base: `main` at `16a7365701f9ce8f93ca77a27a8dc2fffb807869`.
Working branch: `test/quality-baseline-ruler-guard-20261012`.

## Source inventory

- 20 workspace package manifests beneath `apps/`, `crates/` and `xtask/`: 16 library crates, 3 applications (desktop, web, CLI), and 1 xtask package.
- 29 specifically named Rust test source files under `tests/`, `src/tests*.rs`, or `*_tests.rs` at the base SHA, **not** the number of collected test cases.
- Inline `#[test]` and module tests exist elsewhere. The actual runner count remains **unmeasured** until `cargo test --workspace -- --list` or `cargo xtask stats --exact` completes.
- Existing release/platform workflows do not establish a complete PR quality baseline.

## Instrumented metrics

| Scope | Line coverage | Branch coverage | Function coverage | Status |
|---|---|---|---|---|
| Whole workspace | Unknown | Unknown | Unknown | Not measured |
| `designcraft-geom` | Awaiting artifact | Unknown | Unknown | Instrumentation introduced |
| Desktop UI, web UI, CLI | Unknown | Unknown | Unknown | Not measured |
| Import/export and renderer | Unknown | Unknown | Unknown | Not measured |

The first instrumented command is `cargo llvm-cov -p designcraft-geom --locked --lcov --output-path coverage/geom.lcov`, run by `quality.yml` on Ubuntu. Its uploaded artifact is named `geometry-lcov`; it must be inspected before writing a percentage. It is **not** a workspace-wide percentage. No coverage threshold is enforced before a valid baseline.

## Evidence and interpretation

GitHub Actions: https://github.com/Rwanbt/designcraft/actions/workflows/quality.yml

Base commit was 19 upstream commits behind `storytold/designcraft:main` when checked. The fork baseline is intentionally not updated during the quality experiment.

`cargo fmt`, Clippy, tests, coverage collection, and native/web platform checks must be evaluated **per exact head SHA**. A successful geom job cannot certify the entire product. No binary GUI E2E test is included in this first batch.

To update this baseline: record the run ID, SHA, collected test count and instrumented numerator/denominator from the artifact; then expand coverage by crate without averaging incompatible measurement universes.
