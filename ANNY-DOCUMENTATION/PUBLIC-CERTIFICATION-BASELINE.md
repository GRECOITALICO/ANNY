# ANNY Public Certification Baseline

This document records the certification baseline used by the public ANNY distribution. Internal CONRRAD repositories remain the certification and evidence environment; their private operational state is not shipped with ANNY.

## Baseline

P0-P4: foundational governance, runtime and safety certification history.
P5/P5.1-P5.5: actor and departmental deep-runtime certification history.
P6.0: organizational registry reconciliation.
P6.1: cross-department network certification.
P7-M: reusable real actor runtime capability.
P7: 100 real long-horizon transitions, synthetic transitions = 0.
P8: adversarial meta-audit of P5-P7 claims.

## Product boundary

The public distribution contains the generic ANNY product surface and the public Repository Fabric client/contract boundary. Private CONRRAD topology, private Fabric implementation, internal evidence stores, and operational state are excluded.

Certification is not activation. A new installation starts unactivated and derives its identity from the authenticated GitHub context and its own durable state.
