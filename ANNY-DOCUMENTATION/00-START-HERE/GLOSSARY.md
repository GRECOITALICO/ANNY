# Glossary

All terms used in the ANNY organizational system, explained simply.

## Audit

A formal review of actions, decisions, and evidence to verify compliance with rules and procedures.

## Authority

The permission to perform specific actions. Authority flows downward: L0 has full authority, L1 has department authority, L2 has execution authority. Authority is never self-assigned.

## Canonical State

The official, authoritative state of the organization as recorded in the Git repository. If there is a conflict between any other source and the canonical state, the canonical state wins.

## Certification

A formal declaration by L0 that a piece of work meets all requirements. Only L0 can certify. Certification requires complete evidence.

## Delegation

The act of assigning a task or mission from a higher authority to a lower one. L0 delegates to L1, L1 delegates to L2. The delegator retains accountability.

## Evidence

A recorded artifact that proves something happened. Every action, decision, and result creates evidence. Evidence is immutable once created.

## Genesis

The process of creating a new ANNY organization from scratch. Genesis creates L0, all L1 directors, and all L2 workers in a single atomic operation. After Genesis, the organization is ready to operate.

## Handoff

A formal transfer of work or responsibility from one actor to another. Cross-department handoffs require L0 authorization.

## L0

The top-level organizational authority. There is exactly one L0. It makes final decisions, creates departments, and certifies work. Think of L0 as the CEO of the organization.

## L1

A department director. Each L1 leads one department and has one L2 worker. L1s receive missions from L0 and delegate tasks to their L2. Think of an L1 as a department head.

## L2

A department worker and specialist. Each L2 belongs to one L1 director and executes tasks within that department. L2s cannot create their own missions or delegate. Think of an L2 as a skilled team member.

## Mission

A unit of work with a defined objective, scope, and success criteria. Missions flow from L0 to L1 to L2. They have a lifecycle: CREATED → IN_PROGRESS → COMPLETED (or FAILED).

## Provenance

The chain of origin for any piece of work or data. Provenance tracks who created something, when, why, and under what authority.

## Reconstruction

The process of rebuilding the organizational state from durable canonical records. A new process must be able to reconstruct the full organizational state without any prior memory.

## Repository

A durable storage location for organizational records. The canonical repository (Git) is the source of truth for the organizational structure.

## Repository Fabric

The system that manages connections between repositories and ensures data consistency across the organization.

## Workspace

A designated area where a department's work happens. Each department has its own workspace with defined inputs, outputs, and records.
