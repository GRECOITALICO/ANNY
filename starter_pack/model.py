#!/usr/bin/env python3
"""ANNY Standard Organizational Model.

This module defines the standard ANNY organizational structure
that every new instance receives. The customer does NOT choose
departments, directors, or workers. ANNY delivers the complete
structure automatically.

All documentation generators read from this model.
"""

# =====================================================================
# STANDARD DEPARTMENTS — 8 departments, each with an L1 and L2
# =====================================================================
STANDARD_DEPARTMENTS = [
    {
        "name": "Marketing",
        "director_name": "ANNA",
        "worker_name": "DESIGN",
        "prefix": "MARK",
        "purpose": "Drives brand strategy, market positioning, and communication.",
        "responsibilities": [
            "Brand identity and messaging",
            "Market research and analysis",
            "Campaign planning and execution",
            "Content strategy",
            "Public relations",
            "Customer communication channels",
        ],
        "mission_types": [
            "Campaign execution",
            "Market research",
            "Brand audit",
            "Content production",
        ],
        "workspace_description": "The Marketing workspace handles all brand, communication, and market-facing activities. Incoming items include market data, customer feedback, and campaign briefs. Outputs include campaign assets, market reports, and communication plans.",
    },
    {
        "name": "Product",
        "director_name": "IRIS",
        "worker_name": "PRISM",
        "prefix": "PROD",
        "purpose": "Defines what gets built, why, and for whom.",
        "responsibilities": [
            "Product vision and roadmap",
            "Feature prioritization",
            "User research and requirements",
            "Product metrics and KPIs",
            "Cross-functional coordination",
            "Release planning",
        ],
        "mission_types": [
            "Feature specification",
            "User research",
            "Product review",
            "Roadmap update",
        ],
        "workspace_description": "The Product workspace is where product vision becomes actionable plans. Incoming items include market insights, user feedback, and technical constraints. Outputs include feature specifications, roadmaps, and acceptance criteria.",
    },
    {
        "name": "Engineering",
        "director_name": "KIRA",
        "worker_name": "FORGE",
        "prefix": "ENGI",
        "purpose": "Builds, tests, and maintains the technical systems.",
        "responsibilities": [
            "Software development and architecture",
            "Code review and quality assurance",
            "Infrastructure and deployment",
            "Technical debt management",
            "Performance optimization",
            "Developer tooling",
        ],
        "mission_types": [
            "Implementation",
            "Bug fix",
            "Architecture review",
            "Infrastructure change",
            "Performance optimization",
        ],
        "workspace_description": "The Engineering workspace is where technical work happens. Incoming items include specifications, bug reports, and architecture decisions. Outputs include code, tests, deployments, and technical documentation.",
    },
    {
        "name": "Security & Trust",
        "director_name": "KLARA",
        "worker_name": "SENTINEL",
        "prefix": "SECU",
        "purpose": "Protects the organization, its data, and its users.",
        "responsibilities": [
            "Security policy and standards",
            "Threat assessment and mitigation",
            "Access control and identity",
            "Compliance monitoring",
            "Incident response",
            "Security auditing",
        ],
        "mission_types": [
            "Security audit",
            "Threat assessment",
            "Incident response",
            "Policy update",
            "Access review",
        ],
        "workspace_description": "The Security & Trust workspace monitors and enforces organizational safety. Incoming items include security alerts, audit requests, and compliance requirements. Outputs include security reports, policy documents, and incident responses.",
    },
    {
        "name": "Legal & Compliance",
        "director_name": "RUTH",
        "worker_name": "LEX",
        "prefix": "LEGA",
        "purpose": "Ensures the organization operates within legal and regulatory boundaries.",
        "responsibilities": [
            "Contract review and management",
            "Regulatory compliance",
            "Intellectual property protection",
            "Data privacy and GDPR",
            "Legal risk assessment",
            "Policy documentation",
        ],
        "mission_types": [
            "Contract review",
            "Compliance audit",
            "Policy drafting",
            "Legal risk assessment",
            "Regulatory filing",
        ],
        "workspace_description": "The Legal & Compliance workspace handles all regulatory and legal matters. Incoming items include contracts, regulations, and compliance requirements. Outputs include legal opinions, policy documents, and compliance reports.",
    },
    {
        "name": "Customer & Market",
        "director_name": "MINA",
        "worker_name": "SCOUT",
        "prefix": "CUST",
        "purpose": "Understands, serves, and advocates for the customer.",
        "responsibilities": [
            "Customer relationship management",
            "Support and service delivery",
            "Customer feedback collection",
            "Market intelligence",
            "Customer success metrics",
            "Voice of the customer",
        ],
        "mission_types": [
            "Customer research",
            "Support escalation",
            "Satisfaction survey",
            "Market analysis",
            "Customer onboarding",
        ],
        "workspace_description": "The Customer & Market workspace is the organization's interface with its customers. Incoming items include customer inquiries, feedback, and market signals. Outputs include support responses, satisfaction reports, and market intelligence.",
    },
    {
        "name": "Operations",
        "director_name": "STELLA",
        "worker_name": "WATCH",
        "prefix": "OPER",
        "purpose": "Keeps the organization running smoothly and efficiently.",
        "responsibilities": [
            "Process optimization",
            "Resource allocation",
            "Operational monitoring",
            "Workflow management",
            "Vendor management",
            "Capacity planning",
        ],
        "mission_types": [
            "Process improvement",
            "Operational review",
            "Resource planning",
            "Vendor evaluation",
            "Capacity assessment",
        ],
        "workspace_description": "The Operations workspace manages the day-to-day functioning of the organization. Incoming items include operational data, resource requests, and process reports. Outputs include operational plans, resource allocations, and efficiency reports.",
    },
    {
        "name": "Finance & Economics",
        "director_name": "ZARA",
        "worker_name": "LEDGER",
        "prefix": "FINA",
        "purpose": "Manages the financial health and economic strategy of the organization.",
        "responsibilities": [
            "Budget planning and management",
            "Financial reporting and analysis",
            "Cost optimization",
            "Revenue tracking",
            "Financial risk assessment",
            "Economic forecasting",
        ],
        "mission_types": [
            "Budget review",
            "Financial audit",
            "Cost analysis",
            "Revenue forecast",
            "Investment evaluation",
        ],
        "workspace_description": "The Finance & Economics workspace manages all financial aspects of the organization. Incoming items include financial data, budget requests, and economic reports. Outputs include financial statements, budget plans, and economic analyses.",
    },
]


