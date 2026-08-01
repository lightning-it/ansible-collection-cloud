# lit.cloud

`lit.cloud` provides public, environment-neutral Ansible roles for secure cloud
infrastructure configuration and orchestration.

## Roles

- `lit.cloud.hetzner_object_storage` plans, audits, and reconciles private
  Hetzner Object Storage buckets with versioning, Object Lock, retention,
  multipart cleanup, and deterministic least-privilege policies for
  separate-project principals.

See each role README for its complete variable, security, and lifecycle
contract. Heavy provider-backed acceptance is centrally orchestrated by
`lightning-it/modulix-validation`; ordinary collection gates remain
credential-free.

## License

MIT
