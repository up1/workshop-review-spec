#!/usr/bin/env python3
import sys
import json
import os
import re

def log_error(message):
    print(f"[SpecGate Error]: {message}", file=sys.stderr)

def validate_spec_content(filepath):
    if not os.path.exists(filepath):
        return False, f"Specification file '{filepath}' does not exist."
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Required sections check (Case-insensitive markdown headers)
    has_goal = re.search(r'(?i)#+\s*goal', content)
    has_scope = re.search(r'(?i)#+\s*scope', content)
    has_ac = re.search(r'(?i)#+\s*(acceptance\s*criteria|ac)', content)
    
    missing = []
    if not has_goal: missing.append("Goal")
    if not has_scope: missing.append("Scope (IN/OUT)")
    if not has_ac: missing.append("Acceptance Criteria (AC)")
    
    if missing:
        return False, f"Missing required sections in spec: {', '.join(missing)}"
    
    return True, "Specification is valid."

def main():
    # Claude Code passes tool execution context via stdin or arguments
    try:
        hook_input = json.load(sys.stdin)
    except Exception:
        # Fallback if invoked outside standard JSON stdin pipeline
        sys.exit(0)

    tool_name = hook_input.get("tool", "")
    tool_args = hook_input.get("arguments", {})
    
    # Target only write/edit operations
    code_modifying_tools = ["edit_file", "write_file", "patch_file", "execute_bash"] 
    if tool_name not in code_modifying_tools:
        sys.exit(0) # Allow read-only tools to pass freely
        
    # Check for a spec directory
    spec_dir = "specs"
    if not os.path.exists(spec_dir) or not os.path.listdir(spec_dir):
        log_error("No specifications found in the '/specs' directory. You must create a Spec Template first.")
        sys.exit(1) # Block execution
        
    # Find the most relevant spec file or latest active spec
    # For advanced setups, map the target file path in tool_args to a specific spec
    spec_files = [os.path.join(spec_dir, f) for f in os.listdir(spec_dir) if f.endswith('.md')]
    
    valid_spec_found = False
    errors = []
    
    for spec in spec_files:
        is_valid, msg = validate_spec_content(spec)
        if is_valid:
            valid_spec_found = True
            break
        else:
            errors.append(f"{os.path.basename(spec)}: {msg}")
            
    if not valid_spec_found:
        log_error("Code modification blocked. No complete specification passed the gate.")
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        print("\nPlease ensure your specification includes:\n1. # Goal\n2. # Scope\n3. # Acceptance Criteria", file=sys.stderr)
        sys.exit(1) # Reject tool use

    # Pass validation
    sys.exit(0)

if __name__ == "__main__":
    main()
