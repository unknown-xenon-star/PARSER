# CodeFlow Visualizer

**Start Date:** March 18, 2026
**Tagline:** Turning large, chaotic codebases into understandable, interactive maps.
**Description:** CodeFlow Visualizer is a developer tool that parses local TypeScript and Python repositories, builds a directed graph of imports and function calls, and renders that graph in an interactive web UI for exploration, debugging, and architecture analysis.

## 🧭 Suggested Structure

```text
codeflow-visualizer/
├── docs/
│   ├── scope.md
│   ├── architecture.md
│   ├── roadmap.md
│   └── benchmarks.md
├── parser/
│   ├── index.ts
│   ├── ts/
│   └── python/
├── graph/
│   ├── index.ts
│   ├── nodes.ts
│   └── edges.ts
├── insights/
│   ├── index.ts
│   ├── circular-deps.ts
│   ├── hotspots.ts
│   └── dead-code.ts
├── server/
│   ├── index.ts
│   └── routes/
├── client/
│   ├── src/
│   └── package.json
└── tests/
    ├── fixtures/
    ├── parser/
    ├── graph/
    └── integration/
```

## 🔗 Key References

- [Scope](Scope.md)
- [Architecture](./docs/architecture.md)
- [Benchmarks](./docs/benchmarks.md)
- [Parser](./parser/index.ts)
- [Graph](./graph/index.ts)
- [Insights](./insights/index.ts)
- [Server](./server/index.ts)
- [Client](./client/src)
- [Tests](./tests)

## 🚀 Phase-Based Roadmap

### Phase 0: Scope & MVP

- [ ] Define MVP boundaries in [Scope](Scope.md)
- [ ] Confirm supported languages for v1: TypeScript and Python
- [ ] Define repository size target and acceptable processing time
- [ ] Agree on graph primitives in [Architecture](./docs/architecture.md)
- [ ] Set initial success criteria for parsing accuracy and UI responsiveness
- [ ] Prioritize single-repo local analysis before multi-repo support

### Phase 1: Code Parsing (AST Extraction)

- [ ] Implement entry points in [Parser](./parser/index.ts)
- [ ] Add TypeScript AST extraction under [Parser](./parser/index.ts)
- [ ] Add Python AST extraction under [Parser](./parser/index.ts)
- [ ] Extract files, modules, imports, exported symbols, and function declarations
- [ ] Extract call expressions with source file and location metadata
- [ ] Normalize parser output into a shared intermediate representation
- [ ] Add parser fixtures in [Tests](./tests)

### Phase 2: Graph Modeling (Nodes and Edges)

- [ ] Implement graph core in [Graph](./graph/index.ts)
- [ ] Define node types: repository, module, class, function, symbol
- [ ] Define edge types: imports, calls, contains, references
- [ ] Add stable IDs for cross-file linking and deduplication
- [ ] Support graph serialization for API transport and snapshot testing
- [ ] Validate graph integrity with graph-focused tests in [Tests](./tests)

### Phase 3: Visualization MVP (D3.js or React Flow)

- [ ] Choose rendering baseline in [Client](./client/src)
- [ ] Build a graph viewer with pan, zoom, and node selection
- [ ] Add filtering by file, symbol type, and edge type
- [ ] Show import and call relationships on node click
- [ ] Connect [Server](./server/index.ts) to graph data endpoints
- [ ] Provide an initial architecture map for medium-sized repos

### Phase 4: Insights (Circular Deps, Hotspots, Dead Code)

- [ ] Implement insight orchestration in [Insights](./insights/index.ts)
- [ ] Detect circular dependencies in [Insights](./insights/circular-deps.ts)
- [ ] Identify hotspots by fan-in, fan-out, and change-prone proxy metrics
- [ ] Surface likely dead code using unreachable or unreferenced symbols
- [ ] Expose insight summaries in the UI and API
- [ ] Add regression coverage for known edge cases in [Tests](./tests)

### Phase 5: Data Flow Tracking

- [ ] Extend parser output to capture assignments and parameter flow
- [ ] Model basic intra-function data flow between variables and calls
- [ ] Support source-to-sink path inspection for selected functions
- [ ] Highlight value propagation paths in the graph UI
- [ ] Document known precision limits in [Architecture](./docs/architecture.md)

### Phase 6: Performance & Bottlenecks

- [ ] Profile parse time, graph build time, and render time
- [ ] Add caching for unchanged files and incremental graph rebuilds
- [ ] Reduce UI rendering overhead for dense graphs
- [ ] Introduce graph clustering or collapsing for large repositories
- [ ] Track performance targets in [Benchmarks](./docs/benchmarks.md)

### Phase 7: Testing & Real-Repo Benchmarking

- [ ] Expand fixture coverage for tricky TS and Python patterns
- [ ] Add integration tests across parser, graph, insights, server, and client
- [ ] Benchmark against representative real repositories
- [ ] Record failures, unsupported syntax, and false positives in [Benchmarks](./docs/benchmarks.md)
- [ ] Define release gates for correctness, speed, and stability

### Phase 8: CLI & DX

- [ ] Add a CLI entry point for local repository scanning
- [ ] Support commands for parse, build-graph, serve, and export
- [ ] Add output formats such as JSON snapshots and report summaries
- [ ] Improve onboarding with local setup docs in [Scope](Scope.md)
- [ ] Add developer scripts for fixtures, profiling, and smoke tests
- [ ] Prepare the project for internal alpha usage

## ⚠️ Risks

