# ANNY Public Release Manifest

## Release candidate

Version: 1.1.0-rc.1

Source repository: `GRECOITALICO/ANNY`

Product status: RELEASE CANDIDATE

## Product boundary

ANNY is the customer-facing distributed runtime. Each installation is independent and uses the customer's authenticated GitHub account as its identity boundary.

Repository Fabric is shared service infrastructure outside this public repository. The public product uses the RF client/contract boundary and does not package the private Fabric implementation.

CONRRAD is the internal infrastructure and certification environment. Its private organizational state is not part of this distribution.

## Included baseline

- Generic ANNY Genesis and schemas
- Governance contracts
- Public Repository Fabric client and contract
- Authenticated GitHub principal contract
- Public installation and onboarding documentation
- P0-P8 certification baseline declaration

## Not included

- CONRRAD departmental state
- Private Repository Fabric implementation
- Internal operational evidence
- Private infrastructure configuration
- Customer-specific state from any other ANNY installation

## Release integrity

The release artifact must be generated from the tagged release commit and accompanied by a SHA-256 digest. The existing `v1.0.0` ZIP remains the historical release artifact and must not be presented as this 1.1.0 candidate.
