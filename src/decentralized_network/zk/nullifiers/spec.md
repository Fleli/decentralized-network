# ZK Nullifier Spec

This is the first tiny ZK skeleton for nullifiers.

The first concrete statement is:

- public: `service_id`, `nullifier`
- private: `domain_secret`

and the proof statement is:

`nullifier = HASH_NULLIFIER(domain_secret, HASH_SCOPE(service_id_bytes))`

where:

- `service_id` is provided externally as a hex string
- it must decode to exactly 32 bytes
- `domain_secret` is the service-nullifier secret derived from the root secret

For now this folder does **not** implement a real proving backend yet.

Its current purpose is only to fix the interface and proof statement before
adding Circom, Noir, or another proving stack.
