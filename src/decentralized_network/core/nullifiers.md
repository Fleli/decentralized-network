# Nullifiers

This is a working semantic draft for nullifiers.

The goal here is to define what a nullifier *means* before we commit to any
specific ZK backend or circuit language.

## Purpose

A nullifier is a deterministic, one-way identifier used to enforce "one use per
scope" without revealing the underlying secret.

Typical uses:

- prevent replay
- prevent double-action within a scope
- support rate limits or one-time permissions

## Main Objects

### Root Secret

The root secret is the long-term private secret from which other secrets are
derived.

It should usually *not* be used directly in application-level nullifiers.

### Domain Secret

A domain secret is a secret derived from the root secret for one specific
subsystem or purpose.

Example idea:

- one domain secret for service-account nullifiers
- one domain secret for organization voting nullifiers
- one domain secret for message anti-replay nullifiers

This limits cross-domain linkage and compartmentalizes damage.

### Scope

The scope is the public namespace in which uniqueness is enforced.

Examples:

- "service-X:daily-action:2026-04-16"
- "organization-Y:proposal-12"
- "message-send:channel-7:epoch-402"

The same secret used with the same scope should produce the same nullifier.
Changing the scope should change the nullifier.

### Nullifier

The nullifier is the public identifier published to enforce uniqueness within
the scope.

It is safe to reveal the nullifier. It is *not* safe to reveal the secret used
to derive it.

## Draft Semantic Formula

Current draft semantic shape:

1. `domain_secret = KDF(root_secret, domain_label)`
2. `scope_hash = HASH_SCOPE(canonical_scope_data)`
3. `nullifier = HASH_NULLIFIER(domain_secret, scope_hash)`

This is intentionally written in abstract form.

For now, the important decision is the *shape*:

- derive a domain-specific secret first
- canonicalize the public scope
- derive the nullifier from the domain secret and scope

The exact primitive choices can be fixed later.

Likely direction:

- a normal KDF outside circuits
- a SNARK-friendly hash inside circuits

## Canonical Scope Data

The scope must not be "whatever string a caller happened to build".

It should be treated as structured data with a canonical order.

Example structure:

- protocol version
- subsystem label
- object identifier
- action label
- epoch / time window / nonce namespace

Then that structured data is canonicalized and hashed into `scope_hash`.

This prevents different parts of the system from producing different nullifiers
for what is conceptually the same action.

## Required Properties

The semantic design should satisfy:

- same `domain_secret` + same `scope` => same nullifier
- same `domain_secret` + different `scope` => different nullifier
- different `domain_secret` + same `scope` => different nullifier
- nullifier does not reveal the secret
- nullifiers from different subsystems should not collide by accident

## What Is Public vs Private

Public:

- scope
- nullifier

Private:

- root secret
- domain secret

## First ZK Statement

Ignoring membership for now, the first proof statement should be:

- public inputs: `scope`, `nullifier`
- private witness: `domain_secret`
- prove: `nullifier = HASH_NULLIFIER(domain_secret, HASH_SCOPE(scope))`

That is the simplest meaningful nullifier proof.

## Why Domain Secret Instead Of Root Secret

Using the root secret directly would work mechanically, but it is weaker as a
system design.

Using a domain secret instead:

- separates subsystems cleanly
- reduces cross-context linkage
- allows future rotation or migration per subsystem
- keeps the root secret at a higher trust boundary

## Open Decisions

Still intentionally unresolved:

- exact hash / KDF primitives
- exact encoding of `canonical_scope_data`
- whether `scope` is passed around as structured data or as a precomputed hash
- whether some nullifier families need extra public inputs beyond scope

## Summary

The current intended meaning is:

"A nullifier is a public uniqueness marker derived from a private
domain-specific secret and a public scope."

That is the semantic contract that both the plain Python implementation and the
future ZK circuits should follow.
