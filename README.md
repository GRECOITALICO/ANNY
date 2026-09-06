# ANNY

ANNY is a governed operational runtime designed to work with a user's authenticated GitHub identity and authorized repositories.

## Product boundary

ANNY is the distributable product. Repository Fabric is shared infrastructure outside this repository and is accessed through the public RF client/contract boundary. CONRRAD organizational state is not bundled into an ANNY installation.

## Core properties

- Instance-local durable state and evidence.
- GitHub identity must come from an authenticated principal; it is never trusted from user-supplied actor/login fields.
- Repository scope is derived from authenticated authorization.
- Governed operations fail closed when required infrastructure or identity is unavailable.
- Repository Fabric remains a separate service boundary.
- Certification and activation are distinct states.

## Installation

Start with `ANNY-DOCUMENTATION/00-START-HERE/DOWNLOAD-AND-INSTALL.md`.

## Certification baseline

The public distribution tracks the validated ANNY product baseline through P8. See `ANNY-DOCUMENTATION/PUBLIC-CERTIFICATION-BASELINE.md` for the public-facing mapping and scope limitations.
