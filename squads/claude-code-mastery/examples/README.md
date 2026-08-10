# Claude-Code-Mastery Squad — Production Examples

Outputs do squad `claude-code-mastery` são configurações de Claude Code, hooks, skills, MCP integrations e agent definitions que vivem em `.claude/`.

## Onde os outputs reais vivem

| Tipo | Localização |
|---|---|
| Hooks configurados | `.claude/hooks/` + `settings.json` |
| Skills instaladas | `.claude/skills/` |
| Subagent definitions | `.claude/agents/` |
| Slash commands | `.claude/commands/` |
| MCP configs | `.mcp.json` |
| Claude Code settings | `settings.json`, `settings.local.json` |

## Evidência de uso

- 80+ skills instaladas e ativas
- Hooks configurados (pre-push-validation, ide-sync, etc.)
- Subagents customizados (`claude-mastery-chief`, `claude-code-guide`)
- MCP gateway integration em produção
- Integração com Claude API / Anthropic SDK em apps

## Tasks canônicas

- Claude Code configuration, hooks setup, skill/agent creation
- Anthropic SDK best practices (prompt caching, model selection, tool use)

## Provenance

Squad governa a própria infraestrutura Claude Code do repo. Configurações ativas são a evidência de uso — `.claude/` inteira é output do squad.
