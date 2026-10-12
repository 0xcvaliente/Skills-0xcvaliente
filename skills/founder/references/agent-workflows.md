# Founder agents and automation

<!-- Adaptation notice: this workflow was rewritten and generalized for Founder Codex on 2026-10-07, and ported to Claude Code as `founder` on 2026-10-10, from anthropics/launch-your-agent, Copyright 2026 Anthropic PBC, Apache-2.0. The original license is retained in ../licenses/anthropics--launch-your-agent.txt; the pinned source is listed in sources.md. -->

Use when the founder asks to build an AI worker, automate a business workflow, or ship an agent product. This adapts the outcome-and-evaluation pattern from the upstream launch-your-agent workflow (see [sources](sources.md)) into a provider-neutral workflow. It does not require any vendor's managed-agent product.

## Define the actual job

Capture trigger, actor/audience, inputs and access, desired output, success criteria, allowed actions, cadence if requested, and business failure consequences. Start from the founder's chosen product and platform. Ask only for missing decisions that change the build.

Scope an end-to-end first version that delivers the core outcome. Include integrations essential to that outcome if available and authorized. Separate real capability limits, unavailable credentials/access, and intentionally deferred scope. For each deferred feature, record the mechanism and revisit trigger instead of vaguely promising “later.”

## Stage and build

Inspect existing code/configuration before creating a new workspace. Prepare the implementation, contracts, prompts, configuration, sample inputs, output format, launch instructions, and relevant evaluation before requesting unavailable credentials or permissions. Use supported secret storage; do not ask for keys in chat or print them in logs.

Choose tools and architecture from the actual job: deterministic code for stable transformations; a model for judgment or unstructured inputs; a bounded workflow where possible; a more open agent loop only when the task needs it. Do not add multiple agents, memory, a database, or a schedule merely because they are available. While building, subagents (if the host provides them) can take independent research or verification steps in parallel; that is a build aid, not a reason to give the shipped workflow multiple agents.

Verify current official provider APIs, capabilities, pricing, and model choices when needed. Pin versions/configuration for repeatability. Do not transplant a source repository's model names, CLI, payload, or token limits into another provider.

If a connector is unavailable, build a realistic input fixture or exact output payload when that advances the job. Make the boundary explicit: a mocked send is not a delivered message. If delivery is core, produce the exact message/ticket the connector will later send. Keep credentials and real IDs out of shareable artifacts.

## Evaluate outcomes, not just executions

Derive observable criteria from the requested result: factual/source accuracy, required fields, business calculation, useful format, task completion, permitted actions, cost, and latency when relevant. Use representative real cases with known outcomes when available, plus edge/failure cases and held-back cases appropriate to the risk. Label synthetic fixtures.

Run the workflow and inspect actual output against those criteria. A model grader can help, but verify critical facts/calculations and known expected behavior independently. A successful API response or an agent's own “done” claim is not proof of success. Record case, exact config/version, criterion, result, evidence, usage/cost, and limitations.

Fix the demonstrated failure, then rerun affected checks and enough regression cases to detect collateral damage. Bound retries, iterations, and resource spend proportionally to the task. Stop repeated blind retries; diagnose the error or surface the concrete blocker.

## External actions and operations

Respect existing user authorization. Where write/send/spend authority is missing, complete the reviewable artifact first and request the specific action. Use deduplication/idempotency or explicit outcome readback for operations that can duplicate commitments. Never retry an ambiguous payment or delivery without checking whether it happened.

For an authorized recurring workflow, use an available automation tool. Choose by durability: a host-provided scheduled-task or cloud-routine feature suits an unattended recurring job; an in-session repeat or loop feature runs only while the session stays open; system cron or the founder's own platform scheduler suits a local or production job. Define timezone, relative date windows, deduplication, meaningful notification conditions, ownership, cost/resource caps, and stop/recovery behavior. Confirm next run and exercise the relevant trigger when supported. Do not schedule a one-off workflow.

Hand off the implemented artifact, observed evaluation, unresolved constraints, operating owner, intervention path, and next version trigger. Explain what is actually live versus local, mocked, or proposed. Avoid claiming autonomy from a single demonstration.
