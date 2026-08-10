# Changelog

## 2026-07-06 — .claude/skills/roundtable/SKILL.md

Movido para fora do contexto carregado.

## Change Log

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | 2026-03-28 | Initial release — review mode only, 9 atoms, 5 presets |
| v1.1 | 2026-03-28 | Gap analysis + meta-roundtable findings: +6 modes, +12 tokens, +6 presets, +tiered limits, +flags, +logging, +state machine, +artifact lifecycle |
| v2.0 | 2026-03-28 | **REAL AGENTS:** Agent tool with run_in_background. context: conversation. Personas from .claude/agents/. |
| v2.1 | 2026-03-28 | **AGENT TEAMS:** Upgraded from Agent(run_in_background) to TeamCreate + Agent(team_name) + SendMessage. Teammates persist, communicate bidirectionally, show colored names. ATM-RT-006 uses SendMessage to wake idle teammates instead of re-spawning. Shutdown + TeamDelete on completion. |
| v2.3.0 | 2026-06-09 | Orchestration Telemetry section absorbed from sinkra-v5 cohort edition (kept v2.1 fallback/feature-detection base). |

