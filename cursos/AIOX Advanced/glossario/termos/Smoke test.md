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
  aiox_advanced: 11
  aiox_advanced_squads: 0
  total: 11
  counted_at: '2026-08-10'
---
# Smoke test

Checagem rápida pós-deploy: o caminho crítico funciona de verdade? Evidência mínima de que o ambiente responde.

## Como é usado

Rode o **Smoke test** imediatamente após cada deploy: percorra o caminho crítico do produto (a página abre, o login funciona, a ação principal responde) para provar que o ambiente está vivo antes de qualquer anúncio ou próximo passo.

**Exemplo prático:** na aula [[73-prontidao-de-producao]], depois do deploy o operador confere o essencial: `GET /` retorna 200, o login de teste entra e a ação principal completa; se qualquer passo falha, é rollback ou correção imediata — e o resultado fica registrado como evidência.

**Não confunda:** **Smoke test** não substitui a suíte de testes: é a evidência mínima de que o ambiente responde, não cobertura de comportamento — passar no smoke não prova que tudo funciona, só que nada crítico está morto.

**Frequência nos cursos:** **11** menções (AIOX Advanced: 11 · AIOX Advanced Squads: 0).

## Aulas

- [[73-prontidao-de-producao]]
- [[71-vercel-deploy]]
- [[72-cicd-pipeline-completa]]

## Ver também

- [[Deploy]]
- [[Evidência]]
- [[Health check]]
- [[Glossário AIOX Advanced]]
