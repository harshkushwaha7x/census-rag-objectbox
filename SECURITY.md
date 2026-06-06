# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Currently supported versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it by emailing **nebeyoumusie@gmail.com** with the following information:

- Type of vulnerability
- Full paths of source file(s) related to the vulnerability
- Location of the affected source code (tag/branch/commit or direct URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

**Please do not report security vulnerabilities through public GitHub issues.**

## Security Best Practices

### API Key Management
- Never commit `.env` files or API keys to version control
- Use environment variables or secret managers for production
- Rotate API keys regularly
- Limit API key permissions to minimum required

### Docker Security
- Use official base images
- Don't run containers as root
- Keep images updated with security patches
- Scan images for vulnerabilities

### Input Validation
- User inputs are sanitized before processing
- Maximum input length enforced
- Special characters handled properly

### Dependencies
- Regularly update dependencies
- Use `pip-audit` to check for vulnerabilities
- Monitor security advisories

## Disclosure Policy

When we receive a security bug report, we will:

1. Confirm the problem and determine affected versions
2. Audit code to find similar problems
3. Prepare fixes for all supported versions
4. Release patches as soon as possible

## Security Update Process

Security updates will be released as patch versions (e.g., 1.0.1, 1.0.2) and will include:

- Description of the vulnerability
- Affected versions
- Patched versions
- Credit to the reporter (if desired)

## Contact

For security issues: nebeyoumusie@gmail.com
