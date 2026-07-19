# Environments

How the stack degrades or strengthens per surface. Load at the start of every run.

## Cowork (home)

Full stack. Subagents available for the fresh-context verifier, Python and shell execute the scripts, files persist in the mounted folder. Harness inheritance applies: state files and deliverables go to the harness output folder (OUTPUTS/YYYY-MM-DD/) with versioned names, harness validators (SKILLS/_validators/) join the machine checks, the verification phase maps onto the harness verify step. Announce exact paths.

## Claude Code

Full stack, plus native /goal (v2.1.139 and later): a completion condition checked after every turn by a prompt-based Stop hook running the configured small fast model (Haiku by default). Interplay rules:

- Native /goal is a free extra gate, not a replacement. It checks the condition as written, so its value equals the contract's sharpness. Feed it the contract's success stop as the condition, interactively or headless (claude -p "/goal <condition>" runs the loop to completion in one invocation).
- The native evaluator reads only the conversation. It cannot run commands or open files. When translating the contract's success stop into a condition, phrase every criterion as pasted proof ("the verify_contract.py output showing all checks PASS is pasted in chat"), never promised proof. Mirror the contract's cap stop as a turn clause inside the condition ("or stop after N turns").
- Condition cap is 4,000 characters and one goal per session (a new /goal replaces the old), so feed it the success stop, not the whole contract. The contract file stays the source of truth.
- The deterministic gate still runs. The native evaluator is a model reading a condition, the script is a program reading facts. Keep both.
- Native goals survive session resume (the condition carries over, turn and token counters reset), which complements the state files, it does not replace them: the progress file carries evidence and iteration history that no evaluator condition holds.
- Gates: /goal needs the workspace trust dialog accepted and is unavailable under disableAllHooks or allowManagedHooksOnly. When native /goal is unavailable, the skill's own loop carries the run unchanged.

## Codex (translate, do not emulate)

Codex has its own Goal system (six-element contract, evidence-gated, lifecycle commands) and Automations for recurring work. Running this skill's loop inside Codex duplicates a native mechanism badly. Instead: build the contract here (CONTRACT mode), then compose with the loop-goal-engineer skill to translate it into a six-element Codex /goal, mapping outcome to outcome, machine checks plus judgment criteria to the verification surface, scope to boundaries, iteration policy across directly, blocked stop across directly. Hand off and stop.

## Plain chat (degraded, say so)

No subagents, no script execution. The protocol:

- Machine checks become manual checks performed one at a time with results quoted (count the sections, search for forbidden strings, state each result).
- Fresh-context verification becomes staged self-verification: finish the artifact, then re-read the contract alone, then grade the artifact against it criterion by criterion with quoted evidence, without re-reading the working reasoning. Weaker than a real fresh context, label it: "self-verified, degraded mode."
- State files become chat-visible blocks the user can copy out.

Degraded mode is honest about being degraded. The report always names which mode verified the work.
