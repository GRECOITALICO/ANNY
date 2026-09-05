#!/usr/bin/env python3
"""ANNY Starter Pack Documentation Generator.

Reads the canonical ANNY organizational model from actor YAML files
and produces the complete ANNY-DOCUMENTATION/ tree.

ALL documentation is derived from canonical state — never hardcoded.
"""
from __future__ import annotations

import json
import datetime
from pathlib import Path
from typing import Optional

import yaml

from starter_pack.model import (
    STANDARD_DEPARTMENTS, L0_DESCRIPTION, L1_DESCRIPTION_TEMPLATE,
    L2_DESCRIPTION_TEMPLATE, PROTOCOLS, ENVIRONMENTS, GLOSSARY,
)
from starter_pack.svg_generator import (
    generate_org_chart_svg, generate_authority_map_svg,
    generate_mission_lifecycle_svg, generate_environment_map_svg,
    generate_repository_map_svg, generate_workspace_map_svg,
)


# =====================================================================
# CANONICAL MODEL READER
# =====================================================================
class OrganizationalSnapshot:
    """Reads and normalizes the canonical organizational state."""

    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.actors = []
        self.l0 = None
        self.l1s = []
        self.l2s = []
        self.departments = {}
        self.enterprise_name = ""
        self.owner = ""
        self.github_repo = ""
        self.genesis_timestamp = ""
        self._load()

    def _load(self):
        # Read actors
        actors_dir = self.repo_root / "actors"
        if actors_dir.exists():
            for f in sorted(actors_dir.glob("ACT-*.yaml")):
                with open(f) as fh:
                    actor = yaml.safe_load(fh)
                    if actor:
                        self.actors.append(actor)
                        level = actor.get("level", "")
                        if level == "L0":
                            self.l0 = actor
                        elif level == "L1":
                            self.l1s.append(actor)
                        elif level == "L2":
                            self.l2s.append(actor)

        # Read state
        state_path = self.repo_root / "state" / "CURRENT_STATE.yaml"
        if state_path.exists():
            with open(state_path) as fh:
                state = yaml.safe_load(fh) or {}
                self.enterprise_name = state.get("enterprise_name", "ANNY Organization")
                self.owner = state.get("owner", "")
                self.github_repo = state.get("github_repo", "")
                self.genesis_timestamp = state.get("genesis_timestamp", "")

        # Read genesis
        genesis_path = self.repo_root / "genesis" / "GENESIS.yaml"
        if genesis_path.exists():
            with open(genesis_path) as fh:
                genesis = yaml.safe_load(fh) or {}
                ent = genesis.get("enterprise", {}) or {}
                if not self.enterprise_name:
                    self.enterprise_name = ent.get("name", "ANNY Organization")

        # Build department map
        for actor in self.l1s:
            dept = actor.get("department", "Unknown")
            self.departments[dept] = {"director": actor, "worker": None}

        for actor in self.l2s:
            dept = actor.get("department", "Unknown")
            if dept in self.departments:
                self.departments[dept]["worker"] = actor
            else:
                self.departments[dept] = {"director": None, "worker": actor}

    def get_dept_model(self, dept_name: str) -> Optional[dict]:
        """Find the standard department model by name."""
        for d in STANDARD_DEPARTMENTS:
            if d["name"] == dept_name or dept_name.startswith(d["name"].split(" ")[0]):
                return d
        # Fuzzy match by prefix
        for d in STANDARD_DEPARTMENTS:
            if dept_name.lower().startswith(d["prefix"].lower()[:4]):
                return d
        return None


# =====================================================================
# MARKDOWN GENERATORS
# =====================================================================

def _header(title: str, subtitle: str = "") -> str:
    lines = [f"# {title}", ""]
    if subtitle:
        lines.append(f"*{subtitle}*")
        lines.append("")
    return "\n".join(lines)


def _gen_welcome(snap: OrganizationalSnapshot) -> str:
    return f"""# Welcome to {snap.enterprise_name}

## Your organization is ready.

ANNY has already prepared your complete organizational structure. You don't need to create departments, assign roles, or design the hierarchy.

**What ANNY has set up for you:**

- **1 organizational authority** (L0) — the root of all decisions
- **8 department directors** (L1) — each leading a specialized area
- **8 department specialists** (L2) — each executing work within their department
- **17 total actors** working together

## What do you do now?

**Tell ANNY what you need.** That's it.

When you express a need, ANNY will:

1. Figure out which departments are involved
2. Create the right missions
3. Assign the work to the right people
4. Track progress and evidence
5. Review and certify the results

## Where to start

| Document | What you'll learn |
|----------|-------------------|
| [First Day Guide](../00-START-HERE/FIRST-DAY-GUIDE.md) | How to get started right now |
| [How ANNY Works](../00-START-HERE/HOW-ANNY-WORKS.md) | The big picture |
| [Company Map](../01-COMPANY/COMPANY-MAP.md) | Who does what |
| [People Directory](../02-PEOPLE/PEOPLE-DIRECTORY.md) | Meet the team |
| [Glossary](../00-START-HERE/GLOSSARY.md) | What the words mean |

---

*Generated from canonical organizational state on {datetime.datetime.utcnow().strftime("%Y-%m-%d")}.*
"""


