# ANNY Product Boundary

ANNY is the distributable product. Each customer operates an independent ANNY installation and an independent GitHub principal/scope.

Repository Fabric is shared infrastructure operated outside this public repository. ANNY reaches it through the public RF client and contract boundary.

## Separation

Customer-specific:
- authenticated GitHub principal
- repository scope
- instance state
- memory
- missions and decisions
- evidence

Shared service:
- Repository Fabric service
- controlled synchronization infrastructure

Internal CONRRAD:
- organizational topology
- internal certification evidence
- private operational repositories
- internal infrastructure configuration

## Identity rule

The customer identity used for authorization must come from the authenticated GitHub principal. A caller-supplied login, user id, owner name, or repository owner field is not an authentication source.

## Fail-closed rule

If the authenticated principal, required Repository Fabric service, or required durable state cannot be established, ANNY must stop with an explicit blocked/unavailable result rather than infer authority.
