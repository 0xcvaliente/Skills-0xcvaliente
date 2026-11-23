# Semantics and layout

Read the section matching the reader's question. These contracts apply to custom SVG, Mermaid, and editor-native diagrams.

| Reader's question | Representation | Preserve |
|---|---|---|
| What talks to what? | Architecture/data flow | Direction, payload/action, boundaries, sync/async |
| Where does it run? | Deployment | Environments, instances, hosts, replicas; separate from logical modules |
| What happens next? | Flowchart | Branch conditions, terminal outcomes, loops, exceptions |
| What are the steps, in order? | Numbered stage rail | Order only: no time scale, branches, or owners; no arrows between neighbors |
| Who hands work to whom? | Swimlanes | Ownership, handoffs, waits; lanes do not imply parallelism |
| In what order do messages happen? | Sequence | Actors, message direction, guards, alternatives, concurrency |
| What can this thing become? | State machine | Events, guards, effects, initial/terminal states |
| Which request records which fact, and what view shows it? | Event model | Command, event, read model per stage; stated links only; order, not duration |
| How are records related? | ER/schema | Cardinality, optionality, keys, logical versus physical |
| What depends on what? | Dependency graph | Declare “uses” versus “is required by”; retain cycles |
| Which task chain sets the finish, and where is the slack? | Schedule network (activity on node) | Durations in one stated unit, finish-to-start links, derived early/late times, total float, every tied critical chain |
| Is each requirement met and checked? | Traceability matrix | Source, requirement, satisfying design, verifying check by ID; printed gaps |
| What changed structurally? | Before/after map | Stable identity, changed nodes/edges |
| What does the customer see versus what stays hidden? | Service blueprint | Stage order, customer/frontstage/backstage/support layers, the line of visibility |
| What contains or owns what? | Tree/nested groups | Single parent per child in a tree; cross-links need a graph |
| What reinforces what? | Causal loop | Known polarity/delays; influence versus transfer |
| Which branch got each commit, and where did branches split and join? | Git graph (not a timeline or swimlane) | One lane per branch, one shared column order, merges as two-parent commits, tags on existing commits |
| When did it happen? | Timeline | Date spacing versus explicitly ordinal sequence |

For numeric magnitude, distribution, correlation, or measured trends, use a chart workflow with honest scales and units. A Sankey needs quantities and conservation assumptions. A stage funnel is not measured conversion without counts. A quadrant needs defined axes and an honest placement basis. Do not invent precision to fill a visual.

## Architecture, data flow, deployment

Start from concrete interfaces and ownership boundaries. Label edges with verbs/payloads rather than vague “connects”. Explain whether an arrow means request, return, stored record, dependency, or event.

A service is not a machine; a module is not necessarily independently deployed; a cloud logo is not hosting evidence. Containment does not prove trust. Derive boundaries from enforcement or mark them proposed. Separate logical structure from deployment unless the question needs both.

Put sources/consumers along a clear reading direction and stores near their accessing component. Route feedback/failure around the main path. If a queue changes delivery semantics, show it rather than drawing direct delivery. Configuration proves a declared dependency, not production health or observed runtime behavior.

### Containment scopes

Use nesting only when the hierarchy itself is the claim (what sits inside which scope), and draw each level with an inset, a label, and a visibly different fill so the nesting reads. Keep two kinds of scope distinct and never interchange them:

- **Administrative scope** (account, subscription, project, tenant): billing, permission, and lifecycle ownership. It carries no traffic, so draw it as a wide band or outer frame, not as a network boundary.
- **Traffic scope** (network, subnet, security group, cluster namespace): a boundary that traffic crosses only under an explicit rule. Draw it as a box and derive it from enforcement (rules, policies) or mark it proposed.

Place a managed service (hosted database, queue, object store) in the administrative scope that owns it, not inside a traffic scope. What belongs inside the subnet is the private endpoint or client that reaches it. Drawing the service itself in the subnet claims it sits behind that subnet's rules. Draw peering or other cross-scope paths as labeled connectors between the two traffic scopes they join. Give every scope and node a single immediate parent in the evidence ledger. If a flat zone label ("VNET / SNET-APP") would hide a real hierarchy, nest; if nesting adds nothing, keep zones flat and few.

### Service blueprints

A service blueprint shows how a service is delivered across stages: stages run left to right as equal columns, and layers run top to bottom: optional physical evidence, customer actions, frontstage actions (visible staff or product), backstage actions (work the customer cannot see), and optional support processes. The **line of visibility** between frontstage and backstage is the load-bearing element: draw it heavier than the other dividers and keep every cell on the correct side of it. Lighter dividers can mark the lines of interaction (customer to frontstage) and internal interaction (backstage to support).

Put one action per stage per layer, and write an explicit "none" or "not applicable" in an empty required cell rather than leaving a hole. Waits and system names belong in cell text. Do not turn it into a swimlane: lanes show who hands work to whom with arrows, while a blueprint is a stage-by-layer census. Use a journey map when the point is sentiment with no backstage, a swimlane when ownership and handoff arrows are the claim, and a process flow when the data payloads matter. Emphasize no more than a single cell, the one that carries the point of the figure, such as a breakdown, delay, or transfer between layers. Backstage actions and timings come from observed operations or are labeled inferred or proposed; never invent them to fill a grid. The helper does not render this notation; author it in SVG/HTML with a layer and stage attribute on each cell so the drawing can be compared with its ledger.

## Flows and swimlanes

Use actions for process nodes and questions/guards for decisions. Label outgoing branches with distinct conditions; do not imply exhaustive yes/no when null, timeout, or cancellation exists. Attach exceptions to the failing operation. Retries need a destination and a stopping condition when known.