- [ ] Graph complexity may make large repositories visually noisy and computationally expensive
- [ ] Static analysis limits may reduce accuracy for dynamic imports, reflection, decorators, metaprogramming, and runtime dispatch
- [ ] Cross-language symbol resolution may require strict normalization rules to avoid broken edges
- [ ] Performance bottlenecks may appear in both AST traversal and client-side graph rendering

## 🌱 Future

- [ ] VS Code Extension for in-editor graph exploration and symbol tracing
- [ ] AI-powered explanations for architectural hotspots, dependency chains, and suspicious dead code
- [ ] Multi-repo and monorepo-aware dependency views
- [ ] Historical graph diffs across commits or releases

## 💬 TPM Comments & Suggestions

- [ ] Keep the v1 scope narrow: local analysis, read-only behavior, TypeScript and Python only, and a single-repository workflow
- [ ] Prefer shipping a reliable import graph and basic call graph before attempting deep data flow or advanced semantic inference
- [ ] Treat graph correctness as more important than visual polish in early phases because trust is the product foundation
- [ ] Avoid promising full static accuracy for dynamic languages; position results as "best-effort analysis with transparent limits"
- [ ] Define one clear user outcome for MVP: "A developer can open a repo and understand module relationships within 5 minutes"
- [ ] Add screenshots and sample benchmark repos early so progress is visible to contributors and future users

## 🛠️ Recommended Development Stack

- [ ] Use `TypeScript` as the primary implementation language for parser orchestration, graph modeling, server, CLI, and shared contracts
- [ ] Use the `TypeScript Compiler API` for TS parsing and Python `ast` or `tree-sitter` bindings for Python parsing
- [ ] Use `Node.js` for the backend runtime to simplify local CLI, server, and client integration
- [ ] Use `React` with `React Flow` for the first UI iteration because it is faster to ship than a custom D3-only interaction layer
- [ ] Use `Fastify` or `Express` for lightweight local APIs; keep the server thin and stateless
- [ ] Use `Vitest` for unit tests and integration tests across parser and graph layers
- [ ] Use `Playwright` for UI smoke tests once the graph viewer is stable
- [ ] Use `pnpm` for workspace and package management if the project becomes a multi-package repo
- [ ] Use structured JSON output contracts between parser, graph, and UI to reduce coupling

## 👩‍💻 Developer Experience

- [ ] Add a one-command local start flow such as `pnpm dev` or `npm run dev`
- [ ] Provide fixture repositories in [Tests](./tests) so contributors can reproduce parser behavior quickly
- [ ] Add example outputs in [Benchmarks](./docs/benchmarks.md) to show what "correct enough" looks like
- [ ] Enforce formatting, linting, and type-checking in pre-commit or CI from the start
- [ ] Keep modules small and responsibilities explicit: parser extracts facts, graph resolves relationships, insights compute findings, UI renders state
- [ ] Add debug flags for parser traces, graph dumps, and timing metrics to shorten issue triage
- [ ] Document unsupported syntax and false positives instead of hiding them

## 🌱 Beginner Developer Guidance

- [ ] Label beginner-safe tasks such as fixture creation, docs updates, UI filters, and test case additions
- [ ] Add a contributor guide that explains AST basics, graph terminology, and how each subsystem fits together
- [ ] Create "good first issues" around isolated modules rather than core graph resolution logic
- [ ] Include sample before/after examples for parser output so new contributors can reason about correctness
- [ ] Avoid assigning deep static analysis work to beginner contributors without scaffolding and reference examples
- [ ] Pair advanced features with design notes in [Architecture](./docs/architecture.md) so contributors understand tradeoffs before coding

## 🧪 Suggested Delivery Approach

- [ ] Milestone 1 should end with parsing metadata from a small TS repo and rendering a static graph snapshot
- [ ] Milestone 2 should add live interaction, filtering, and stable graph serialization
- [ ] Milestone 3 should add first insights: circular dependencies and hotspot ranking
- [ ] Milestone 4 should focus on scaling, caching, and real-repo benchmarks before adding more intelligence
- [ ] Treat data flow tracking as an advanced phase that should not block MVP release
- [ ] Reserve AI-powered features until the deterministic graph pipeline is trusted and benchmarked

## 🎯 User Experience Principles

- [ ] Optimize for clarity over density; default views should reduce noise instead of exposing the full graph immediately
- [ ] Make first-run onboarding simple: choose a local repo, scan, see a usable graph, inspect a file or function
- [ ] Provide multiple zoom levels such as repository view, module view, and symbol view
- [ ] Add search early because graph navigation without search becomes frustrating on real projects
- [ ] Show why a node or edge exists with source file paths and line references whenever possible
- [ ] Use progressive disclosure for insights so users are not overwhelmed by warnings and metrics
- [ ] Keep visual language consistent: edge colors, node types, severity markers, and layout behavior should be predictable

## 📈 Practicality Notes

- [ ] Prioritize repositories in the small-to-medium range first; very large monorepos can distort early roadmap decisions
- [ ] Expect imperfect call-graph resolution for dynamic code and design the UI to communicate uncertainty
- [ ] Add exportable reports so the tool is useful even for users who do not want to live inside the graph UI
- [ ] Consider memory use as a first-class concern because graph-heavy apps can degrade quickly on developer laptops
- [ ] Keep the initial deployment model local-first to avoid privacy and source-code handling concerns
- [ ] Measure success with practical questions: Did the tool help a developer find architecture problems faster, onboard faster, or debug dependencies faster?