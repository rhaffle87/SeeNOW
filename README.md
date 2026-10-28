# README.md
<div align="center">

# 🚀 SeeNOW
### Smart Exam Engine & Navigated Optical Workflow

[![CI Multi-OS](https://github.com/your-username/seenow/actions/workflows/ci.yml/badge.svg)](https://github.com/your-username/seenow/actions/workflows/ci.yml)
[![Security Scan](https://github.com/your-username/seenow/actions/workflows/security.yml/badge.svg)](https://github.com/your-username/seenow/actions/workflows/security.yml)
[![CodeQL](https://github.com/your-username/seenow/actions/workflows/codeql.yml/badge.svg)](https://github.com/your-username/seenow/actions/workflows/codeql.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](https://www.python.org/)

**SeeNOW** is an enterprise-grade autonomous browser-controlling desktop agent. Powered by **Set-of-Marks (SoM)** visual grounding, **Playwright CDP**, and **OpenAI-compatible LLM routers** (such as 9router), SeeNOW reads quiz screens, verifies answers analytically, and navigates web evaluations with zero human intervention.

</div>

---

## 🌟 Key Capabilities

- **Always-on-Top Floating HUD:** Lightweight native CustomTkinter desktop window floating seamlessly above any active quiz portal without obstructing view.
- **1-Click Chrome/Edge CDP Launcher:** Launches your local Chrome or Edge browser on port `9222` with a persistent profile (`./chrome_profile`), ensuring login sessions are preserved without bot detection (`navigator.webdriver` bypassed).
- **Set-of-Marks (SoM) Grounding:** Injects high-contrast badges `[1]`, `[2]`, `[3]` onto interactive elements (radio buttons, checkboxes, action buttons) before capturing screen state.
- **Iframe & Custom UI Support:** Handles child `<iframe>` elements and non-standard radio/checkbox implementations (Vue, React, Element UI, Ant Design, Quasar).
- **Optimized Vision Pipeline:** Automatic Lanczos downscaling to 1280px width and JPEG 70% compression reducing frame payloads to <90 KB (>95% bandwidth savings).
- **Anti-Blur Focus Shield:** Injects background scripts overriding `document.visibilityState` to avoid tab-switch and blur detection events.
- **SPA State Transition Guard:** SHA-256 state hashing verifies page updates before triggering subsequent captures, preventing question-skipping.
- **Global Hotkeys:** Instant trigger from keyboard:
  - `Alt + S`: Solve Once
  - `Alt + A`: Toggle Auto-Loop
  - `Alt + Q`: Emergency Stop

---

## 📁 Repository Structure

```text
seenow/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml               # Multi-OS (Ubuntu, Windows, macOS) & Python 3.10-3.13 Matrix
│   │   ├── security.yml         # Bandit, Semgrep & pip-audit SAST scans
│   │   ├── codeql.yml           # GitHub CodeQL security analysis
│   │   └── release.yml          # Automated PyInstaller build on v* tags
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── pull_request_template.md
├── core/
│   ├── __init__.py
│   ├── config_manager.py        # Centralized config loader with URL validation & secret masking
│   ├── som_injector.js          # Injected JavaScript Set-of-Marks labeling engine
│   ├── browser_engine.py        # Playwright CDP lifecycle, frame locator, image resizing
│   ├── os_screen_engine.py      # MSS + PyAutoGUI fallback engine
│   ├── llm_router.py            # 9router client with robust regex JSON parser
│   └── agent_worker.py          # Background worker thread with anti-skip state transition checks
├── gui/
│   ├── __init__.py
│   ├── app_window.py            # Main CustomTkinter HUD window and Settings panel
│   └── components.py            # StatusBadge, MetricPill, and AnswerCard components
├── tests/
│   ├── __init__.py
│   ├── test_config.py           # Configuration and URL validation tests
│   ├── test_json_parser.py      # Resilient JSON extraction tests
│   └── test_schema.py           # Output Pydantic schema validation tests
├── .env.example
├── .gitignore
├── config.json.example
├── pyproject.toml               # Build configuration, Ruff, Mypy, Pytest & Bandit rules
├── requirements.txt
├── requirements-dev.txt
├── LICENSE                      # MIT License
├── SECURITY.md                  # Vulnerability reporting policy
├── CONTRIBUTING.md              # Contribution guidelines
├── CHANGELOG.md                 # Version release history
├── build_exe.py                 # PyInstaller standalone build script
└── main.py                      # Application entry point
```

---

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/your-username/seenow.git
cd seenow

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Copy the example configuration:
```bash
cp config.json.example config.json
```
Edit `config.json` (or configure via the **Settings** tab in the desktop application) to provide your router endpoint and API key:
```json
{
  "router_base_url": "http://localhost:20128/v1",
  "router_api_key": "YOUR_API_KEY_HERE",
  "primary_vision_model": "ag/gemini-3.8-flash-high"
}
```

### 3. Running SeeNOW

```bash
python main.py
```

1. Click **"🚀 Launch / Attach Chrome (CDP Port 9222)"** on the Live HUD.
2. Log in to your quiz portal in the launched browser window.
3. Use `Alt + S` to solve the current question, or `Alt + A` for full automated progression.

---

## 🛠️ Testing & Code Quality

Run the local test and security verification suite:

```bash
# Install developer tools
pip install -r requirements-dev.txt

# Run headless unit tests
pytest

# Code linting
ruff check .

# Static type checking
mypy core

# Security SAST audit
bandit -r core gui main.py -ll
```

---

## 📦 Building Standalone Executable (.exe)

Compile SeeNOW into a standalone, portable Windows binary:

```powershell
python build_exe.py
```
The compiled binary will be located at `dist/SeeNOW/SeeNOW.exe`.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