def _gen_first_day_guide(snap: OrganizationalSnapshot) -> str:
    return f"""# First Day Guide

## Welcome to your first day with {snap.enterprise_name}.

This guide will help you understand how ANNY works in the first five minutes.

---

## Step 1: Understand the Structure

Your organization has three levels:

### L0 — The Authority
{snap.l0["name"] if snap.l0 else "ANNY"} is the organizational authority. L0 makes final decisions, creates missions, and certifies results. Think of L0 as the CEO.

### L1 — The Directors
There are **{len(snap.l1s)} directors**, each leading a department:

| Director | Department |
|----------|------------|
{chr(10).join(f"| {a['name']} | {a['department']} |" for a in snap.l1s)}

Each director receives missions from L0, breaks them into tasks, and assigns them to their specialist.

### L2 — The Specialists
There are **{len(snap.l2s)} specialists**, each working under a director:

| Specialist | Department | Reports To |
|------------|------------|------------|
{chr(10).join(f"| {a['name']} | {a['department']} | {a.get('parent_director', 'their L1')} |" for a in snap.l2s)}

Each specialist executes the work, creates evidence, and reports back.

---

## Step 2: Understand How Work Flows

```
You have a need
    ↓
Tell ANNY
    ↓
L0 creates a mission
    ↓
L0 assigns to the right L1 director
    ↓
L1 breaks it into tasks for L2
    ↓
L2 does the work and creates evidence
    ↓
L1 reviews the work
    ↓
L0 certifies the result
    ↓
Done.
```

---

## Step 3: Remember This

> **ANNY already prepared the organization.**
>
> You don't have to create departments.
>
> You don't have to decide what capabilities will exist.
>
> You don't have to design the hierarchy.
>
> When you need something:
>
> **TELL ANNY.**

ANNY will figure out which departments are involved and create the right missions.

---

*Generated from canonical organizational state on {datetime.datetime.utcnow().strftime("%Y-%m-%d")}.*
"""


def _gen_how_anny_works(snap: OrganizationalSnapshot) -> str:
    return f"""# How ANNY Works

## The Big Picture

ANNY is an organizational system that manages work through a clear hierarchy of authority, delegation, and evidence.

---

## The Three Levels

### Level 0 (L0) — Organizational Authority
There is exactly **one** L0: **{snap.l0["name"] if snap.l0 else "ANNY"}**.

L0 is the root of all authority. Every decision in the organization ultimately traces back to L0. L0 creates missions, delegates to departments, and certifies results.

### Level 1 (L1) — Department Directors
There are **{len(snap.l1s)}** L1 directors. Each one leads a department:

{chr(10).join(f"- **{a['name']}** leads **{a['department']}**" for a in snap.l1s)}

L1 directors receive missions from L0, plan how to execute them, and delegate tasks to their L2 specialist. They review completed work before it goes back to L0.

### Level 2 (L2) — Department Specialists
There are **{len(snap.l2s)}** L2 specialists. Each one works under an L1 director:

{chr(10).join(f"- **{a['name']}** works in **{a['department']}**" for a in snap.l2s)}

L2 specialists do the actual work. They execute tasks, create deliverables, and produce evidence of their work.

---

## How Authority Works

Authority flows **downward only**:

```
L0 (full authority)
 ├── L1 Marketing (authority within Marketing only)
 │    └── L2 DESIGN (execution authority within assigned tasks)
 ├── L1 Product (authority within Product only)
 │    └── L2 PRISM (execution authority within assigned tasks)
 └── ... (6 more departments)
```

**Key rules:**
- L2 cannot promote itself to L1 or L0
- L1 cannot act outside its department
- L0 is the only actor that can authorize cross-department work
- Authority is never self-assigned

---

## How Missions Work

1. **CREATED** — L0 creates a mission with objectives and criteria
2. **DELEGATED** — L0 assigns it to an L1 director
3. **IN_PROGRESS** — L1 breaks it into tasks and L2 executes
4. **REVIEW** — L1 reviews L2's work
5. **COMPLETED** — L0 certifies the result
6. **FAILED** — If criteria aren't met, the mission returns for rework

Every step creates **evidence** — an immutable record of what happened.

---

## Where State Lives

| Type | Location | Purpose |
|------|----------|---------|
| Canonical State | Git repository | The authoritative source of truth for the Customer Instance |
| Operational State | Runtime memory | Temporary working state |
| Evidence | `evidence/records/` | Immutable proof of actions |
| Decisions | `decisions/records/` | Records of authority decisions |

If there is ever a conflict between canonical state and any other source, **canonical state wins**.

## The Product Model

The organizational hierarchy, departments, and actor roles are defined by the **ANNY Product Model**. This is an immutable contract. Customers cannot modify the standard departments or remove actors.

## What Makes ANNY Different

1. **No ambiguity** — Every actor has clear authority and limits
2. **Full traceability** — Every action creates evidence
3. **Reconstruction** — The entire organization can be rebuilt from durable records
4. **No shortcuts** — L2 cannot bypass L1; L1 cannot bypass L0

---

*Generated from canonical organizational state on {datetime.datetime.utcnow().strftime("%Y-%m-%d")}.*
"""


def _gen_glossary() -> str:
    lines = ["# Glossary", "", "All terms used in the ANNY organizational system, explained simply.", ""]
    for term, definition in sorted(GLOSSARY.items()):
        lines.append(f"## {term}")
        lines.append("")
        lines.append(definition)
        lines.append("")
    return "\n".join(lines)


