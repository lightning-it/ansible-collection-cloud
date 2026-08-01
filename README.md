# lit.cloud

<!-- BEGIN LIT_QUALITY_BADGES -->

[![CI](https://github.com/lightning-it/ansible-collection-cloud/actions/workflows/collection-ci.yml/badge.svg?branch=develop)](https://github.com/lightning-it/ansible-collection-cloud/actions/workflows/collection-ci.yml)
[![Latest Release](https://img.shields.io/github/v/release/lightning-it/ansible-collection-cloud?sort=semver)](https://github.com/lightning-it/ansible-collection-cloud/releases/latest)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/lightning-it/ansible-collection-cloud/badge)](https://scorecard.dev/viewer/?uri=github.com/lightning-it/ansible-collection-cloud)
[![Ansible Galaxy](https://img.shields.io/ansible/collection/v/lit/cloud?label=Ansible%20Galaxy)](https://galaxy.ansible.com/ui/repo/published/lit/cloud/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

<!-- END LIT_QUALITY_BADGES -->

<!-- BEGIN LIT_SHARED_RELEASE_MODEL -->

## Release and Quality Model

This repository follows the Lightning IT shared release and quality model.

See [RELEASE.md](./RELEASE.md) for:

- branch and release flow
- required quality checks
- test matrix
- release evidence
- artifact publishing
- supported repository-specific release behavior

Repository classification: **Ansible Collection**.
Required test profiles: `pre-commit, lint, light, molecule-light, molecule-heavy-incus, release-validation`.
Publishing targets: `github-release, ansible-galaxy`.

## Supported and Tested Platforms

| Platform / Product     |                  Status | Validation       |
| ---------------------- | ----------------------: | ---------------- |
| ubuntu-latest          |               Supported | Molecule / Incus |
| ansible-core           | Tested where applicable | Molecule / Incus |
| incus                  | Tested where applicable | Molecule / Incus |
| hetzner-object-storage | Tested where applicable | Molecule / Incus |

<!-- END LIT_SHARED_RELEASE_MODEL -->

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
