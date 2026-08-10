# FAQ da Cohort (T1 + T2) — padrões reais

Perguntas condensadas dos grupos WhatsApp. Respostas no espírito do que Alan e o time responderam (não são citação jurídica; são padrão de operação).

---

### 1. Instalei o PRO e os squads novos não vieram
**Padrão de resposta:** reinstalar/atualizar PRO; se falhar, usar pacote zip da turma + `*validate-squad` e `*upgrade-squad`. Contagem de 90 dias começa na ativação.

**Aulas:** canteiro/setup, 45, 34, 55.

---

### 0. Não acho o material / qual a última versão?

**Padrão de resposta:** não mandar scroll no WhatsApp. Abrir **`cohort-insights/CATALOG.md`**, buscar o pack, usar só **LATEST**. Se precisar do arquivo, reenviar essa versão nomeada.

**Por quê:** T1 export tem 9× squad-creator, 8× design, 6× hormozi. WhatsApp é correio, não repositório.

**Aulas / docs:** `CATALOG.md`, `FINDABILITY.md`, aula `75-faq-cohort-campo` §00.

---


### 2. Posso rodar várias stories em subagents para não estourar contexto?
**Padrão:** isola contexto **por task**, mas **não economiza dinheiro** — N agentes em paralelo multiplicam tokens (ex.: 10 × 80–120k). Use partição de ownership e meça wall-clock.

**Aulas:** 16, 17, 58, 59, 61.

---

### 3. CLAUDE.md global vs por projeto — boa prática?
**Padrão:** o AIOX/bootstrap resolve grande parte; regras do projeto ficam no CLAUDE.md do repo; global é magro. Budget ~150 instruções — 461 linhas é inchado.

**Aulas:** 03, 27 · material `escrevendo-um-bom-claude-md.md`.

---

### 4. Squad creator open source some / sumiu do GitHub
**Padrão:** conteúdo carrega modelo de negócio; caminho é PRO / versão especial da turma, não copiar o núcleo aberto sem curadoria.

**Aulas:** 34, 55.

---

### 5. Ralph pra desenvolvimento?
**Padrão de Alan:** vários Ralphs para **ETL**; **não** para desenvolvimento de feature (risco de colisão e caos).

**Aulas:** 58, 22, 59.

---

### 6. Quando acaba o Max semanal — API?
**Padrão:** API como backup; o jogo de longo prazo é **menos generativo, mais determinístico** (processos, runners).

**Aulas:** 01, 21, 30, 60.

---

### 7. Design system em vários produtos da mesma empresa
**Padrão:** base compartilhada + derivados; DESIGN.md/Storybook como contrato; não reinventar tokens em cada app.

**Aulas:** 41–43, 56–57 · trilha dedicada: `cursos/AIOX-Design/`.

---

### 7b. Já automatizei / montei algo — como monetizo ou viro SaaS?
**Padrão:** isso **não** é FAQ de setup. Capacidade com evidência → Decision Pack (wedge, ROI, canal, formato, estágio). Uso interno ≠ produto. Não abrir hormozi/copy antes do pack.

**Curso:** `cursos/AIOX-Productizacao/` · FAQ: `FAQ-campo-cohort.md` · personas: `personas-capstone.md`.

---

### 8. @ sem / chama agente?
**Padrão:** @ carrega persona; / dispara ritual/comando. Sem processo, a IA “vai pro lugar burro”.

**Aulas:** 45, 14, 15.

---

### 9. Quality Gate e status da task
**Campo T2:** task **não** deve ir pra completed no meio do QG loop — fica `in_progress` até o loop fechar (learning real capturado no grupo).

**Aulas:** 47, 48, 49.

---

### 10. “IA sem processo”
**Citação-guia Alan:** direcionar o sistema pro caminho certo > torcer pro modelo adivinhar. Processo economiza token e nervo.

**Aulas:** 08, 09, 21, 28.
