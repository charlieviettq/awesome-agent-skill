---
name: ios-testflight-github-actions
description: "Set up iOS TestFlight delivery via GitHub Actions—build, sign, upload—with secret hygiene and no auto-push."
allowed-tools: Read, Glob, Grep
---

# iOS TestFlight via GitHub Actions

Guide for CI pipelines that build signed iOS apps and upload to TestFlight. Focus on guardrails; user supplies Apple credentials via GitHub Secrets.

## When to use

- Automating beta builds on tag or main
- Standardizing Fastlane or xcodebuild upload steps
- Documenting secret requirements for the team

## When not to use

- Manual Xcode archive only
- Android Play Console (different pipeline)
- Production App Store release without beta gate

## Required secrets (examples)

Store in GitHub Actions secrets — never in repo:

- `APP_STORE_CONNECT_API_KEY` or issuer ID + key ID + `.p8` content
- `MATCH_PASSWORD` / certificate repo access if using match
- Signing identities via keychain or ephemeral CI keychain

## Workflow outline

1. **Trigger** — workflow_dispatch, tag, or branch push (document which)
2. **Checkout** — include submodules if needed
3. **Ruby/Node setup** — if using Fastlane
4. **Install deps** — `bundle install`, CocoaPods/SPM resolve
5. **Build** — archive release configuration
6. **Sign** — match or manual cert; verify team ID
7. **Upload** — `upload_to_testflight` or `xcrun altool` successor APIs
8. **Notify** — Slack/issue comment on success/failure

## Guardrails

- **No auto-commit** of version bumps unless team explicitly wants it
- **No auto-push** to main from CI on failure retry loops
- Pin action SHAs or versions; review third-party actions
- Separate workflows for PR (build-only) vs release (upload)

## Verification

- Build succeeds on CI before enabling upload
- TestFlight build appears in App Store Connect
- Internal testers can install

## Troubleshooting

| Issue | Check |
|-------|-------|
| Code signing error | Cert expiry, wrong bundle ID, profile mismatch |
| Upload 401 | API key roles, key ID, issuer ID |
| Missing compliance | Export compliance in App Store Connect |
