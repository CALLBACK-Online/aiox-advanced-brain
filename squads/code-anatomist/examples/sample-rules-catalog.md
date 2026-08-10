# Catálogo de Regras: Redactia

**Data:** 2026-03-23
**Agente:** Graham Witt (Tier 3) - Expressão em Linguagem Natural
**Público:** Misto (técnico + negócio)
**Padrão:** Vocabulário controlado, sem ambiguidade

---

## Vocabulário Controlado

| Termo | Definição | Contexto |
|-------|-----------|----------|
| **Redação** | Texto dissertativo-argumentativo submetido por um aluno para avaliação | Redactia |
| **Competência** | Uma das 5 dimensões de avaliação ENEM (C1 a C5), cada uma pontuada de 0 a 200 | Redactia |
| **Nota global** | Soma das 5 competências, variando de 0 a 1000 | Redactia |
| **OCR** | Reconhecimento óptico de caracteres: extração de texto manuscrito a partir de imagem/PDF | Redactia |
| **Confiança** | Valor numérico de 0.0 a 1.0 que indica a certeza do OCR sobre uma palavra extraída | Redactia |
| **Confiança global** | Média aritmética da confiança de todas as palavras extraídas | Redactia |
| **Rasura** | Texto que o aluno intencionalmente riscou na folha de redação | Redactia |
| **Palavra incerta** | Palavra cuja confiança de OCR está entre 0.40 e 0.60 | Redactia |
| **Revisão humana** | Processo onde um professor verifica e corrige o texto extraído pelo OCR antes da correção automática | Redactia |
| **Roteamento** | Decisão automática de enviar a redação para correção imediata ou para fila de revisão humana | Redactia |
| **Organização** | Instituição de ensino (escola, cursinho) que utiliza o Redactia no modelo B2B | Redactia |
| **Turma** | Grupo de alunos dentro de uma organização, associado a um professor | Redactia |
| **Reforço** | Indicação de que um aluno precisa de atenção especial em uma competência (score < 100) | Redactia |

---

## 1. Regras de OCR e Roteamento

### 1.1 Extração de texto

**R-001.** O sistema DEVE extrair texto apenas da região do corpo da página, definida como a área entre 10% e 92% da altura total da página.

**R-002.** O sistema DEVE ignorar texto localizado nas margens laterais, definidas como a área abaixo de 8% e acima de 92% da largura total da página.

**R-003.** O sistema DEVE ignorar números de 1 a 30 que apareçam no início de uma linha, pois são numeração impressa da folha de redação.

