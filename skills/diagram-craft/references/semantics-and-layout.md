# Semantics and layout

Read the section matching the reader's question. These contracts apply to custom SVG, Mermaid, and editor-native diagrams.

| Reader's question | Representation | Preserve |
|---|---|---|
| What talks to what? | Architecture/data flow | Direction, payload/action, boundaries, sync/async |
| Where does it run? | Deployment | Environments, instances, hosts, replicas; separate from logical modules |
| What happens next? | Flowchart | Branch conditions, terminal outcomes, loops, exceptions |
| Who hands work to whom? | Swimlanes | Ownership, handoffs, waits; lanes do not imply parallelism |
| In what order do messages happen? | Sequence | Actors, message direction, guards, alternatives, concurrency |
| What can this thing become? | State machine | Events, guards, effects, initial/terminal states |
| How are records related? | ER/schema | Cardinality, optionality, keys, logical versus physical |
| What depends on what? | Dependency graph | Declare “uses” versus “is required by”; retain cycles |
| What changed structurally? | Before/after map | Stable identity, changed nodes/edges |
| What contains or owns what? | Tree/nested groups | Single parent per child in a tree; cross-links need a graph |
| What reinforces what? | Causal loop | Known polarity/delays; influence versus transfer |
| When did it happen? | Timeline | Date spacing versus explicitly ordinal sequence |

For numeric magnitude, distribution, correlation, or measured trends, use a chart workflow with honest scales and units. A Sankey needs quantities and conservation assumptions. A stage funnel is not measured conversion without counts. A quadrant needs defined axes and an honest placement basis. Do not invent precision to fill a visual.

## Architecture, data flow, deployment

Start from concrete interfaces and ownership boundaries. Label edges with verbs/payloads rather than vague “connects”. Explain whether an arrow means request, return, stored record, dependency, or event.

A service is not a machine; a module is not necessarily independently deployed; a cloud logo is not hosting evidence. Containment does not prove trust. Derive boundaries from enforcement or mark them proposed. Separate logical structure from deployment unless the question needs both.

Put sources/consumers along a clear reading direction and stores near their accessing component. Route feedback/failure around the main path. If a queue changes delivery semantics, show it rather than drawing direct delivery. Configuration proves a declared dependency, not production health or observed runtime behavior.

## Flows and swimlanes

Use actions for process nodes and questions/guards for decisions. Label outgoing branches with distinct conditions; do not imply exhaustive yes/no when null, timeout, or cancellation exists. Attach exceptions to the failing operation. Retries need a destination and a stopping condition when known.

Choose lanes when responsibility is central. Put actions under owners and show cross-lane handoffs. Show known parallel work with fork/join or explained notation, not merely neighboring columns. Label waits as waits.

## Sequences and states

Sequence time advances on one axis. Call and return differ in style/direction. Asynchronous messages need not block the sender. Use guarded alternative/optional frames, loops, and known parallel frames. Keep self-calls visible. Numbering cannot correct an inaccurate order. Reserve a clear band for fragment headings and guards; inspect them against lifelines and messages because generic text-containment checks do not detect every intersection.

State nodes name persistent conditions, not actions. Transitions name the event and, if needed, `[guard] / effect`. Distinguish unreachable, terminal, and failure states. Do not infer transitions merely because two states appear in source. Hierarchical states are containment; crossing transitions need defined meaning.

## ER, schemas, UML

Separate logical entities from physical tables. Include field types/constraints only when supported. A foreign key alone does not establish mandatory participation on both ends; derive optionality and cardinality from constraints and behavior. Explain unusual notation. Align physical FK connectors to corresponding fields.

Use conventional UML generalization/composition/aggregation/dependency symbols only when the semantics apply. Composition implies lifecycle ownership; a generic “has” does not establish it. Include methods/signatures relevant to the reader without turning the diagram into a code listing.

## Comparison and simplification

Align matching IDs in before/after views; preserve positions and scale unless movement is the change. Keep an added/removed/changed/rewired ledger. Don't recolor every object when only two changed. Attribute-only comparisons usually fit a table unless the user requested a diagram.

Give overview groups stable IDs and link details. Explain collapsed internals; keep boundary inputs/outputs accurate. A summarized retry loop can point to a detail view, but cannot become an unconditional straight line.

When refining, distinguish correctness defects from presentation defects. Preserve terminology and intentional notation. Record semantic changes with evidence. Surface material conflicts between source and request rather than silently picking the convenient model.
