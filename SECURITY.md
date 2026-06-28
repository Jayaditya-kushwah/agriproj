# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x     | ✅ Yes    |

## Reporting a Vulnerability

**Please do NOT report security vulnerabilities via public GitLab issues.**

To report a vulnerability:
1. Email: security@agridoc.example (replace with actual contact)
2. Include: description, steps to reproduce, potential impact
3. We will acknowledge within 48 hours
4. We aim to patch critical issues within 7 days

## Security Design

AgriDoc is designed with farmer privacy as a core principle:

- **Local-first**: All data stored on the user's device/local server
- **No telemetry**: We collect zero usage data
- **File validation**: Only PDF/JPG/PNG accepted; MIME-type checked
- **Parameterized queries**: No SQL injection possible
- **Secret scanning**: Gitleaks/detect-secrets in pre-commit and CI
- **Dependency audit**: pip-audit runs in every CI pipeline

## Known Limitations

- Authentication is not implemented in v1.0 (designed for single-user local deployment)
- AgriStack sync endpoint is a stub; real implementation should use OAuth2