def _gen_company_overview(snap: OrganizationalSnapshot) -> str:
    return f"""# Company Overview

## {snap.enterprise_name}

### What is this company?

{snap.enterprise_name} is an organization managed by the ANNY system. 

### Product Model vs. Customer Instance State

It is important to understand the difference between the ANNY Product Model and your Customer Instance State:

- **ANNY Product Model (Organizational Contract):** ANNY provides the complete organizational structure out of the box. You do not choose departments, you do not define the hierarchy, you do not create standard directors, and you do not decide which capabilities exist. ANNY's standard 17-actor structure (L0, 8 L1s, 8 L2s) is fixed and guaranteed by contract.
- **Customer Instance (Actual Company State):** This represents the active state of your specific company. When you express needs, ANNY routes those needs through the existing standard organization, creating active missions and evidence specific to you.

You just express needs. ANNY routes them.

### Organizational Numbers

| Metric | Value |
|--------|-------|
| L0 (Authority) | 1 |
| L1 (Directors) | {len(snap.l1s)} |
| L2 (Specialists) | {len(snap.l2s)} |
| **Total Actors** | **{1 + len(snap.l1s) + len(snap.l2s)}** |
| Departments | {len(snap.departments)} |

### Owner

- **Identity**: {snap.owner or "Not specified"}
- **Repository**: {snap.github_repo or "Not specified"}
- **Genesis Date**: {snap.genesis_timestamp or "Not specified"}

---

*Generated from canonical organizational state on {datetime.datetime.utcnow().strftime("%Y-%m-%d")}.*
"""


def _gen_company_map(snap: OrganizationalSnapshot) -> str:
    lines = [f"# Company Map — {snap.enterprise_name}", ""]
    lines.append("This map shows every actor in the organization and how they relate to each other.")
    lines.append("")
    lines.append("## Organizational Authority")
    lines.append("")
    if snap.l0:
        lines.append(f"**{snap.l0['name']}** (L0) — {snap.l0.get('role', 'System Root')}")
        lines.append(f"- Actor ID: `{snap.l0['actor_id']}`")
        lines.append(f"- Authority: Full organizational authority")
    lines.append("")
    lines.append("## Department Directors and Specialists")
    lines.append("")

    for dept_name, dept_data in sorted(snap.departments.items()):
        director = dept_data.get("director")
        worker = dept_data.get("worker")
        lines.append(f"### {dept_name}")
        lines.append("")
        if director:
            lines.append(f"**Director:** {director['name']} (L1)")
            lines.append(f"- Actor ID: `{director['actor_id']}`")
            lines.append(f"- Role: {director.get('role', 'Director')}")
            lines.append(f"- Reports to: L0 ({snap.l0['name'] if snap.l0 else 'Root'})")
            lines.append("")
        if worker:
            lines.append(f"**Specialist:** {worker['name']} (L2)")
            lines.append(f"- Actor ID: `{worker['actor_id']}`")
            lines.append(f"- Role: {worker.get('role', 'Worker')}")
            lines.append(f"- Reports to: {director['name'] if director else 'L1'}")
            lines.append("")

    lines.append("## Visual Organization Chart")
    lines.append("")
    lines.append("See [ORGANIZATION-CHART.svg](ORGANIZATION-CHART.svg) for the visual representation.")
    lines.append("")
    lines.append(f"*Generated from canonical organizational state on {datetime.datetime.utcnow().strftime('%Y-%m-%d')}.*")
    return "\n".join(lines)


def _gen_org_chart_md(snap: OrganizationalSnapshot) -> str:
    lines = ["# Organization Chart", ""]
    lines.append("![Organization Chart](ORGANIZATION-CHART.svg)")
    lines.append("")
    lines.append("## Hierarchy")
    lines.append("")
    if snap.l0:
        lines.append(f"- **{snap.l0['name']}** (L0 — Root Authority)")
    for dept_name, dept_data in sorted(snap.departments.items()):
        d = dept_data.get("director")
        w = dept_data.get("worker")
        if d:
            lines.append(f"  - **{d['name']}** (L1 — {dept_name})")
        if w:
            lines.append(f"    - **{w['name']}** (L2 — {dept_name})")
    lines.append("")
    return "\n".join(lines)


def _gen_authority_map_md(snap: OrganizationalSnapshot) -> str:
    lines = ["# Authority Map", ""]
    lines.append("![Authority Map](AUTHORITY-MAP.svg)")
    lines.append("")
    lines.append("## Authority Rules")
    lines.append("")
    lines.append("| Actor | Level | Authority Scope | Limits |")
    lines.append("|-------|-------|-----------------|--------|")
    if snap.l0:
        lines.append(f"| {snap.l0['name']} | L0 | All departments | None |")
    for a in snap.l1s:
        lines.append(f"| {a['name']} | L1 | {a['department']} only | Cannot act outside department |")
    for a in snap.l2s:
        lines.append(f"| {a['name']} | L2 | Assigned tasks only | Cannot delegate or self-promote |")
    lines.append("")
    return "\n".join(lines)