# =====================================================================
# ACTOR ROLE DESCRIPTIONS
# =====================================================================
L0_DESCRIPTION = {
    "title": "System Root — Organizational Authority",
    "responsibilities": [
        "Ultimate decision-making authority",
        "Strategic direction and vision",
        "Department creation and dissolution",
        "Authority delegation to L1 directors",
        "Certification and final approval",
        "Cross-department conflict resolution",
        "Genesis and organizational bootstrap",
    ],
    "authority": "Full organizational authority over all departments and actors",
    "authority_limits": "None — L0 is the ultimate authority",
    "mission_role": "Creates and assigns top-level missions; certifies completed work",
}

L1_DESCRIPTION_TEMPLATE = {
    "title_template": "Director of {department}",
    "responsibilities_template": [
        "Leads the {department} department",
        "Delegates tasks to {worker_name} (L2 worker)",
        "Reviews and approves work within {department}",
        "Reports to L0 on department status",
        "Manages department resources and priorities",
        "Escalates cross-department issues to L0",
    ],
    "authority": "Full authority within {department}; cannot act outside department scope",
    "authority_limits": "Cannot modify L0 decisions; cannot act in other departments; cannot self-promote",
    "mission_role": "Receives missions from L0; breaks them into tasks for L2; reviews results",
}

