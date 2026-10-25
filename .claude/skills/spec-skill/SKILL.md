---
name: spec-skill
description: Enforces a Spec-First Development Workflow by ensuring that code modifications are only allowed when a valid specification document exists. Include keywords that help agents identify relevant tasks.
---

# Spec-First Architecture Guard

You operate under a strict **Spec-First Development Workflow**. You are explicitly forbidden from modifying, creating, or deleting source code files without an active, verified, and complete Specification Document.

## The Spec Gate Rule
A automated Pre-Tool Hook (`spec_gate.py`) actively monitors all code-modifying tools (`write_file`, `edit_file`, `patch_file`, `execute_bash`). 
* If you attempt to modify code without an approved specification file in the `specs/` directory, the hook will fail execution.
* Do not attempt to bypass the hook. Instead, immediately pivot to generating or correcting the required specification.

## Required Specification Structure
Every specification file created under `specs/*.md` must strictly contain the following sections to pass verification:

1. **# Goal**: A clear description of the problem, the business value, and the high-level technical objective.
2. **# Scope**: Must explicitly break down boundaries into sub-headers:
   - `### IN`: Items, modules, and changes included in this task.
   - `### OUT`: Expressly stated elements or features excluded from this task to prevent scope creep.
3. **# Acceptance Criteria (AC)**: A definitive checklist of conditions that must be satisfied for the task to be marked complete.

## Execution Workflow
1. **Discover/Create Spec**: Check the `specs/` directory. If a spec for the active task does not exist, use `write_file` to create one using the template.
2. **Refine & Verify**: Fill out the Goal, Scope, and AC completely.
3. **Invoke Implementation**: Once the spec file is cleanly saved and valid, proceed with your standard code modification tools. The gate will dynamically read your spec and allow the execution to pass.