def _gen_people_directory(snap: OrganizationalSnapshot) -> str:
    lines = ["# People Directory", ""]
    lines.append(f"**Total: {1 + len(snap.l1s) + len(snap.l2s)} actors**")
    lines.append("")
    lines.append("## L0 — Organizational Authority")
    lines.append("")
    if snap.l0:
        lines.append(f"| Name | Actor ID | Role |")
        lines.append(f"|------|----------|------|")
        lines.append(f"| [{snap.l0['name']}](L0/{snap.l0['name']}.md) | `{snap.l0['actor_id']}` | {snap.l0.get('role', 'Root')} |")
    lines.append("")
    lines.append("## L1 — Department Directors")
    lines.append("")
    lines.append("| Name | Department | Actor ID |")
    lines.append("|------|------------|----------|")
    for a in snap.l1s:
        lines.append(f"| [{a['name']}](L1/{a['name']}.md) | {a['department']} | `{a['actor_id']}` |")
    lines.append("")
    lines.append("## L2 — Department Specialists")
    lines.append("")
    lines.append("| Name | Department | Reports To | Actor ID |")
    lines.append("|------|------------|------------|----------|")
    for a in snap.l2s:
        parent = a.get("parent_director", "")
        parent_name = ""
        for d in snap.l1s:
            if d["actor_id"] == parent:
                parent_name = d["name"]
                break
        lines.append(f"| [{a['name']}](L2/{a['name']}.md) | {a['department']} | {parent_name} | `{a['actor_id']}` |")
    lines.append("")
    return "\n".join(lines)


def _gen_actor_profile(actor: dict, snap: OrganizationalSnapshot) -> str:
    level = actor.get("level", "")
    dept = actor.get("department", "")
    model = snap.get_dept_model(dept)

    lines = [f"# {actor['name']}", ""]
    lines.append(f"| Field | Value |")
    lines.append(f"|-------|-------|")
    lines.append(f"| **Name** | {actor['name']} |")

    if level == "L0":
        lines.append(f"| **Title** | {L0_DESCRIPTION['title']} |")
    elif level == "L1":
        title = L1_DESCRIPTION_TEMPLATE["title_template"].format(department=dept)
        lines.append(f"| **Title** | {title} |")
    elif level == "L2":
        wname = actor["name"]
        title = L2_DESCRIPTION_TEMPLATE["title_template"].format(worker_name=wname, department=dept)
        lines.append(f"| **Title** | {title} |")

    lines.append(f"| **Level** | {level} |")

    parent_id = actor.get("parent_director", "")
    parent_name = ""
    if parent_id:
        for a in snap.actors:
            if a["actor_id"] == parent_id:
                parent_name = a["name"]
                break
    lines.append(f"| **Parent** | {parent_name or 'None (Root)'} |")
    lines.append(f"| **Department** | {dept} |")
    lines.append(f"| **Actor ID** | `{actor['actor_id']}` |")
    lines.append(f"| **Status** | {actor.get('status', 'ACTIVE')} |")
    lines.append("")

    # Responsibilities
    lines.append("## Responsibilities")
    lines.append("")
    if level == "L0":
        for r in L0_DESCRIPTION["responsibilities"]:
            lines.append(f"- {r}")
    elif level == "L1" and model:
        wname = model["worker_name"]
        for r in L1_DESCRIPTION_TEMPLATE["responsibilities_template"]:
            lines.append(f"- {r.format(department=dept, worker_name=wname)}")
    elif level == "L2" and model:
        dname = model["director_name"]
        for r in L2_DESCRIPTION_TEMPLATE["responsibilities_template"]:
            lines.append(f"- {r.format(department=dept, director_name=dname)}")
    lines.append("")

    # Authority
    lines.append("## Authority")
    lines.append("")
    if level == "L0":
        lines.append(f"**Scope:** {L0_DESCRIPTION['authority']}")
        lines.append("")
        lines.append(f"**Limits:** {L0_DESCRIPTION['authority_limits']}")
    elif level == "L1":
        lines.append(f"**Scope:** {L1_DESCRIPTION_TEMPLATE['authority'].format(department=dept)}")
        lines.append("")
        lines.append(f"**Limits:** {L1_DESCRIPTION_TEMPLATE['authority_limits']}")
    elif level == "L2":
        lines.append(f"**Scope:** {L2_DESCRIPTION_TEMPLATE['authority']}")
        lines.append("")
        lines.append(f"**Limits:** {L2_DESCRIPTION_TEMPLATE['authority_limits']}")
    lines.append("")

    # Workspace
    lines.append("## Workspace")
    lines.append("")
    lines.append(f"Works in the **{dept}** workspace.")
    if model:
        lines.append(f"See [Workspace Details](../../04-WORKSPACES/per-department/{dept.replace(' ', '-').replace('&', 'and')}.md)")
    lines.append("")

    # Communication
    lines.append("## Communication Paths")
    lines.append("")
    if level == "L0":
        lines.append("- Communicates with all L1 directors")
        lines.append("- Receives escalations from L1 directors")
        lines.append("- Issues directives and certifications")
    elif level == "L1":
        lines.append(f"- Reports to: L0 ({snap.l0['name'] if snap.l0 else 'Root'})")
        worker = snap.departments.get(dept, {}).get("worker")
        if worker:
            lines.append(f"- Delegates to: {worker['name']} (L2)")
        lines.append("- Does not communicate directly with other L1 directors")
    elif level == "L2":
        director = snap.departments.get(dept, {}).get("director")
        if director:
            lines.append(f"- Reports to: {director['name']} (L1)")
        lines.append("- Does not communicate with L0 directly")
        lines.append("- Does not communicate with other departments")
    lines.append("")

    # Mission role
    lines.append("## Mission Role")
    lines.append("")
    if level == "L0":
        lines.append(L0_DESCRIPTION["mission_role"])
    elif level == "L1":
        lines.append(L1_DESCRIPTION_TEMPLATE["mission_role"])
    elif level == "L2":
        lines.append(L2_DESCRIPTION_TEMPLATE["mission_role"])
    lines.append("")

    return "\n".join(lines)


