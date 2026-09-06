# First Day Guide

ANNY is designed to be installed independently by each organization.

## Step 1: Establish your identity

Your ANNY instance uses the authenticated GitHub account you connect to it as the identity and ownership boundary for the installation.

Do not type a GitHub login, owner name, or user id and treat it as proof of identity. Authentication must come from the connected GitHub principal.

## Step 2: Understand the organizational model

A fresh ANNY organization has three logical levels:

- **L0 — Organizational Authority:** the customer-controlled root authority.
- **L1 — Directors:** department-level authorities created by Genesis.
- **L2 — Specialists:** execution actors working within assigned scopes.

The actual actor ids and department state are generated and persisted by the customer's own ANNY instance. The public product does not embed the actors of the CONRRAD internal organization.

## Step 3: Understand the work flow

```text
You have a need
    ↓
Tell ANNY
    ↓
ANNY creates or reconstructs durable context
    ↓
L0 establishes the mission
    ↓
L1 plans and delegates
    ↓
L2 executes bounded work
    ↓
Evidence is recorded
    ↓
Review and certification follow the applicable authority rules
```

## Step 4: Remember the boundaries

Your ANNY instance is not a copy of CONRRAD. It is a customer-owned operational instance of the ANNY product.

Repository Fabric is shared infrastructure outside the public distribution. ANNY uses its public client/contract boundary to reach that service.

## Step 5: Continue from any new session

Close the chat and return later. ANNY reconstructs its operational context from durable canonical records instead of depending on conversation memory.
