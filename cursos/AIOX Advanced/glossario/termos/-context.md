---
type: glossary-term
course: aiox-advanced
tags:
- glossario
- aiox
- course-brain
updated: '2026-08-10'
status: reference
canonical_scope: cursos/AIOX Advanced
freq:
  aiox_advanced: 34
  aiox_advanced_squads: 0
  total: 34
  counted_at: '2026-08-10'
---
# /context

O comando que mostra a ocupação da janela: system prompt, arquivos e histórico.

## Como é usado

Rode **/context** antes de missões longas ou quando o agente começar a errar: a saída mostra quanto da janela está ocupado por system prompt, ferramentas/MCPs, arquivos carregados e histórico da conversa — e é essa leitura que orienta a decisão de compactar, remover fontes ou abrir sessão nova.

**Exemplo prático:** na aula [[16-janela-de-contexto]], o operador roda **/context** no meio de uma sessão extensa e descobre que MCPs conectados e histórico já consomem a maior parte da janela; antes de continuar a implementação, desconecta os MCPs ociosos e compacta a conversa para devolver espaço útil ao agente.

**Não confunda:** **/context** só diagnostica, não libera espaço — quem compacta, desconecta MCP ou reinicia a sessão é o operador. Também não é a janela de contexto em si: é o instrumento que mede a ocupação dela.

**Frequência nos cursos:** **34** menções (AIOX Advanced: 34 · AIOX Advanced Squads: 0).

## Aulas

- [[16-janela-de-contexto]]

## Ver também

- [[Glossário AIOX Advanced]]