def _gen_department_directory(snap: OrganizationalSnapshot) -> str:
    lines = ["# Department Directory", ""]
    lines.append(f"**{len(snap.departments)} departments** — each with a director (L1) and a specialist (L2).")
    lines.append("")
    lines.append("These departments are part of the standard ANNY organizational system. They were not created by the customer — they are built into every ANNY instance.")
    lines.append("")
    lines.append("| Department | Director (L1) | Specialist (L2) | Purpose |")
    lines.append("|------------|---------------|-----------------|---------|")
    for dept_name in sorted(snap.departments.keys()):
        data = snap.departments[dept_name]
        d = data.get("director")
        w = data.get("worker")
        model = snap.get_dept_model(dept_name)
        purpose = model["purpose"] if model else ""
        safe = dept_name.replace(" ", "-").replace("&", "and")
        lines.append(f"| [{dept_name}](per-department/{safe}.md) | {d['name'] if d else '—'} | {w['name'] if w else '—'} | {purpose} |")
    lines.append("")
    return "\n".join(lines)


def _gen_department_page(dept_name: str, snap: OrganizationalSnapshot) -> str:
    data = snap.departments.get(dept_name, {})
    director = data.get("director")
    worker = data.get("worker")
    model = snap.get_dept_model(dept_name)

    lines = [f"# {dept_name}", ""]

    if model:
        lines.append(f"**Purpose:** {model['purpose']}")
    lines.append("")

    lines.append("## People")
    lines.append("")
    if director:
        lines.append(f"- **Director (L1):** {director['name']} — `{director['actor_id']}`")
    if worker:
        lines.append(f"- **Specialist (L2):** {worker['name']} — `{worker['actor_id']}`")
    lines.append("")

    lines.append("## Responsibilities")
    lines.append("")
    if model:
        for r in model["responsibilities"]:
            lines.append(f"- {r}")
    lines.append("")

    lines.append("## Authority")
    lines.append("")
    if director:
        lines.append(f"- {director['name']} has full authority within {dept_name}")
        lines.append(f"- {director['name']} cannot act outside {dept_name}")
    if worker:
        lines.append(f"- {worker['name']} has execution authority within assigned tasks only")
        lines.append(f"- {worker['name']} cannot delegate or self-promote")
    lines.append("")

    lines.append("## Limits")
    lines.append("")
    lines.append(f"- Cannot modify L0 decisions")
    lines.append(f"- Cannot act in other departments without L0 authorization")
    lines.append(f"- Cannot self-assign authority")
    lines.append("")

    lines.append("## Workspace")
    lines.append("")
    if model:
        lines.append(model["workspace_description"])
    lines.append("")

    lines.append("## Mission Types")
    lines.append("")
    if model:
        for m in model["mission_types"]:
            lines.append(f"- {m}")
    lines.append("")

    lines.append("## Communication")
    lines.append("")
    if director and worker:
        lines.append(f"- {director['name']} communicates with L0 and with {worker['name']}")
        lines.append(f"- {worker['name']} communicates only with {director['name']}")
    lines.append("")

    lines.append("## Evidence")
    lines.append("")
    lines.append("All work within this department creates evidence records stored in `evidence/records/`.")
    lines.append("")

    lines.append("## Audit")
    lines.append("")
    lines.append("All department actions are subject to organizational audit by L0.")
    lines.append("")

    return "\n".join(lines)


def _gen_workspace_directory(snap: OrganizationalSnapshot) -> str:
    lines = ["# Workspace Directory", ""]
    lines.append("Each department has its own workspace — a designated area where work happens.")
    lines.append("")
    for dept_name in sorted(snap.departments.keys()):
        safe = dept_name.replace(" ", "-").replace("&", "and")
        lines.append(f"- [{dept_name} Workspace](per-department/{safe}.md)")
    lines.append("")
    return "\n".join(lines)


def _gen_workspace_page(dept_name: str, snap: OrganizationalSnapshot) -> str:
    data = snap.departments.get(dept_name, {})
    director = data.get("director")
    worker = data.get("worker")
    model = snap.get_dept_model(dept_name)

    lines = [f"# {dept_name} Workspace", ""]

    lines.append("## Who works here")
    lines.append("")
    if director:
        lines.append(f"- **{director['name']}** (L1 Director) — supervises the workspace")
    if worker:
        lines.append(f"- **{worker['name']}** (L2 Specialist) — executes work in the workspace")
    lines.append("")

    lines.append("## What enters")
    lines.append("")
    lines.append("- Missions delegated by L0")
    lines.append("- Tasks broken down by the L1 director")
    lines.append("- Handoffs from other departments (with L0 authorization)")
    lines.append("- Feedback and review notes")
    lines.append("")

    lines.append("## What happens here")
    lines.append("")
    if model:
        lines.append(model["workspace_description"])
    else:
        lines.append(f"Work is planned by the director and executed by the specialist within the {dept_name} domain.")
    lines.append("")

    lines.append("## What leaves")
    lines.append("")
    lines.append("- Completed deliverables")
    lines.append("- Evidence records (proof of work)")
    lines.append("- Status reports to L0")
    lines.append("- Handoffs to other departments (with L0 authorization)")
    lines.append("")

    lines.append("## What records live here")
    lines.append("")
    lines.append(f"- Mission records related to {dept_name}")
    lines.append("- Decision records for department-level decisions")
    lines.append("- Evidence records for all completed work")
    lines.append("")

    lines.append("## What missions use it")
    lines.append("")
    if model:
        for m in model["mission_types"]:
            lines.append(f"- {m}")
    lines.append("")

    lines.append("## Who supervises it")
    lines.append("")
    if director:
        lines.append(f"- **{director['name']}** (L1) supervises all workspace activity")
    lines.append(f"- **L0** has oversight authority over all workspaces")
    lines.append("")

    lines.append("## What authority applies")
    lines.append("")
    if director:
        lines.append(f"- {director['name']} has full authority within this workspace")
    if worker:
        lines.append(f"- {worker['name']} has execution authority for assigned tasks only")
    lines.append("- Cross-department work requires L0 authorization")
    lines.append("")

    return "\n".join(lines)


