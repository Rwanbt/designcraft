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
| Whole workspace | **80.41% (67,637/84,117)** at `699e0285` | Unknown | Unknown | **243 files instrumented on Linux; baseline established** |
| `designcraft-geom` | 92.14% (1,641/1,781) on `c360bc91`; **95.22% (1,753/1,841)** on `0a0d7ad0` | Unknown | Unknown | Measured via LLVM LCOV, 60 tests passed on latest |
| Desktop UI, web UI, CLI | Unknown | Unknown | Unknown | Not measured |
| Import/export and renderer | Unknown | Unknown | Unknown | Not measured |

The workspace baseline is from [Actions run 38272759915](https://github.com/Rwanbt/designcraft/actions/runs/38272759915), commit `699e02850c2323ca5d5f5fa1183ca8e14580bcfc`, measuring **67,637/84,117 = 80.41%** across 243 Rust files. This was measured before the later recovery hardening and command roundtrip tests; a new exact-HEAD run is needed before any updated percentage is claimed. Its downloadable artifact is `workspace-lcov` (LCOV plus JSON summary). Branch/function coverage remains unmeasured.

The first instrumented command is `cargo llvm-cov -p designcraft-geom --locked --lcov --output-path coverage/geom.lcov`, run by `quality.yml` on Ubuntu. Its uploaded artifact is named `geometry-lcov`; it must be inspected before writing a percentage. It is **not** a workspace-wide percentage. No global coverage threshold is enforced without a measured workspace baseline. The geom measurements use the same LLVM LCOV workflow but distinct source revisions: a change in the denominator is expected after adding tests.

## Evidence and interpretation

GitHub Actions: https://github.com/Rwanbt/designcraft/actions/workflows/quality.yml

Base commit was 19 upstream commits behind `storytold/designcraft:main` when checked. The fork baseline is intentionally not updated during the quality experiment.

`cargo fmt`, Clippy, tests, coverage collection, and native/web platform checks must be evaluated **per exact head SHA**. A successful geom job cannot certify the entire product. No binary GUI E2E test is included in this first batch.

To update this baseline: record the run ID, SHA, collected test count and instrumented numerator/denominator from the artifact; then expand coverage by crate without averaging incompatible measurement universes.

## Verified CI results and scope

- Geometry first measured run [38267656139](https://github.com/Rwanbt/designcraft/actions/runs/38267656139) (`c360bc91`): **54 passed**, 0 failed; Linux/Windows/macOS jobs green; LLVM **1,641/1,781 = 92.14%** lines.
- Initial PR run [38268165029](https://github.com/Rwanbt/designcraft/actions/runs/38268165029) (`0dff87b1`): workspace Linux **1,155 passed**, 0 failed, **3 ignored** across 47 harness result groups; Clippy, assets, layering and geometry WASM passed. Full workspace LCOV still **unmeasured**.
- Geometry follow-up run [38270010377](https://github.com/Rwanbt/designcraft/actions/runs/38270010377) (`0a0d7ad0`): **60 passed** on Linux (Windows/macOS geometry jobs also passed); LLVM **1,753/1,841 = 95.22%**. Full workspace/CLI E2E jobs skipped on push: their success must be verified after PR branch update.

## Full workspace coverage execution

- Command: `cargo llvm-cov --workspace --locked --lcov --output-path coverage/workspace.lcov` on Ubuntu 24.04.
- [Run 38272759915](https://github.com/Rwanbt/designcraft/actions/runs/38272759915), exact SHA `699e0285`: **67,637 covered / 84,117 instrumented**, **80.41%** over 243 source files.
- This is the first reproducible workspace-wide line baseline; no policy currently asserts 100% or mixes line, function and branch coverage.
- The new `.github/workflows/workspace-coverage.yml` preserves LCOV artifacts for 30 days and runs on internal PRs (and by dispatch; weekly only after main integration).
