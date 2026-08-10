---
type: module-quiz
course: aiox-advanced
module: M4
status: canonical
canonical_scope: Cursos/AIOX Advanced
passing_score: 80
question_count: 4
source_version: 1.0.0
tags: [curso/aiox-advanced, avaliacao, quiz]
---

# Quiz M4 — Determinismo e comando

Eu respondo sem consultar as aulas. Depois abro o gabarito, explico cada erro com minhas palavras e volto à evidência do módulo. Minha referência de domínio é 80%.

## Questões

### 1. Determinismo progressivo 30→60→90 serve para:

- A. Eliminar qualquer uso de LLM
- B. Trocar git por FTP
- C. Subir qualidade por gates (self-heal → review → CI)
- D. Aumentar temperature do modelo

### 2. 'Determinístico primeiro, LLM onde gera ouro' recomenda:

- A. Script/runner no mecânico; LLM em decisão/síntese de alto valor
- B. LLM em todo rename de arquivo
- C. Nunca escrever testes
- D. Só Opus em tudo

### 3. Pipeline ETL com agentes organiza falha por:

- A. Uma única mensagem com tudo misturado
- B. Deploy direto no extract
- C. Ignorar dados ruins
- D. Camadas Extract → Transform → Load com donos

### 4. Um processo recorrente falha de um jeito diferente a cada execução. Qual redesenho aumenta a confiabilidade sem eliminar o julgamento útil da IA?

- A. Aumentar o prompt até cobrir toda exceção imaginável
- B. Fixar as etapas repetíveis, reservar o LLM para ambiguidades e colocar gate na saída
- C. Trocar de modelo a cada falha
- D. Remover logs para reduzir contexto

<details>
<summary>Gabarito comentado</summary>

**1. C** — Cada gate compra certeza; FAIL corrige e repete o portão.

**2. A** — Fitness da tarefa define o executor/modelo.

**3. D** — Camada isola falha e ferramenta certa.

**4. B** — Determinismo progressivo desce o que é mecânico para regras e mantém julgamento generativo apenas onde ele cria valor.

</details>

## Transferência

Eu produzo esta evidência no meu projeto: Um processo real decomposto por camada, com Goal ou Loop escolhido, stop rule e tratamento de falha.

## Navegação

↑ [[modulos/Módulo 4 - Determinismo e Comando|M4]] · [[Assessments|Todas as avaliações]]
