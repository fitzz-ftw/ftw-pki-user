# Changelog: ftw-pki-user

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.3] - 2026-06-18

### Changed
- Integrate TomlPreParser into user CSR program
- Refactor argument validation logic
- Rename legacy TOML functions to modernize utility interfaces
- Update CLI flags and improve error handling protocols
- Update test data paths and documentation structure

### Documentation
- Update documentation structure, links, and API references
- Standardize configuration flags and namespaces in developer docs

### Testing
- Improve CSR workflow testing and validation assets

## [0.0.2a1] - 2026-05-18

### Added
- Integrate local `UserPKIConfig` to handle secure user-level configuration and dynamic path evaluations.
- Replace the generic placeholder docstring for `prog_user_csr` with a comprehensive, Sphinx-compliant English specification.

### Changed
- Shift password verification strategy from parameter injection (`pwcall`) to direct monkeypatching of standard library `getpass.getpass` within all interactive doctests.
- Enforce secure and explicit `.pem` file extensions (`.key.pem` and `config.ext_public`) for all generated user keypairs.
- Update file-saving workflows to utilize unified `config.config_path` and `config.data_path` locations instead of relying on static directory structures.

### Removed
- **Breaking Change**: Remove the deprecated `pwcall` argument from the `prog_user_csr` interface and its underlying pipeline forwarding.
- Remove the unused `platformdirs` intersphinx mapping from the Sphinx documentation build (`conf.py`).
- Delete the obsolete and duplicated `get_started_programms_old.ci.rst` documentation file.

---

## [0.0.1] - 2026-05-18
- Initial commit and package skeleton for the user workspace.
