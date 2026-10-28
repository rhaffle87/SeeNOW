# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2026-10-28

### Added
- **Shadow DOM Traversal:** Recursive `querySelectorAllDeep` in SoM injector scanning open `shadowRoot` trees and custom web-components.
- **Viewport Auto-Scroll:** Automatic scroll-down trigger during SoM capture when options or navigation buttons are below the fold.
- **CDP Auto-Reconnect & Stale Page Recovery:** `is_connection_alive()` watchdog with automatic tab switching and silent CDP reconnection.
- **Atomic Config Persistence:** Atomic file writes (`config.json.tmp` + `os.replace`) with corrupted JSON recovery and automatic bootstrap from `config.json.example`.
- **Headless Environment Resilience:** Safe lazy imports for `pyautogui`, `mss`, and `keyboard` preventing CI headless crashes.
- **Jittered Exponential Backoff:** Exponential backoff with random jitter and strict Pydantic model validation with safe defaults in LLM router.

## [1.0.0] - 2026-10-28

### Added
- **Native GUI HUD:** Built with CustomTkinter featuring dark enterprise aesthetics (`#090d16`), Always-on-Top floating mode, and responsive layout.
- **Set-of-Marks (SoM) Grounding:** Injects high-contrast bounding badges (`[1]`, `[2]`, `[3]`) into browser DOM elements for visual-language mapping.
- **1-Click CDP Launcher:** Automatic detection of Google Chrome and Microsoft Edge on Windows, macOS, and Linux with persistent local user profile.
- **Anti-Blur Protection:** Injected stealth script overriding `document.visibilityState` to avoid test blur/tab-switch detection.
- **Bandwidth-Optimized Vision Pipeline:** Automatic Lanczos downscaling to 1280px width and JPEG 70% compression (<90 KB payload per frame).
- **Zero-Glitch Regex JSON Parser:** Resilient JSON parser eliminating redundant 9router request re-tries caused by markdown formatting.
- **Multi-OS CI/CD Workflows:** Automated GitHub Actions test matrix across Windows, macOS, Ubuntu, and Python 3.10–3.13, verified with CodeQL, Bandit, and Semgrep.