L2_DESCRIPTION_TEMPLATE = {
    "title_template": "{worker_name} — {department} Specialist",
    "responsibilities_template": [
        "Executes tasks assigned by {director_name} (L1 director)",
        "Produces deliverables within {department}",
        "Reports progress to {director_name}",
        "Creates evidence for completed work",
        "Follows department protocols",
    ],
    "authority": "Execution authority within assigned missions only",
    "authority_limits": "Cannot create missions; cannot delegate; cannot modify authority; cannot access other departments",
    "mission_role": "Receives tasks from L1; executes work; produces evidence; reports completion",
}


# =====================================================================
# PROTOCOLS
# =====================================================================
PROTOCOLS = {
    "communication": {
        "name": "Communication Protocol",
        "purpose": "Defines how actors exchange information within the organization.",
        "rules": [
            "L2 workers communicate with their L1 director, never directly with L0.",
            "L1 directors communicate with L0 and with their L2 worker.",
            "L1 directors do NOT communicate directly with other L1 directors unless through L0 mediation.",
            "All communication is recorded as evidence.",
            "Messages flow through designated channels (incoming/outgoing directories).",
        ],
        "example": "FORGE (L2 Engineering) needs clarification on a task. FORGE sends a message to KIRA (L1 Engineering). KIRA either answers directly or escalates to L0 if it crosses department boundaries.",
    },
    "delegation": {
        "name": "Delegation Protocol",
        "purpose": "Defines how authority and tasks flow downward through the hierarchy.",
        "rules": [
            "L0 delegates missions to L1 directors.",
            "L1 directors break missions into tasks and delegate to their L2 worker.",
            "Delegation must include: scope, constraints, deadline, and success criteria.",
            "The delegator retains responsibility — delegation does not transfer accountability.",
            "L2 cannot delegate to anyone.",
        ],
        "example": "L0 creates a mission 'Launch marketing campaign'. L0 delegates to ANNA (L1 Marketing). ANNA breaks it into tasks and assigns them to DESIGN (L2 Marketing).",
    },
    "handoff": {
        "name": "Handoff Protocol",
        "purpose": "Defines how work transitions between actors or departments.",
        "rules": [
            "Handoffs require explicit documentation in the HANDOFFS/ directory.",
            "The receiving actor must acknowledge the handoff.",
            "Handoffs between departments require L0 authorization.",
            "Each handoff must include: what is being transferred, why, from whom, to whom, and any constraints.",
        ],
        "example": "Engineering completes a feature. KIRA creates a handoff to KLARA (Security) for a security review. L0 authorizes the cross-department handoff.",
    },
    "review": {
        "name": "Review Protocol",
        "purpose": "Defines how completed work is evaluated and approved.",
        "rules": [
            "L2 work is reviewed by their L1 director.",
            "L1 decisions that affect other departments are reviewed by L0.",
            "Reviews must reference specific evidence and criteria.",
            "Failed reviews return work to the executor with specific feedback.",
            "Approved work generates evidence of approval.",
        ],
        "example": "FORGE completes a code implementation. KIRA reviews against the acceptance criteria. If approved, KIRA records evidence of approval. If rejected, KIRA returns it to FORGE with specific issues.",
    },
    "escalation": {
        "name": "Escalation Protocol",
        "purpose": "Defines how problems move upward through the hierarchy.",
        "rules": [
            "L2 escalates to their L1 director when blocked or when the issue exceeds their authority.",
            "L1 escalates to L0 when the issue crosses department boundaries or exceeds L1 authority.",
            "Escalation must include: the problem, what was attempted, why it cannot be resolved at the current level.",
            "L0 must respond to all escalations.",
            "De-escalation happens when L0 assigns the resolution back to appropriate L1/L2.",
        ],
        "example": "FORGE discovers a security vulnerability while coding. This exceeds Engineering scope. KIRA escalates to L0. L0 creates a cross-department mission involving KIRA (Engineering) and KLARA (Security).",
    },
    "certification": {
        "name": "Certification Protocol",
        "purpose": "Defines how organizational outputs are formally validated and certified.",
        "rules": [
            "Only L0 can issue final certifications.",
            "Certification requires complete evidence trail.",
            "Certified artifacts are immutable — changes require new certification.",
            "Certification covers: correctness, completeness, compliance, and provenance.",
        ],
        "example": "After Engineering completes a release and Security approves it, L0 certifies the release as ready for production. The certification record references all evidence from both departments.",
    },
}


