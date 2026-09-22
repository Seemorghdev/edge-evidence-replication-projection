# Security Policy

## Supported versions

Security fixes are applied to the current `main` branch and the most recent tagged release, when a tagged release exists. Older commits and development branches are not supported.

## Reporting a vulnerability

Use GitHub Private Vulnerability Reporting for this repository:

1. Open the repository **Security** tab.
2. Choose **Advisories** and **Report a vulnerability**.
3. Include the affected version or commit, impact, reproduction steps, and any suggested mitigation.

Do not open a public issue for a vulnerability. Do not include credentials, bucket or target identifiers, provider coordinates, retained evidence, personal data, access tokens, service-account material, or private infrastructure details in public discussions. When private reporting is unavailable, contact the repository owner through GitHub before sharing sensitive details.

## Response expectations

Maintainers aim to acknowledge a report within three business days, provide an initial triage within seven business days, and coordinate disclosure after a fix or mitigation is available. Timelines may vary with severity and reproducibility.

## Scope

Reports are especially useful for target-identity bypass, unsafe path handling, collision or immutability bypass, readback-verification gaps, SQLite integrity errors, credential exposure, command injection, container privilege escalation, dependency compromise, or Terraform examples that could perform unintended provider actions.

Good-faith security research that avoids privacy violations, service disruption, destructive actions, and access to data beyond what is necessary to demonstrate the issue is welcomed.
