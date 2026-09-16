# ANNY Bootstrap Command Contract

## Purpose

This document defines the deterministic conversational trigger for ANNY bootstrap.

The phrase `bootstrap` in an ANNY conversation is **not** interpreted as the CSS/JavaScript framework, a generic software bootstrap, or an arbitrary project initialization request when it is used in one of the canonical command forms below.

## Canonical command

The canonical ANNY activation command is:

```text
INICIA BOOTSTRAP ANNY
```

Case is insignificant. Leading/trailing whitespace is insignificant.

The following equivalent forms MUST resolve to the same command:

```text
inicia bootstrap anny
Inicia Bootstrap Anny
INICIA BOOTSTRAP ANNY
```

## Deterministic dispatch rule

When a conversation contains the canonical command `INICIA BOOTSTRAP ANNY`, ANNY MUST enter the ANNY bootstrap protocol.

It MUST NOT:

- interpret `bootstrap` as the Bootstrap CSS/JavaScript framework;
- ask whether the user means the CSS/JavaScript framework;
- substitute a generic application bootstrap procedure;
- infer a different actor or framework from conversational context;
- initialize a repository before identifying the authenticated GitHub principal and target instance;
- treat the public `GRECOITALICO/ANNY` distribution repository as the customer's instance merely because it contains Genesis code.

## Bootstrap protocol

After deterministic dispatch, ANNY MUST:

1. identify itself as ANNY;
2. establish the authenticated GitHub principal available to the session;
3. determine the authorized repository scope available to that principal;
4. identify the intended ANNY instance repository;
5. inspect durable repository state before any initialization;
6. determine whether that instance is initialized or uninitialized;
7. continue through the canonical ANNY bootstrap/Genesis procedure defined by the installed product contract;
8. fail closed when identity, repository scope, required durable state, or required infrastructure cannot be established.

The conversational command is an activation trigger for the protocol. It is **not** itself authorization to mutate an arbitrary repository.

## Target selection rule

`GRECOITALICO/ANNY` is the public ANNY distribution repository. It is not automatically the runtime instance for a customer.

A customer instance is an independently initialized repository selected from the authenticated GitHub scope.

ANNY MUST NOT initialize the public distribution repository merely because `INICIA BOOTSTRAP ANNY` was issued.

## Related deterministic actor commands

The organizational control plane may define additional canonical commands using the same grammar:

```text
INICIA BOOTSTRAP KIRA
INICIA BOOTSTRAP FORGE
```

These are actor-specific protocol dispatch commands. They MUST resolve to the canonical durable bootstrap entrypoint for that actor and MUST NOT be interpreted as generic software/bootstrap terminology.

For KIRA specifically, the canonical Engineering bootstrap source is:

```text
GRECOITALICO/CONRRAD-ENGINEERING/DIRECTOR/BOOTSTRAP/ENTRYPOINT.md
```

## Source-of-truth rule

The command contract defines lexical dispatch. The actor's canonical repository bootstrap entrypoint defines the actual bootstrap procedure.

Conversation memory is not the authoritative operational state.

## Fail-closed behavior

If the session cannot establish the authenticated principal or the canonical bootstrap source, ANNY MUST report the exact missing capability or evidence and stop. It MUST NOT guess.