# =====================================================================
# ENVIRONMENTS
# =====================================================================
ENVIRONMENTS = [
    {
        "name": "DEVELOPMENT",
        "purpose": "Where new work is created and initially tested.",
        "who_uses": "L2 workers during task execution.",
        "authority_note": "Environment does NOT grant authority. An L2 worker in DEVELOPMENT has the same authority limits as everywhere else.",
    },
    {
        "name": "TEST",
        "purpose": "Where work is validated against acceptance criteria.",
        "who_uses": "L1 directors during review, L2 workers during validation.",
        "authority_note": "Test results create evidence but do not change authority.",
    },
    {
        "name": "STAGING",
        "purpose": "A production-like environment for final verification.",
        "who_uses": "L1 directors for final review before certification.",
        "authority_note": "Staging approval does not equal production deployment authority.",
    },
    {
        "name": "PRODUCTION",
        "purpose": "The live operational environment.",
        "who_uses": "Controlled by L0 certification. No direct L2 access.",
        "authority_note": "Production deployment requires L0 certification. Environment access is NOT the same as deployment authority.",
    },
]


# =====================================================================
# GLOSSARY
# =====================================================================
GLOSSARY = {
    "L0": "The top-level organizational authority. There is exactly one L0. It makes final decisions, creates departments, and certifies work. Think of L0 as the CEO of the organization.",
    "L1": "A department director. Each L1 leads one department and has one L2 worker. L1s receive missions from L0 and delegate tasks to their L2. Think of an L1 as a department head.",
    "L2": "A department worker and specialist. Each L2 belongs to one L1 director and executes tasks within that department. L2s cannot create their own missions or delegate. Think of an L2 as a skilled team member.",
    "Genesis": "The process of creating a new ANNY organization from scratch. Genesis creates L0, all L1 directors, and all L2 workers in a single atomic operation. After Genesis, the organization is ready to operate.",
    "Mission": "A unit of work with a defined objective, scope, and success criteria. Missions flow from L0 to L1 to L2. They have a lifecycle: CREATED → IN_PROGRESS → COMPLETED (or FAILED).",
    "Workspace": "A designated area where a department's work happens. Each department has its own workspace with defined inputs, outputs, and records.",
    "Authority": "The permission to perform specific actions. Authority flows downward: L0 has full authority, L1 has department authority, L2 has execution authority. Authority is never self-assigned.",
    "Delegation": "The act of assigning a task or mission from a higher authority to a lower one. L0 delegates to L1, L1 delegates to L2. The delegator retains accountability.",
    "Handoff": "A formal transfer of work or responsibility from one actor to another. Cross-department handoffs require L0 authorization.",
    "Evidence": "A recorded artifact that proves something happened. Every action, decision, and result creates evidence. Evidence is immutable once created.",
    "Provenance": "The chain of origin for any piece of work or data. Provenance tracks who created something, when, why, and under what authority.",
    "Audit": "A formal review of actions, decisions, and evidence to verify compliance with rules and procedures.",
    "Repository": "A durable storage location for organizational records. The canonical repository (Git) is the source of truth for the organizational structure.",
    "Repository Fabric": "The system that manages connections between repositories and ensures data consistency across the organization.",
    "Canonical State": "The official, authoritative state of the organization as recorded in the Git repository. If there is a conflict between any other source and the canonical state, the canonical state wins.",
    "Reconstruction": "The process of rebuilding the organizational state from durable canonical records. A new process must be able to reconstruct the full organizational state without any prior memory.",
    "Certification": "A formal declaration by L0 that a piece of work meets all requirements. Only L0 can certify. Certification requires complete evidence.",
}
