# Feature-to-test traceability — initial risk inventory

Snapshot: `Rwanbt/designcraft`, base `main@16a7365701f9ce8f93ca77a27a8dc2fffb807869`. These statuses distinguish the existence of source tests from verified execution. No subsystem is product-certified solely because tests exist.

| ID | Functional contract / component | Known test surface | Current validation | Missing proof / next action |
|---|---|---|---|---|
| GEO-001 | Units, measurement parsing, ruler tick generation; `crates/geom` | Inline tests in `units.rs`, new invalid/extreme zoom regression | PARTIAL | Check Linux, Windows, macOS and measured geom LCOV on exact SHA |
| GEO-002 | Path editing, geometry, snapping and hit testing; `crates/geom`, `crates/tools` | In-source tests and `crates/tools/src/tests.rs` | UNVERIFIED | Edge cases and property-based contracts |
| DOC-001 | Page/item/story editing, persistent document state and undo/redo; `crates/doc`, `crates/engine` | `src/tests.rs`, engine command modules | UNVERIFIED | Full workspace tests; roundtrip save and reload with reference assertions |
| TEXT-001 | Paragraph composition, bidi, hyphenation, tables; `crates/compose` | `src/tests.rs` and in-module tests | UNVERIFIED | Golden behavior, boundary and shaping-platform cases |
| FORMAT-001 | Native document, IDML import/export, EPUB, DOCX/RTF/XLSX; `format`, `idml`, `epub`, `textimport` | IDML tests and format module tests | UNVERIFIED | Independent oracle corpus; corruption, ZIP bounds, roundtrips |
| EXPORT-001 | PDF export / preflight / print; `crates/pdf` and engine export commands | `src/tests.rs` and tests under `crates/pdf/tests` | UNVERIFIED | Semantic inspection and malformed-data tests |
| RENDER-001 | Image decode, text, effects, raster rendering; `images`, `render` | Image and rendering tests, golden images | UNVERIFIED | Golden stability across operating systems and hardware |
| CLI-001 | Headless command script, file saves and export; `apps/designcraft-cli` | `apps/designcraft-cli/tests/cli.rs` | UNVERIFIED | Execute CLI against real binary; inspect output bytes |
| MCP-001 | MCP/control commands and structured errors; `crates/mcp` | `crates/mcp/src/tests.rs` | UNVERIFIED | Transport errors, timeouts, malformed inputs, permission boundaries |
| UI-001 | Desktop panels, menus, docking, interaction; `crates/ui-egui`, `apps/designcraft` | `panel_docking_tests.rs` and module tests | UNVERIFIED | Real app smoke + UI automation with persisted workspace and dialogs |
| WEB-001 | WASM app and browser behavior; `apps/designcraft-web` | Browser-policy source and web application | UNVERIFIED | Actual browser E2E, responsive, JS errors; full WASM build |
| RECOVERY-001 | Crash recovery, protected document copies; `crates/engine/src/recovery.rs` | Recovery test module | UNVERIFIED | Concurrent sessions, interrupted writes and symlink/path attacks |

Status policy: VERIFIED = expected contract asserted in passing, applicable CI on the reviewed SHA; PARTIAL = partial observed coverage; UNVERIFIED = implementation or tests found but the requisite end-to-end evidence is absent; BLOCKED = runner/service unavailable.