**R-004.** O sistema DEVE ignorar palavras que correspondam a padrões de texto impresso (logotipos, instruções, marcas d'água), conforme lista de 60+ padrões cadastrados.

**R-005.** O sistema DEVE reconstituir palavras hifenizadas entre linhas. Exemplo: "desenvol-" seguido de "vimento" na próxima linha se torna "desenvolvimento".

**R-006.** O sistema DEVE identificar quebras de parágrafo quando o espaço vertical entre duas linhas exceder 1.8 vezes a altura média das linhas.

### 1.2 Marcação de confiança

**R-007.** Cada palavra extraída DEVE receber uma das seguintes marcações, conforme sua confiança:

| Confiança | Marcação | Significado |
|-----------|----------|-------------|
| 0.85 ou mais | Nenhuma | Palavra clara, avaliar normalmente |
| 0.60 a 0.84 | Nenhuma | Palavra aceitável, avaliar normalmente |
| 0.40 a 0.59 | [palavra?] | Palavra incerta, avaliar com cautela |
| Abaixo de 0.40 | [RASURA] | Texto riscado, ignorar na avaliação |

### 1.3 Validação linguística

**R-008.** Após a extração, o sistema DEVE verificar as palavras contra um dicionário de português brasileiro, desde que o texto contenha pelo menos 10 palavras verificáveis.

**R-009.** Antes da verificação no dicionário, o sistema DEVE excluir:
- Palavras com menos de 3 caracteres
- Palavras presentes na lista de 150+ termos comuns do ENEM
- Palavras iniciadas com letra maiúscula (nomes próprios)
- Siglas (todas maiúsculas com 5 ou menos caracteres)
- Fragmentos morfológicos (sufixos como "ção", "mente", "dade")
- Palavras com mais de 15 caracteres (palavras compostas/técnicas)

**R-010.** Se pelo menos 1 palavra não for encontrada no dicionário após os filtros, o sistema DEVE encaminhar a redação para revisão humana.

### 1.4 Decisão de roteamento

**R-011.** O sistema DEVE calcular a confiança global como a média aritmética da confiança de todas as palavras extraídas do corpo da redação.

**R-012.** O sistema DEVE calcular a razão de incerteza como: (quantidade de palavras com confiança abaixo de 0.60) dividido pelo (total de palavras extraídas).

**R-013.** A decisão de roteamento DEVE seguir esta ordem de prioridade:

1. Se a validação linguística detectou palavras desconhecidas: encaminhar para **revisão humana**
2. Se a confiança global é 0.80 ou mais E a razão de incerteza é 0.05 ou menos: encaminhar para **correção automática**
3. Se a confiança global é 0.72 ou mais (mas não atende ao critério acima): encaminhar para **correção automática com alerta**
4. Caso contrário: encaminhar para **revisão humana**

**R-014.** A validação linguística (regra 1) TEM PRIORIDADE ABSOLUTA sobre os critérios de confiança numérica. Mesmo com confiança global de 100%, se houver palavra desconhecida no dicionário, a redação vai para revisão humana.

### 1.5 Revisão humana

**R-015.** Redações encaminhadas para revisão humana DEVEM receber o status "pending_review" e NÃO DEVEM ser enviadas para correção automática até que um professor aprove o texto.

**R-016.** Ao aprovar a revisão, o professor PODE aceitar o texto como está ou salvar correções manuais.

**R-017.** Após a aprovação do professor, o texto corrigido DEVE ter pelo menos 50 caracteres para ser enviado à correção automática.

---

## 2. Regras de Avaliação (LLM Scoring)

### 2.1 Competências ENEM

**R-018.** Cada redação DEVE ser avaliada em exatamente 5 competências:

| ID | Competência | O que avalia |
|----|------------|--------------|
| C1 | Domínio da Norma Culta | Ortografia, morfossintaxe, concordância, construção de período |
| C2 | Compreensão do Tema | Cobertura do tema proposto, consistência argumentativa, repertório sociocultural |
| C3 | Seleção e Organização | Macroestrutura textual, progressão lógica, coesão entre partes |
| C4 | Mecanismos Linguísticos | Conectores, pronomes, concordância textual, recursos coesivos |
| C5 | Proposta de Intervenção | Clareza, viabilidade, detalhamento da proposta, respeito aos direitos humanos |

**R-019.** Cada competência DEVE receber uma nota de 0 a 200 pontos.

**R-020.** A nota global da redação DEVE ser a soma das 5 competências, resultando em um valor de 0 a 1000 pontos.

**R-021.** Se o modelo de IA retornar uma nota fora do intervalo permitido, o sistema DEVE ajustar para o limite mais próximo: mínimo 0, máximo 200 por competência e máximo 1000 no total.

### 2.2 Tratamento de marcações OCR na avaliação

**R-022.** Texto marcado como [RASURA] DEVE ser completamente ignorado na avaliação. Representa texto que o aluno intencionalmente riscou.

**R-023.** Texto marcado como [palavra?] DEVE ser avaliado com cautela. Não penalizar erros que possam ser causados pela transcrição, focando no conteúdo claramente escrito.

### 2.3 Qualidade da resposta

**R-024.** Se a resposta do modelo de IA contiver campos vazios, placeholders ("<<<") ou texto "não fornecido", o sistema DEVE fazer uma segunda tentativa com prompt reforçado.

**R-025.** Se a segunda tentativa também retornar campos incompletos, o sistema DEVE usar textos de fallback padrão em vez de deixar campos vazios.

**R-026.** O modelo de IA DEVE ser chamado com temperatura 0.0 (modo determinístico) para garantir consistência entre avaliações.

---

## 3. Regras de Acesso e Autorização

### 3.1 Autenticação

**R-027.** Todo usuário DEVE ter um perfil válido com um dos seguintes papéis: aluno (student), professor (teacher), gestor (manager), ou administrador (admin).

**R-028.** Se o campo "projetos permitidos" (allowed_projects) estiver preenchido no perfil do usuário, ele DEVE conter "redactia" para que o usuário acesse o sistema. Se o campo estiver vazio ou nulo, o acesso é permitido por padrão.

**R-029.** Se o filtro de cursos (REDACTIA_ALLOWED_COURSES) estiver configurado no sistema e o usuário tiver um curso associado, o curso DEVE estar na lista permitida. O padrão é permitir apenas o curso "enem".

### 3.2 Acesso a redações

**R-030.** Um usuário PODE acessar uma redação se satisfizer pelo menos uma das seguintes condições:
- É o dono da redação (owner_id)
- É quem submeteu a redação (submitted_by)
- É membro da organização à qual a redação pertence

**R-031.** Alunos PODEM ver apenas suas próprias redações.

**R-032.** Professores, gestores e administradores PODEM ver todas as redações da sua organização.

**R-033.** Administradores do sistema PODEM acessar redações de qualquer organização, sem necessidade de ser membro.

### 3.3 Edição de feedback

**R-034.** Apenas professores, gestores e administradores PODEM editar o feedback de uma avaliação.

**R-035.** Na primeira edição de um feedback, o sistema DEVE salvar uma cópia de segurança da avaliação original gerada pela IA.

**R-036.** Ao editar notas das competências, o sistema DEVE automaticamente recalcular a nota global como a soma das 5 competências.

**R-037.** O feedback DEVE ser marcado como "editado por humano" (was_edited = true) após qualquer alteração.

---

## 4. Regras de Status e Ciclo de Vida

**R-038.** Uma redação DEVE seguir este ciclo de vida, sem pular etapas:

```
Rascunho -> Submetida -> [Aguardando Revisão OU Processando] -> Concluída OU Falha
```

**R-039.** As transições permitidas são:

| De | Para | Quando |
|----|------|--------|
| Rascunho (draft) | Submetida (submitted) | Aluno envia a redação |
| Submetida | Aguardando Revisão (pending_review) | OCR requer revisão humana |
| Submetida | Processando (processing) | OCR aprova para correção automática |
| Aguardando Revisão | Processando | Professor aprova o texto do OCR |
| Processando | Concluída (completed) | IA conclui avaliação com sucesso |
| Processando | Falha (failed) | IA encontra erro na avaliação |

**R-040.** O envio de feedback por email SOMENTE é permitido quando a redação está no status "Concluída".

---

## 5. Regras de Analytics e Reforço

### 5.1 Classificação de desempenho

**R-041.** A nota de cada competência DEVE ser classificada em um dos seguintes níveis:

| Faixa | Nível | Significado |
|-------|-------|-------------|
| 180 a 200 | Excelente | Domínio pleno da competência |
| 140 a 179 | Bom | Domínio adequado com poucos desvios |
| 100 a 139 | Regular | Domínio mediano, necessita aprimoramento |
| 60 a 99 | Abaixo | Domínio insuficiente, necessita atenção |
| 0 a 59 | Critico | Domínio precário, necessita intervenção urgente |

### 5.2 Indicadores de reforço

**R-042.** Um aluno DEVE ser marcado como "necessita reforço" em uma competência quando sua nota média nessa competência for inferior a 100 pontos.

**R-043.** Uma competência DEVE ser classificada como "crítica" para uma turma quando mais de 30% dos alunos necessitam de reforço nessa competência.

**R-044.** Uma competência DEVE ser classificada como "alerta" para uma turma quando entre 15% e 30% dos alunos necessitam de reforço.

**R-045.** Um aluno DEVE ser marcado como "em risco" quando necessitar de reforço em 3 ou mais competências simultaneamente.

---

## 6. Regras de Auditoria

**R-046.** O sistema DEVE registrar em log de auditoria toda ação relevante, incluindo: submissão de redação, edição de feedback, envio de feedback, troca de organização.

**R-047.** O log de auditoria é somente-leitura (append-only). Nenhum registro PODE ser alterado ou excluído via interface.

**R-048.** Apenas administradores PODEM visualizar os logs de auditoria.

**R-049.** Registros de auditoria DEVEM ser retidos por 90 dias. Após esse período, PODEM ser removidos automaticamente.

**R-050.** Falhas ao gravar log de auditoria NÃO DEVEM impedir a operação principal. O registro de auditoria opera em modo "fire-and-forget".

---

## 7. Regras de Multi-Tenancy

**R-051.** Toda operação que envolva listagem de redações, alunos, turmas ou analytics DEVE receber o identificador da organização como parâmetro obrigatório.

**R-052.** Professores e gestores PODEM visualizar dados apenas da sua própria organização.

**R-053.** Administradores do sistema PODEM visualizar dados de qualquer organização sem necessidade de ser membro.

**R-054.** A associação entre alunos e turmas é de muitos-para-muitos. Um aluno PODE pertencer a mais de uma turma.

**R-055.** O limite máximo de registros por consulta é 200. O padrão é 50.

---

## 8. Regras de Armazenamento

**R-056.** Arquivos de redação (PDF/imagem) DEVEM ser armazenados no Google Cloud Storage com o caminho: `redactia-essays/{user_id}/{essay_id}/{uuid}{extensão}`.

**R-057.** URLs assinadas para download de arquivos DEVEM ter validade de 7 dias.

**R-058.** O tipo de arquivo DEVE ser detectado automaticamente pelos bytes iniciais (magic bytes), não pela extensão.

---

## Rastreabilidade

Cada regra neste catálogo possui rastreabilidade completa para o código-fonte no arquivo de extração correspondente:
- `outputs/domain-decoder/forefy-prep-ahead/extraction/redactia-extraction.md`
- `outputs/domain-decoder/forefy-prep-ahead/decision-models/redactia-decision-models.md`
- `outputs/domain-decoder/forefy-prep-ahead/dmn/redactia-dmn.md`

---

**Gate de Expressão:** COMPLETO
**Total de regras expressas:** 58 regras em linguagem natural controlada
**Vocabulário controlado:** 13 termos definidos
