# How ANNY Works

## The Big Picture

ANNY is an organizational system that manages work through a clear hierarchy of authority, delegation, and evidence.

---

## The Three Levels

### Level 0 (L0) — Organizational Authority
There is exactly **one** L0: **AURORA CORPORATION**.

L0 is the root of all authority. Every decision in the organization ultimately traces back to L0. L0 creates missions, delegates to departments, and certifies results.

### Level 1 (L1) — Department Directors
There are **8** L1 directors. Each one leads a department:

- **MINA** leads **Customer & Market**
- **KIRA** leads **Engineering**
- **ZARA** leads **Finance & Economics**
- **RUTH** leads **Legal & Compliance**
- **ANNA** leads **Marketing**
- **STELLA** leads **Operations**
- **IRIS** leads **Product**
- **KLARA** leads **Security & Trust**

L1 directors receive missions from L0, plan how to execute them, and delegate tasks to their L2 specialist. They review completed work before it goes back to L0.

### Level 2 (L2) — Department Specialists
There are **8** L2 specialists. Each one works under an L1 director:

- **FORGE** works in **Engineering**
- **LEDGER** works in **Finance & Economics**
- **WATCH** works in **Operations**
- **DESIGN** works in **Marketing**
- **SCOUT** works in **Customer & Market**
- **SENTINEL** works in **Security & Trust**
- **PRISM** works in **Product**
- **LEX** works in **Legal & Compliance**

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

*Generated from canonical organizational state on 2026-09-05.*
