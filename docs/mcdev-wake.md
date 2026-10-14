# Waking Claude for feedback (#45 → #46): options and a proposal

The user asked (#46) for Claude to be woken periodically to batch-process feedback "as part of the framework".
Today the main session arms a session-only cron (CronCreate, every 15 min). It dies with the session, expires after 7 days,
and a new session has no wake-up until someone re-arms it. Nothing below is implemented. Anything that runs Claude
unattended needs the user's OK first.

Checked on 2026-10-15 against Claude Code 2.1.280 (`claude --help`) and the docs at code.claude.com/docs/en/…

## What Claude Code offers

| Mechanism | Durable? | Reaches localhost / .mcdev? | Notes |
|---|---|---|---|
| `/loop`, CronCreate (current) | No: session only, 7-day expiry, restored by `--resume` | yes | Fires only while that session is open and idle (scheduled-tasks.md). |
| Desktop app scheduled tasks | Yes (`~/.claude/scheduled-tasks/`) | yes | Needs the Desktop app open. The user works in the CLI. (desktop-scheduled-tasks.md) |
| Cloud routines (`/schedule`) | Yes | **no** | Runs in Anthropic's cloud on a fresh git clone, so it can't see feedback.log, RCON or the servers. 1 h minimum interval. (routines.md) |
| Self-hosted environments | Yes | yes | Research preview, Team/Enterprise only, runner to maintain. Overkill here. |
| Hooks (`SessionStart`, `FileChanged`, …) | Config is durable (in repo) | yes | No timer or external-event hook. A `SessionStart` hook can add context to every new or resumed session, but it can't wake an idle one. |
| Channels (MCP push into a running session) | No | yes | Research preview. Not in this CLI's `--help`, so unverified here. Only delivers while a session is open. |
| Headless `claude -p` | One-shot | yes | `--permission-mode dontAsk`, `--allowedTools`, `--permission-prompts none`, `--max-budget-usd`, `--output-format json`. |
| Background sessions `claude --bg [--resume <id>] "prompt"` | Until reboot | yes | `--bg --resume <id>` continues that session in the background, or starts a copy if it's already running. `claude agents --json` lists active sessions. (A `claude message <id>` command was suggested but **doesn't exist** in 2.1.280.) |

## Recommendation

**Step 1 (cheap, no unattended runs; needs only a settings change the user approves):** add a project hook in
`.claude/settings.json`: `SessionStart` → `python tools/mcdev.py feedback --summary` (a small new flag: unread count + titles).
Every new or resumed session starts knowing what's queued, and CLAUDE.md tells it to re-arm the 15-min feedback cron.
The wake-up then becomes part of the repo instead of one session's memory. It still needs an open session.

**Step 2 (the real "framework wakes Claude"; needs explicit approval because it runs Claude unattended):** the mcdev daemon
becomes the scheduler:
- Trigger: unread feedback exists, then it's been quiet for 10 min (the user stopped typing), with at most 1 run per 30 min.
  Nothing runs while no feedback is waiting.
- Skip if an interactive session is working in this repo (`claude agents --json`, cwd = repo), so it never races the main
  session on `main`. In that case it only writes the wake note to the inbox.
- Run: `claude -p "<batch prompt>" --permission-mode dontAsk --permission-prompts none --max-budget-usd 2 --output-format json`
  with `--allowedTools "Read,Grep,Glob,Bash(python tools/mcdev.py feedback*),Bash(python tools/mcdev.py notify*),Bash(git log*)"`.
  - The batch prompt: read `mcdev feedback`, triage into docs/feedback-queue (or a PROGRESS.md section), answer the
    user through `mcdev notify`, and **don't** edit code, merge or restart servers. Code work stays with the main
    session, which reads the triage at its next checkpoint.
- Log each run (cost, session id, result) to `.mcdev/wake.log`; turned on by a flag file `.mcdev/wake.enabled`.
- Alternative to `-p`: keep one framework-owned worker session id in `.mcdev/wake.json` and run `claude --bg --resume <id> "<batch prompt>"`,
  so triage keeps its context between runs. This is more fragile (it dies at reboot, and resuming a running session forks a copy), so it's not the first choice.

**Not recommended:** cloud routines (they can't reach the local servers or files), Desktop scheduled tasks (wrong client),
channels (preview, unverified in this CLI).

## Questions for the user
1. OK to add the `SessionStart` hook (step 1)?
2. OK for the daemon to start headless Claude runs on new feedback (step 2), at a budget of about US$2 per run? Should they only
   triage and reply, or also fix small things?
