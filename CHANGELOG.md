# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-10-28

### Added
- **Native GUI HUD:** Built with CustomTkinter featuring dark enterprise aesthetics (`#090d16`), Always-on-Top floating mode, and responsive layout.
- **Set-of-Marks (SoM) Grounding:** Injects high-contrast bounding badges (`[1]`, `[2]`, `[3]`) into browser DOM elements for visual-language mapping.
- **1-Click CDP Launcher:** Automatic detection of Google Chrome and Microsoft Edge on Windows, macOS, and Linux with persistent local user profile.
- **Anti-Blur Protection:** Injected stealth script overriding `document.visibilityState` to avoid test blur/tab-switch detection.
- **Bandwidth-Optimized Vision Pipeline:** Automatic Lanczos downscaling to 1280px width and JPEG 70% compression (<90 KB payload per frame).
- **Zero-Glitch Regex JSON Parser:** Resilient JSON parser eliminating redundant 9router request re-tries caused by markdown formatting.
- **Multi-OS CI/CD Workflows:** Automated GitHub Actions test matrix across Windows, macOS, Ubuntu, and Python 3.10–3.13, verified with CodeQL, Bandit, and Semgrep.