Choose lanes when responsibility is central. Put actions under owners and show cross-lane handoffs. Show known parallel work with fork/join or explained notation, not merely neighboring columns. Label waits as waits.

A short method with no branches (a playbook, an onboarding path, a "how it works" explainer) can be a single numbered rail: one equal segment per stage, each with a title and one brief line. Equal spacing claims order and nothing else, so the rail needs no arrows between neighbors. Move to a timeline when dates matter, a flowchart when the path forks, and swimlanes when ownership does.

An event model lays ordered stages left to right across three lanes: the command (a request, named as an imperative), the event it records (a fact, named in the past tense), and the read model built from it (a view, not another event). Draw command-to-event and event-to-view links only where the source states them, and label an unknown link as a gap. The figure does not show an event store, broker, persistence, or delivery guarantee unless evidence does; stage spacing is order, not duration, and a branching scenario belongs in a flowchart or separate views.

## Sequences and states

Sequence time advances on one axis. Call and return differ in style/direction. Asynchronous messages need not block the sender. Use guarded alternative/optional frames, loops, and known parallel frames. Keep self-calls visible. Numbering cannot correct an inaccurate order. Reserve a clear band for fragment headings and guards; inspect them against lifelines and messages because generic text-containment checks do not detect every intersection.

State nodes name persistent conditions, not actions. Transitions name the event and, if needed, `[guard] / effect`. Distinguish unreachable, terminal, and failure states. Do not infer transitions merely because two states appear in source. Hierarchical states are containment; crossing transitions need defined meaning.

## Git graphs

Branch and merge history (how a team branches, where a release was cut, which fix was carried back, merge compared with rebase) needs ancestry, which a timeline cannot fork and swimlanes would misread as ownership. Give each branch its own horizontal lane, trunk on top and named at its left end, and put every commit on a single column grid that all lanes share: a column is a step in commit order, the same on every lane, not a date, and an unused column keeps its width. A merge is a commit in its own right with exactly two parents, each in an earlier column and the two on different lanes; a line that joins two rails without such a commit asserts nothing. Draw each edge as a right-angled elbow that only ever moves rightward. A new branch leaves its parent commit vertically, in that commit's column, to reach its own lane, then runs along it; a merge follows the lane it comes from, then bends up or down into the merge commit in that commit's column. Two edges never share a straight run, and an edge never runs along a lane it does not connect. A tag is a small label on a commit that already exists, never an extra lane or dot. Name only the commits the figure's point depends on (the merge, the fix, the release) and leave the rest unlabelled. All lanes share one neutral stroke and are told apart by name; the accent marks two commits at most. Derive the horizontal pitch from the highest column index so the rightmost commit stays inside the canvas, and when that pitch is too tight for labels or merge marks, split the figure into an overview and a zoomed detail. Commits, parents, and tags come from the repository or the stated source; an illustrative history says so. The helper neither renders nor checks this notation.

## ER, schemas, UML

Separate logical entities from physical tables. Include field types/constraints only when supported. A foreign key alone does not establish mandatory participation on both ends; derive optionality and cardinality from constraints and behavior. Explain unusual notation. Align physical FK connectors to corresponding fields.

Use conventional UML generalization/composition/aggregation/dependency symbols only when the semantics apply. Composition implies lifecycle ownership; a generic “has” does not establish it. Include methods/signatures relevant to the reader without turning the diagram into a code listing.

## Schedule networks

Use a schedule network when the source gives task durations and which task must finish before another starts, and the reader asks what sets the end date. It is a dependency graph with arithmetic, so the graph must be acyclic and the arithmetic must be visible: each task box prints its duration, earliest and latest start and finish, and total float. Derive these, never estimate them. A forward pass starts each task at the latest early finish among its predecessors (zero when it has none); a backward pass from the project finish ends each task at the earliest late start among its successors; total float is late start minus early start. Zero-float tasks are critical. A link is critical only when both of its tasks are and the successor starts exactly when the predecessor finishes, so a shortcut between two critical tasks may not be. Show every tied critical chain, and mark the critical set with line weight instead of an accent per task.

Recompute after every edit and compare the printed numbers with the recomputation; a correct drawing of wrong numbers is still wrong. State the unit, the zero origin, and that box size and spacing are not a time scale. Durations and links come from the source. Lag, calendars, resource limits, deadlines, and probabilistic estimates are outside this simple model: name them as omitted instead of folding them in, and do not turn elapsed durations into calendar dates without real calendar rules. Use a dated timeline or Gantt chart when calendar overlap matters and a plain dependency graph when there are no durations. The helper neither computes nor renders this notation.

## Traceability

Give each requirement a row: where it came from, the design element that satisfies it, and the check (test, inspection, review) that verifies it, each named by a stable ID. Put the relationship in the column heading or the label so its direction does not depend on arrow placement. When the evidence has no link, print the gap ("no verifying check") rather than leaving a blank cell or inventing one. A shared ID or a design-to-test arrow does not show that the test verifies the requirement, and an illustrative example must say so. Many-to-many traces usually read better as a table or an overview plus detail.

## Comparison and simplification

Align matching IDs in before/after views; preserve positions and scale unless movement is the change. Keep an added/removed/changed/rewired ledger. Don't recolor every object when only two changed. Attribute-only comparisons usually fit a table unless the user requested a diagram.

Give overview groups stable IDs and link details. Explain collapsed internals; keep boundary inputs/outputs accurate. A summarized retry loop can point to a detail view, but cannot become an unconditional straight line.

When refining, distinguish correctness defects from presentation defects. Preserve terminology and intentional notation. Record semantic changes with evidence. Surface material conflicts between source and request rather than silently picking the convenient model.
