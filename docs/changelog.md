## [1.1.0] – 2025-04-30

### Added
- **Launch_LLM-Powered_RAG_Assistant.bat**  
  - Replaces the old `Launch_CLI_Assistant.bat`.  
  - Initializes the LLM-powered RAG environment, sets up plugin paths and virtual-env activation automatically.
- **llm_orchestrator_with_plugins.py**  
  - Replaces `jarvis_no_voice.py`.  
  - **Intellisense support**: dynamic tab-completion for commands and plugin names.  
  - **Plugin framework**: built-in connectors for VirusTotal, AbuseIPDB, urlscan.io (via `plugin_ioc`), plus placeholders for future CTI plugins.  
  - **Command-dispatch engine**: robust parsing and error handling for new `plugin_ioc`, `plugin_shodan`, etc.  
  - **Investigation evidence output**: automatically writes all report artifacts into an `investigation_evidence/` folder.  
  - **On-screen dashboard**: a new “view” mode to highlight key findings (summary stats, top IOCs, timing).

### Changed
- Removed legacy files:
  - `Launch_CLI_Assistant.bat`
  - `jarvis_no_voice.py`
- Directory layout updated to include:
  - `investigation_evidence/` (default output for logs, exports, screenshots)

### Fixed
- Corrected a syntax error around the `elif command == 'plugin_ioc'` block.
- Addressed path-resolution bugs to ensure all plugin modules load regardless of working directory.
- Improved exception handling for failed API calls (now logs and continues rather than crashing).

### Documentation
- **README.md** updated:
  - New quick-start instructions for `Launch_LLM-Powered_RAG_Assistant.bat`
  - Examples of plugin commands and the on-screen view mode.
- Added detailed inline docstrings to `llm_orchestrator_with_plugins.py` for easier maintenance.

### Miscellaneous
- Standardized logging format (timestamps + log levels).
- Streamlined batch-file header comments to clarify required prerequisites.
