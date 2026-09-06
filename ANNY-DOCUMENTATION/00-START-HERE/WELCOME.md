# Welcome to ANNY

ANNY is a governed operational runtime that can be used independently by different organizations.

Your ANNY installation is identified through your authenticated GitHub principal and operates over the repositories authorized for that principal.

## The model

```text
You / your organization
        ↓
Authenticated GitHub account
        ↓
Your ANNY instance
        ↓
Authorized repositories
        ↓
Repository Fabric service
```

Every organization has its own identity, repository scope, durable state, missions, decisions, and evidence. No customer instance inherits another customer's organizational state.

## What ANNY does

Tell ANNY what you need. It reconstructs durable context, plans and delegates work according to its governance rules, records decisions and evidence, and continues from durable state in later sessions.

## What is shared

The ANNY product code is shared through the public distribution. Repository Fabric is shared infrastructure operated separately from the public ANNY repository.

## What is not shared

Customer state, repository scope, identities, credentials, missions, evidence, and operational memory are not shared between installations.

Start with `ANNY-DOCUMENTATION/00-START-HERE/DOWNLOAD-AND-INSTALL.md`.
