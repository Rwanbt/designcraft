# Reproducible quality test execution

Target: `Rwanbt/designcraft`. PR base: `main`. Never push to `storytold/*` or merge the branch automatically.

## Required toolchain

Rust 1.95+ (edition 2024), Cargo, rustfmt and Clippy; optional `cargo-llvm-cov 0.6.24` with `llvm-tools-preview`. The workspace uses `Cargo.lock`. The existing `AGENTS.md` expects `cargo xtask ci`, which performs formatting, Clippy, tests, asset attribution, dependency layering and WASM checks.

Local runner is unavailable in the session that created this branch (`cargo` not installed, GitHub network DNS inaccessible). Therefore no local test pass is claimed.

## Reproduction commands

```sh
cargo fmt --all -- --check
cargo clippy -p designcraft-geom --all-targets --locked -- -D warnings
cargo test -p designcraft-geom --locked
cargo test --workspace --locked
cargo clippy --workspace --all-targets --locked -- -D warnings
cargo xtask layers
cargo xtask assets
cargo xtask stats --exact
# After installing the pinned cargo-llvm-cov and LLVM tools:
mkdir -p coverage
cargo llvm-cov -p designcraft-geom --locked --lcov --output-path coverage/geom.lcov
```

## CI jobs and independent scope

Workflow: `.github/workflows/quality.yml`. Pushes to `test/**` and `fix/**` trigger a lighter geometry matrix (Ubuntu, Windows, macOS). Draft PRs against `main` also trigger full Linux workspace tests/Clippy/architecture/asset checks and a geometry WASM check. The Linux geometry job uploads `geometry-lcov` for 30 days.

A report is accepted only when linked to an exact SHA and completed workflow run, with test counts, failing logs if applicable, and the raw LCOV artifact. Keep PR as draft until all applicable checks and risks are resolved.

First push-triggered run: https://github.com/Rwanbt/designcraft/actions/runs/38267656139 (started after `c360bc910f3d5c592dbe127ba7c501935cb3ea0e`; inspect its conclusion rather than assuming success).

## Failure policy

A red check requires inspecting the failing job logs and correcting the root cause. Never adjust coverage thresholds arbitrarily, remove a test to obtain green, or treat skipped E2E/full workspace as a pass. Independent oracles, real binary smoke tests, fuzzing, workspace coverage, and Windows/macOS desktop checks remain future deliverables.

## Confirmed executions

- [PR validation 38268165029](https://github.com/Rwanbt/designcraft/actions/runs/38268165029), `0dff87b1`: **success**. Rust workspace Linux 1,155 passing, 0 failing, 3 ignored; LLVM geometry only on separately measured runs; wasm geom and cross-platform geometry green.
- [Geometry follow-up 38270010377](https://github.com/Rwanbt/designcraft/actions/runs/38270010377), `0a0d7ad0`: Linux/Windows/macOS geometry green; 60 geometry tests; LCOV lines 1,753/1,841 (95.22%). CI on this push **did not execute full workspace or CLI E2E**; PR-triggered work is required.
