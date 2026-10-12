# Residual risks and integration blockers

As of 2026-10-12, DesignCraft is **PARTIALLY VERIFIED** as a test-improvement exercise; it has **not** been demonstrated production-ready.

| Priority | Risk | Evidence | Required gate |
|---|---|---|---|
| P0 | Ruler tick computation may hang on zero or negative zoom | `crates/geom/src/units.rs` previously increased major tick width in an unbounded loop; regression test introduced in this branch | Validated: 60 geometry tests on Linux/Windows/macOS and LLVM line coverage at 95.22%; re-run at final PR SHA |
| P1 | Save/recovery integrity and document corruption under malformed files | Complex document and recovery code with existing tests; no full post-change run verified yet | Workspace tests, fault-injected file roundtrips, fuzzing |
| P1 | Untrusted document imports, rendering, export | IDML/PDF/EPUB/image handlers present, lack of measured branch coverage | Malformed fixture suite, parser fuzzing, independent export oracles |
| P1 | Broad application regressions | Existing CI is weighted to release, packaging and platform builds; initial branch adds first general quality workflow | Successful full workspace job, then E2E native and browser tests |
| P1 | Unknown code coverage | No existing instrumented per-package baseline obtained | Examine geom LCOV, then instrument every applicable crate |
| P2 | Cross-platform GUI behavior | Geometry is cross-platform tested; full GUI not yet tested | Windows/macOS native binary smoke, Windows ARM64 E2E, Linux desktop and browser checks |
| P2 | Fork synchronization and protected integration | `main` was 19 commits behind upstream and had no branch protection at initial inspection | Review changes explicitly; configure repo protections separately, no automatic merges |
| P2 | Flaky tests, network corpora, input-dependent timing | Existing tests and corpus requirements need systematic runner observation | Repeat seeded tests, pinned corpora, predictable clocks and timeouts |

The new zoom test guards finite tick calculations and invalid-scale fallback. Its normal-scale behavior is already covered by pre-existing ruler tests. The fix does not establish end-to-end rendering correctness.

Open no upstream PR, change no upstream repository, perform no force-push, and keep the fork PR in **draft** pending complete validation.

## Positive validation boundaries

At `0dff87b1`, a full Linux workspace test run succeeded (1,155 pass, 3 ignored), along with Clippy, dependency-layer and assets checks. At `0a0d7ad0`, 60 geometry tests and LCOV succeeded. Neither result certifies the unexecuted new CLI save/reopen assertion; it must run in the final draft PR. The product remains **PARTIALLY VERIFIED**.
