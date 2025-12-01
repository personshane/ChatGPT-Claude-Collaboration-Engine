#!/usr/bin/env python3
"""
CHATGPT ⇄ CLAUDE COLLABORATION ENGINE - CORE EXECUTION LOOP
Version: 1.0
Purpose: Monitors for incoming micro-projects and executes them according to Protocol v1.0
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path

# Path Configuration
REPO_ROOT = Path(__file__).parent.parent
INBOX_PATH = REPO_ROOT / "Claude_Inbox" / "incoming_microproject.txt"
STATE_PATH = REPO_ROOT / "STATE" / "SESSION_STATE.json"
RESULT_PATH = REPO_ROOT / "SYSTEM" / "RESULT_last.md"

def log(message):
    """Simple logging with timestamp"""
    timestamp = datetime.utcnow().isoformat() + "Z"
    print(f"[{timestamp}] {message}")

def read_session_state():
    """Load current session state from JSON"""
    try:
        with open(STATE_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        log("WARNING: SESSION_STATE.json not found, creating default")
        return {
            "engine_version": "1.0",
            "last_completed": "NONE",
            "current": "IDLE",
            "status": "OFFLINE",
            "last_updated": datetime.utcnow().isoformat() + "Z"
        }

def write_session_state(state):
    """Save session state to JSON"""
    state["last_updated"] = datetime.utcnow().isoformat() + "Z"
    with open(STATE_PATH, 'w') as f:
        json.dump(state, f, indent=2)
    log(f"Session state updated: {state['current']} -> {state['status']}")

def parse_mp_header(content):
    """Extract MP identifier from content (e.g., '# MP-1.3')"""
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('# MP-'):
            return line[2:].strip()  # Returns "MP-1.3"
    return "UNKNOWN"

def execute_microproject():
    """Main execution function when incoming MP detected"""
    log("=" * 70)
    log("INCOMING MICRO-PROJECT DETECTED")
    log("=" * 70)
    
    # Read incoming micro-project
    with open(INBOX_PATH, 'r') as f:
        mp_content = f.read()
    
    mp_id = parse_mp_header(mp_content)
    log(f"Micro-Project ID: {mp_id}")
    
    # Update state: RUNNING
    state = read_session_state()
    state["current"] = mp_id
    state["status"] = "RUNNING"
    write_session_state(state)
    
    log(f"Executing {mp_id}...")
    log("Instructions:")
    log("-" * 70)
    log(mp_content)
    log("-" * 70)
    
    # NOTE: Actual execution logic would go here
    # For now, this is a framework - Claude must execute manually
    log("MANUAL EXECUTION REQUIRED")
    log("Claude must read and execute the micro-project instructions")
    
    # Create result file
    result_content = f"""# EXECUTION RESULT
Micro-Project: {mp_id}
Status: AWAITING_MANUAL_EXECUTION
Timestamp: {datetime.utcnow().isoformat()}Z

The micro-project has been detected and logged.
Claude must now execute the instructions manually and update this result file.
"""
    
    with open(RESULT_PATH, 'w') as f:
        f.write(result_content)
    
    log(f"Result written to: {RESULT_PATH}")
    
    # Delete incoming file
    os.remove(INBOX_PATH)
    log("Incoming micro-project file deleted")
    
    # Update state: IDLE
    state["last_completed"] = mp_id
    state["current"] = "IDLE"
    state["status"] = "ONLINE"
    write_session_state(state)
    
    log("=" * 70)
    log(f"{mp_id} LOGGED - AWAITING MANUAL EXECUTION")
    log("=" * 70)

def watch_for_microprojects():
    """Main loop - watches for incoming micro-projects"""
    log("COLLABORATION ENGINE STARTED")
    log(f"Watching for incoming micro-projects at: {INBOX_PATH}")
    
    state = read_session_state()
    state["status"] = "ONLINE"
    write_session_state(state)
    
    while True:
        if INBOX_PATH.exists():
            try:
                execute_microproject()
            except Exception as e:
                log(f"ERROR: {str(e)}")
                state = read_session_state()
                state["status"] = "ERROR"
                write_session_state(state)
        
        time.sleep(2)  # Check every 2 seconds

if __name__ == "__main__":
    # Ensure required directories exist
    (REPO_ROOT / "Claude_Inbox").mkdir(exist_ok=True)
    (REPO_ROOT / "SYSTEM").mkdir(exist_ok=True)
    (REPO_ROOT / "STATE").mkdir(exist_ok=True)
    
    watch_for_microprojects()
