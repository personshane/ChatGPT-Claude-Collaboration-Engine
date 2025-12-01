# MP-1.3 SPECIFICATION — CORE EXECUTION LOOP

## PURPOSE
Establish the foundational execution loop mechanism that enables ChatGPT to issue micro-project instructions and Claude to execute them in a deterministic, traceable manner.

## EXECUTION TRIGGER
The engine loop activates when:
1. A file is detected at `/Claude_Inbox/incoming_microproject.txt`
2. The file contains valid micro-project instructions
3. The header follows the format: `# MP-X.Y`

## CLAUDE RESPONSE PROTOCOL
When a micro-project is detected, Claude MUST:
1. Read the entire incoming_microproject.txt file
2. Extract the MP identifier from the header (e.g., "MP-1.3")
3. Update SESSION_STATE.json:
   - Set `current` to the MP identifier
   - Set `status` to "RUNNING"
4. Execute ALL instructions in the micro-project EXACTLY as written
5. Create result file at `/SYSTEM/RESULT_last.md` with:
   - Micro-project ID
   - Execution status
   - Any outputs, errors, or confirmations
6. Update SESSION_STATE.json:
   - Set `last_completed` to the MP identifier
   - Set `current` to "IDLE"
   - Set `status` to "ONLINE"
7. Delete the incoming_microproject.txt file
8. HALT and wait for ChatGPT to issue the next micro-project

## CHATGPT ORCHESTRATION
ChatGPT will manage the collaboration loop by:
1. Creating `/Claude_Inbox/incoming_microproject.txt` with micro-project instructions
2. Committing and pushing to GitHub
3. Waiting for Claude to pull, execute, and push results
4. Pulling Claude's results from GitHub
5. Verifying execution correctness
6. Issuing the next micro-project or corrective instructions

## ERROR HANDLING EXPECTATIONS
If Claude encounters ANY error during execution:
1. STOP immediately
2. Log the FULL error output
3. Diagnose the root cause
4. Propose EXACTLY ONE fix
5. Write error details to `/SYSTEM/RESULT_last.md`
6. Update SESSION_STATE.json status to "ERROR"
7. HALT and wait for ChatGPT approval before proceeding

## STATE MANAGEMENT
SESSION_STATE.json maintains:
- `engine_version`: Current engine version
- `last_completed`: Last successfully completed micro-project ID
- `current`: Currently executing micro-project ID (or "IDLE")
- `status`: Engine status (ONLINE, RUNNING, ERROR, OFFLINE)
- `last_updated`: ISO timestamp of last state update

## LOOP ARCHITECTURE
```
┌─────────────────────────────────────────────────────────┐
│  ChatGPT writes MP → GitHub → Claude pulls → Execute   │
│  Claude writes result → GitHub → ChatGPT pulls → Verify │
└─────────────────────────────────────────────────────────┘
```

## SUCCESS CRITERIA
The loop is functioning correctly when:
1. Micro-projects execute deterministically
2. Results are traceable and verifiable
3. State transitions are logged accurately
4. No drift or hallucinations occur
5. GitHub serves as single source of truth

## VERSION
Engine Loop Version: 1.0
Protocol Version: v1.0
Specification Version: MP-1.3

---
**END OF SPECIFICATION**