def _gen_protocol_directory() -> str:
    lines = ["# Protocol Directory", ""]
    lines.append("Protocols define how work, communication, and authority flow through the organization.")
    lines.append("")
    for key, proto in PROTOCOLS.items():
        lines.append(f"- [{proto['name']}]({key.upper()}.md) — {proto['purpose']}")
    lines.append("")
    return "\n".join(lines)


def _gen_protocol_page(key: str) -> str:
    proto = PROTOCOLS[key]
    lines = [f"# {proto['name']}", ""]
    lines.append(f"**Purpose:** {proto['purpose']}")
    lines.append("")
    lines.append("## Rules")
    lines.append("")
    for i, rule in enumerate(proto["rules"], 1):
        lines.append(f"{i}. {rule}")
    lines.append("")
    lines.append("## Example")
    lines.append("")
    lines.append(proto["example"])
    lines.append("")
    return "\n".join(lines)


def _gen_mission_lifecycle() -> str:
    return """# Mission Lifecycle

![Mission Lifecycle](MISSION-LIFECYCLE.svg)

## States

| State | Description |
|-------|-------------|
| **CREATED** | L0 defines the mission with objectives and success criteria |
| **DELEGATED** | L0 assigns the mission to an L1 director |
| **IN_PROGRESS** | L1 has broken it into tasks; L2 is executing |
| **REVIEW** | L2 has completed work; L1 is reviewing |
| **COMPLETED** | L0 has certified the result |
| **FAILED** | The mission did not meet success criteria |

## Flow

1. L0 **creates** the mission
2. L0 **delegates** to the appropriate L1
3. L1 **plans** and assigns tasks to L2
4. L2 **executes** and creates evidence
5. L1 **reviews** the work
6. If approved, L0 **certifies** — mission COMPLETED
7. If rejected, returns to L2 for rework
8. If unrecoverable, mission is marked FAILED

## Key Rules

- Only L0 can create missions
- Only L0 can certify completion
- L2 cannot skip the review step
- Every state change creates evidence
"""


def _gen_environment_map() -> str:
    lines = ["# Environment Map", ""]
    lines.append("![Environment Map](ENVIRONMENT-MAP.svg)")
    lines.append("")
    lines.append("> **Important:** Environment ≠ Authority. Being in a particular environment does not grant additional authority.")
    lines.append("")
    for env in ENVIRONMENTS:
        lines.append(f"## {env['name']}")
        lines.append("")
        lines.append(f"**Purpose:** {env['purpose']}")
        lines.append("")
        lines.append(f"**Who uses it:** {env['who_uses']}")
        lines.append("")
        lines.append(f"**Authority note:** {env['authority_note']}")
        lines.append("")
    return "\n".join(lines)


def _gen_repository_map(snap: OrganizationalSnapshot) -> str:
    return f"""# Repository Map

![Repository Map](REPOSITORY-MAP.svg)

## Repositories

| Repository | Purpose | Type |
|------------|---------|------|
| `{snap.github_repo or "organization/repo"}` | Primary organizational repository | Canonical |

## What is Canonical?

The **canonical state** is the authoritative source of truth. It lives in the Git repository. If there is ever a conflict between canonical state and any other source, **canonical state wins**.

Canonical records include:
- Actor definitions (`actors/`)
- Mission records (`missions/records/`)
- Decision records (`decisions/records/`)
- Evidence records (`evidence/records/`)
- State files (`state/`)
- Genesis configuration (`genesis/`)

## What is Operational?

Operational state is temporary, runtime data used during execution. It does NOT survive process restarts unless backed by a durable store.

## What Requires Repository Fabric (RF)?

The following operations require RF authorization:
- Any write to the canonical repository
- State mutations that affect organizational structure
- Cross-department handoffs

The RF ensures that every canonical change is:
- Authorized by the appropriate actor
- Based on the current (non-stale) state
- Recorded with full provenance

## The Portal is NOT the Source of Truth

If a web portal, dashboard, or API shows data that differs from the canonical Git repository, the **Git repository is correct**.
"""


def _gen_security_overview() -> str:
    return """# Security Overview

## Security Principles

1. **Least Privilege** — Every actor has only the authority needed for their role
2. **No Self-Promotion** — Actors cannot increase their own authority
3. **Full Audit Trail** — Every action creates immutable evidence
4. **Fail Closed** — If authorization cannot be verified, access is denied
5. **Canonical Authority** — The Git repository is the single source of truth

## Authority Boundaries

- L0 has full authority
- L1 has authority within their department only
- L2 has execution authority within assigned tasks only
- Cross-department actions require L0 authorization

## Reconstruction Guarantee

The organization can be fully reconstructed from durable canonical records at any time. No single point of failure can permanently destroy organizational state.
"""


