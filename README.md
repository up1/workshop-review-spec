# Review Specification
* Agent Skills
  - Writing and reviewing specifications for AI-assisted development
  - Ensuring AI-friendly system architecture and structure
* Claude's Hooks
  - PreToolUse: Executes custom hooks before using tools like write_file, edit_file, patch_file, and execute_bash.
    - Example: `.claude/hooks/spec_gate.py` can be used to enforce specification compliance before any file modifications.

## Features
* Generate specifications for AI-assisted development tasks
* Review and enforce compliance with existing specifications before file modifications
* Integrate seamlessly with Claude's hook system for pre-tool use checks
