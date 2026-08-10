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
  aiox_advanced: 4
  aiox_advanced_squads: 1
  total: 5
  counted_at: '2026-08-10'
---
# Idempotência

Propriedade de uma operação que permite repeti-la com segurança sem disparar trabalho duplicado perigoso ou produzir efeitos duplicados indevidos. No AIOX, é parte do contrato de API quando uma chamada pode sofrer retry ou criar um job.

## Como é usado

Use **Idempotência** na criação de jobs e em qualquer operação que possa ser repetida após timeout, falha parcial ou retry: aceite uma chave de idempotência, associe-a ao chamador autorizado e faça a repetição apontar para o mesmo trabalho, em vez de iniciar outro perigoso. A operação ainda precisa expor status e evidência do resultado.

**Exemplo prático:** na aula [[68-squad-fora-do-claude-code]], o `POST /jobs` recebe um payload versionado e `idempotency-key`. Se a mesma criação for reenviada, a chave evita disparar trabalho duplicado; `GET /jobs/:id` permite acompanhar `queued`, `running` ou um estado terminal.

**Não confunda:** **Idempotência** não significa que a operação nunca falha, nem que toda chamada repetida com payload diferente é a mesma. Também não substitui autenticação, autorização ou [[Tenant isolation]]: a chave identifica a repetição, mas não concede permissão. **Alerta de segurança:** valide o chamador, tenant e role antes de reaproveitar o job; não trate uma chave conhecida como credencial.

**Frequência nos cursos:** **5** menções (AIOX Advanced: 4 · AIOX Advanced Squads: 1).

## Aulas

- [[68-squad-fora-do-claude-code]]
- [[69-escada-progressiva-script-a-saas]]

## Ver também

- [[Contrato de API]]
- [[Tenant isolation]]
- [[Job]]
- [[Runner]]
- [[Quality Gate]]
- [[Glossário AIOX Advanced]]