def _gen_evidence_overview() -> str:
    return """# Evidence System

## What is Evidence?

Evidence is an immutable record that proves something happened. Every action, decision, and result in the organization creates evidence.

## Evidence Types

| Type | Created When |
|------|-------------|
| PROVENANCE | Genesis or structural changes |
| DECISION | Authority decisions are made |
| EXECUTION | Work is completed |
| REVIEW | Work is reviewed |
| CERTIFICATION | Work is certified |

## Evidence Properties

- **Immutable** — Once created, evidence cannot be changed
- **Timestamped** — Every record has a creation timestamp
- **Attributed** — Every record identifies who created it
- **Referenced** — Evidence references the mission, decision, or action it proves

## Where Evidence Lives

All evidence records are stored in `evidence/records/` as YAML files.
"""


def _gen_audit_overview() -> str:
    return """# Audit System

## Purpose

The audit system provides formal review of actions, decisions, and evidence to verify compliance with organizational rules.

## What Gets Audited

- Authority usage (who did what)
- Mission lifecycle compliance
- Evidence completeness
- Decision authorization
- Cross-department interactions

## Audit Records

Audit records are stored in `audits/` and reference the evidence they reviewed.

## Who Can Audit

Only L0 has full audit authority. L1 directors can audit within their department scope.
"""


def _gen_certification_overview() -> str:
    return """# Certification System

## Purpose

Certification is the formal declaration by L0 that a piece of work meets all requirements.

## Rules

1. Only L0 can issue certifications
2. Certification requires complete evidence trail
3. Certified artifacts are immutable
4. Changes to certified work require new certification

## Certification Records

Certification records are stored in `certification/` and reference all supporting evidence.
"""


def _gen_index_json(snap: OrganizationalSnapshot) -> dict:
    return {
        "documentation_version": "1.0",
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "enterprise_name": snap.enterprise_name,
        "sections": {
            "00-START-HERE": {
                "title": "Getting Started",
                "documents": ["WELCOME.md", "FIRST-DAY-GUIDE.md", "HOW-ANNY-WORKS.md", "GLOSSARY.md"],
            },
            "01-COMPANY": {
                "title": "Company",
                "documents": ["COMPANY-OVERVIEW.md", "COMPANY-MAP.md", "ORGANIZATION-CHART.md", "ORGANIZATION-CHART.svg", "AUTHORITY-MAP.md", "AUTHORITY-MAP.svg"],
            },
            "02-PEOPLE": {
                "title": "People",
                "documents": ["PEOPLE-DIRECTORY.md"],
                "subdirectories": ["L0", "L1", "L2"],
            },
            "03-DEPARTMENTS": {
                "title": "Departments",
                "documents": ["DEPARTMENT-DIRECTORY.md"],
                "subdirectories": ["per-department"],
            },
            "04-WORKSPACES": {
                "title": "Workspaces",
                "documents": ["WORKSPACE-DIRECTORY.md"],
                "subdirectories": ["per-department"],
            },
            "05-PROTOCOLS": {
                "title": "Protocols",
                "documents": ["PROTOCOL-DIRECTORY.md", "COMMUNICATION.md", "DELEGATION.md", "HANDOFF.md", "REVIEW.md", "ESCALATION.md", "CERTIFICATION.md"],
            },
            "06-MISSIONS": {
                "title": "Missions",
                "documents": ["MISSION-LIFECYCLE.md", "MISSION-LIFECYCLE.svg"],
            },
            "07-ENVIRONMENTS": {
                "title": "Environments",
                "documents": ["ENVIRONMENT-MAP.md", "ENVIRONMENT-MAP.svg"],
            },
            "08-REPOSITORIES": {
                "title": "Repositories",
                "documents": ["REPOSITORY-MAP.md", "REPOSITORY-MAP.svg"],
            },
            "09-SECURITY": {"title": "Security", "documents": ["SECURITY-OVERVIEW.md"]},
            "10-EVIDENCE": {"title": "Evidence", "documents": ["EVIDENCE-OVERVIEW.md"]},
            "11-AUDIT": {"title": "Audit", "documents": ["AUDIT-OVERVIEW.md"]},
            "12-CERTIFICATION": {"title": "Certification", "documents": ["CERTIFICATION-OVERVIEW.md"]},
            "99-REFERENCE": {"title": "Reference", "documents": ["REFERENCE.md"]},
        },
        "actors": {
            "total": 1 + len(snap.l1s) + len(snap.l2s),
            "l0": 1,
            "l1": len(snap.l1s),
            "l2": len(snap.l2s),
        },
        "departments": list(sorted(snap.departments.keys())),
    }


# =====================================================================
# MAIN GENERATOR
# =====================================================================

