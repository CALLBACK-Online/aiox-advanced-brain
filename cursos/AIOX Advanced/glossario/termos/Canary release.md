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
  aiox_advanced: 9
  aiox_advanced_squads: 0
  total: 9
  counted_at: '2026-08-10'
---
# Canary release

Estratégia de liberar uma versão para uma pequena parcela controlada de tráfego, usuários ou instâncias antes de ampliar a exposição. O objetivo é reduzir o blast radius e validar o comportamento em condições reais.

## Como é usado

Use **Canary release** com público ou percentual explícito, janela de observação, métricas de saúde e negócio, critério de promoção e critério de abortar. O responsável deve conseguir expandir ou interromper a exposição sem heroísmo.

**Exemplo prático:** a versão `v2.4.0` recebe 5% do tráfego de checkout por 15 minutos. O operador acompanha erro, latência e conversão; sem regressão, amplia para 25% e 100%. Se o erro passar do limite, interrompe a expansão e executa [[Rollback]].

**Não confunda:** **Canary release** define a exposição gradual da versão; **Feature flag** controla a ativação de uma capacidade. Canary não é apenas deploy em staging nem uma flag desligada: exige tráfego real, observação e uma decisão de ampliar ou abortar.

**Frequência nos cursos:** **9** menções (AIOX Advanced: 9 · AIOX Advanced Squads: 0).

## Aulas

- [[53-brownfield-enhancement]]
- [[48-quality-gate-completo]]
- [[73-prontidao-de-producao]]

## Ver também

- [[Feature flag]]
- [[Release]]
- [[Deploy]]
- [[Rollback]]
- [[Smoke test]]
- [[Glossário AIOX Advanced]]
