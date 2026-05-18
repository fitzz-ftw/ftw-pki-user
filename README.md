# ft-pki-user

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: LGPL v2.1](https://img.shields.io/badge/License-LGPL_v2.1-blue.svg)](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)
[![Coverage: 100%](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)]

A dedicated component of the **ftw-pki** suite for generating and managing Certificate Signing Requests (CSR) for leaf entities.

## 🛠 Features

* **Leaf CSR Generation:** Specialized logic to create standardized CSRs for end-entity certificates.
* **Automated Validation:** Built-in checks to ensure the generated requests meet the requirements of the issuing Intermediate CA.
* **Standard Compliance:** Supports modern X.509 extensions and security profiles required for leaf certificates.

## 📖 Documentation & Usage

This tool is used by end-entities to request certificates from an Intermediate CA within the ftw-pki hierarchy.

* **Command Line Interface:** Use the `ftwpkiusercsr` utility to generate your signing requests. Run `ftwpkiusercsr --help` for full command reference and options.
* **Technical Manual:** Detailed information on supported certificate profiles and internal logic can be found in the `doc/source/` directory.

## 📄 License

This project is licensed under the **LGPL v2.1 (or later)**.

---
© 2026 ftw-pki Contributors