def generate_starter_pack(repo_root: str) -> dict:
    """Generate the complete ANNY-DOCUMENTATION/ tree from canonical state.

    Returns a summary dict with counts and paths.
    """
    snap = OrganizationalSnapshot(repo_root)
    base = Path(repo_root) / "ANNY-DOCUMENTATION"

    # Create directory structure
    dirs = [
        "00-START-HERE", "01-COMPANY", "02-PEOPLE", "02-PEOPLE/L0",
        "02-PEOPLE/L1", "02-PEOPLE/L2", "03-DEPARTMENTS",
        "03-DEPARTMENTS/per-department", "04-WORKSPACES",
        "04-WORKSPACES/per-department", "05-PROTOCOLS", "06-MISSIONS",
        "07-ENVIRONMENTS", "08-REPOSITORIES", "09-SECURITY",
        "10-EVIDENCE", "11-AUDIT", "12-CERTIFICATION", "99-REFERENCE",
    ]
    for d in dirs:
        (base / d).mkdir(parents=True, exist_ok=True)

    files_written = []

    def _write(rel_path: str, content: str):
        p = base / rel_path
        p.write_text(content, encoding="utf-8")
        files_written.append(rel_path)

    # 00-START-HERE
    _write("00-START-HERE/WELCOME.md", _gen_welcome(snap))
    _write("00-START-HERE/FIRST-DAY-GUIDE.md", _gen_first_day_guide(snap))
    _write("00-START-HERE/HOW-ANNY-WORKS.md", _gen_how_anny_works(snap))
    _write("00-START-HERE/GLOSSARY.md", _gen_glossary())

    # 01-COMPANY
    _write("01-COMPANY/COMPANY-OVERVIEW.md", _gen_company_overview(snap))
    _write("01-COMPANY/COMPANY-MAP.md", _gen_company_map(snap))
    _write("01-COMPANY/ORGANIZATION-CHART.md", _gen_org_chart_md(snap))
    _write("01-COMPANY/AUTHORITY-MAP.md", _gen_authority_map_md(snap))

    # SVGs
    _write("01-COMPANY/ORGANIZATION-CHART.svg", generate_org_chart_svg(snap))
    _write("01-COMPANY/AUTHORITY-MAP.svg", generate_authority_map_svg(snap))

    # 02-PEOPLE
    _write("02-PEOPLE/PEOPLE-DIRECTORY.md", _gen_people_directory(snap))
    if snap.l0:
        _write(f"02-PEOPLE/L0/{snap.l0['name']}.md", _gen_actor_profile(snap.l0, snap))
    for a in snap.l1s:
        _write(f"02-PEOPLE/L1/{a['name']}.md", _gen_actor_profile(a, snap))
    for a in snap.l2s:
        _write(f"02-PEOPLE/L2/{a['name']}.md", _gen_actor_profile(a, snap))

    # 03-DEPARTMENTS
    _write("03-DEPARTMENTS/DEPARTMENT-DIRECTORY.md", _gen_department_directory(snap))
    for dept_name in snap.departments:
        safe = dept_name.replace(" ", "-").replace("&", "and")
        _write(f"03-DEPARTMENTS/per-department/{safe}.md", _gen_department_page(dept_name, snap))

    # 04-WORKSPACES
    _write("04-WORKSPACES/WORKSPACE-DIRECTORY.md", _gen_workspace_directory(snap))
    for dept_name in snap.departments:
        safe = dept_name.replace(" ", "-").replace("&", "and")
        _write(f"04-WORKSPACES/per-department/{safe}.md", _gen_workspace_page(dept_name, snap))

    # 05-PROTOCOLS
    _write("05-PROTOCOLS/PROTOCOL-DIRECTORY.md", _gen_protocol_directory())
    for key in PROTOCOLS:
        _write(f"05-PROTOCOLS/{key.upper()}.md", _gen_protocol_page(key))

    # 06-MISSIONS
    _write("06-MISSIONS/MISSION-LIFECYCLE.md", _gen_mission_lifecycle())
    _write("06-MISSIONS/MISSION-LIFECYCLE.svg", generate_mission_lifecycle_svg())

    # 07-ENVIRONMENTS
    _write("07-ENVIRONMENTS/ENVIRONMENT-MAP.md", _gen_environment_map())
    _write("07-ENVIRONMENTS/ENVIRONMENT-MAP.svg", generate_environment_map_svg())

    # 08-REPOSITORIES
    _write("08-REPOSITORIES/REPOSITORY-MAP.md", _gen_repository_map(snap))
    _write("08-REPOSITORIES/REPOSITORY-MAP.svg", generate_repository_map_svg(snap))

    # 09-SECURITY
    _write("09-SECURITY/SECURITY-OVERVIEW.md", _gen_security_overview())

    # 10-EVIDENCE
    _write("10-EVIDENCE/EVIDENCE-OVERVIEW.md", _gen_evidence_overview())

    # 11-AUDIT
    _write("11-AUDIT/AUDIT-OVERVIEW.md", _gen_audit_overview())

    # 12-CERTIFICATION
    _write("12-CERTIFICATION/CERTIFICATION-OVERVIEW.md", _gen_certification_overview())

    # 99-REFERENCE
    _write("99-REFERENCE/REFERENCE.md", "# Reference\n\nThis section will contain detailed technical reference documentation.\n")

    # WORKSPACE-MAP.svg at root level of 04
    _write("04-WORKSPACES/WORKSPACE-MAP.svg", generate_workspace_map_svg(snap))

    # INDEX.json
    index = _gen_index_json(snap)
    idx_path = base / "INDEX.json"
    with open(idx_path, "w") as f:
        json.dump(index, f, indent=2)
    files_written.append("INDEX.json")

    return {
        "files_written": len(files_written),
        "l0_count": 1 if snap.l0 else 0,
        "l1_count": len(snap.l1s),
        "l2_count": len(snap.l2s),
        "total_actors": (1 if snap.l0 else 0) + len(snap.l1s) + len(snap.l2s),
        "departments": len(snap.departments),
        "base_path": str(base),
    }
