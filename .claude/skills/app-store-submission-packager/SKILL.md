---
name: app-store-submission-packager
description: "Prepare iOS App Store and Google Play submissions—metadata, assets, compliance checks, and release checklist. Use before store upload or review submission."
allowed-tools: Read, Glob, Grep
---

# App Store Submission Packager

Checklist-driven preparation for mobile store submissions. Does not handle credentials or automated upload unless user explicitly configures CI with secrets.

## When to use

- First submission or major version bump
- Review rejection remediation
- Cross-platform release alignment

## When not to use

- Internal TestFlight/Play internal testing only (see `ios-testflight-github-actions`)
- Web-only deploy

## Pre-submission checklist

### App binary

- [ ] Version and build number incremented
- [ ] Release configuration (no debug flags, correct signing)
- [ ] Privacy-sensitive APIs declared (iOS Privacy Manifest / Play Data safety)

### Metadata

- [ ] App name, subtitle, description localized as needed
- [ ] Keywords / category appropriate
- [ ] Support URL and privacy policy URL live
- [ ] Age rating questionnaire complete

### Assets

- [ ] Icons all required sizes
- [ ] Screenshots per device class / locale
- [ ] Preview video if used

### Compliance

- [ ] Export compliance / encryption questions answered
- [ ] Third-party SDK disclosures (ATT, analytics, payments)
- [ ] In-app purchase or subscription metadata if applicable

### Testing

- [ ] Smoke test on physical device
- [ ] Login, payments, push (if used) verified on production-like build

## Platform notes

| Platform | Common rejection causes |
|----------|-------------------------|
| iOS | Incomplete metadata, broken links, guideline 4.x privacy, login demo missing |
| Android | Data safety form mismatch, target API level, permissions justification |

## Output

- Completed checklist with blockers highlighted
- Draft release notes for store listing
- List of assets still missing

## Safety

- Never commit provisioning profiles, keystores, or API keys
- Use team secret stores for signing material

*Clean-room workflow inspired by mobile release patterns; not copied from external repos.*
