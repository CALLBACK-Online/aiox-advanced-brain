---
type: quiz
course: aiox-advanced
module: M1
question_count: 8
passing_score: 80
status: canonical
canonical_scope: cursos/AIOX Advanced
---
# Quiz M1 — Sistema e contexto

### 1. Qual regra pertence ao contrato local do projeto?
A. Preferência temporária do chat
B. Invariante que toda execução deve respeitar
C. Segredo de produção
D. Saída de um teste

### 2. Por que separar local, staging e production?
A. Para controlar risco e promover evidência entre ambientes
B. Para duplicar trabalho
C. Para evitar versionamento
D. Para usar modelos diferentes

### 3. Qual é um sinal de contexto degradado?
A. Mais arquivos
B. Menos mensagens
C. Respostas perdem restrições e decisões antigas
D. O build fica mais rápido

### 4. Como reduzir drift no contexto?
A. Adicionar todas as conversas
B. Apagar critérios de aceite
C. Usar apenas memória do modelo
D. Manter instruções curtas, hierárquicas e fontes canônicas

### 5. Toda manhã uma task converte um CSV em JSON com regra fixa e saída sempre igual. Hoje um agent de IA faz isso. Qual é o executor certo?
A. Agent: a IA é a ferramenta mais capaz disponível
B. Clone: preserva o seu jeito de transformar os dados
C. Humano: só ele garante a qualidade da conversão
D. Worker: regra clara e saída fixa pedem script determinístico, barato e confiável

### 6. Uma config editada na mão pelo time vive em JSON e quebra toda semana por vírgula ou aspas faltando. O que fazer?
A. Adicionar um validador de JSON no CI e manter o formato
B. Migrar para YAML: config que humano edita pede formato legível, sem ruído de parsing
C. Converter para tabela em Markdown, que organiza melhor
D. Instruir o LLM a corrigir o JSON sempre que quebrar

### 7. O time decidiu que só o @devops pode dar push e criar release. Onde essa regra deve morar?
A. Na Constitution: ela governa comportamento e autoridade, é artigo não-negociável
B. No CLAUDE.md, para o agente ler em toda sessão
C. No core-config, ligando a capacidade de push
D. Numa rule com paths, restrita à pasta de deploy

### 8. Seu CLAUDE.md carrega uma tabela de 80 linhas de endpoints que o agente raramente consulta. Qual operação de otimização aplicar?
A. Enxugar: comprimir a tabela para 40 linhas
B. Reescrever a tabela em SE/ENTÃO imperativo
C. Quebrar em link: mover a tabela para um doc dedicado e deixar um ponteiro de uma linha
D. Apagar a tabela: detalhe não pertence ao contexto do projeto

<details><summary>Gabarito</summary>

**1. B** · **2. A** · **3. C** · **4. D** · **5. D** · **6. B** · **7. A** · **8. C**
</details>

## Transferência
Audite uma instrução local e remova redundância sem perder invariantes.
