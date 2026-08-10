# Copy Intelligence · transformar análise em material acionável

A camada L7 da skill. Só rode quando o uso for comunicação/venda/copy (não pesquisa descritiva).

## Os 5 componentes obrigatórios

### 1 · Glossário de linguagem que vende vs afasta

Estrutura:

```yaml
linguagem_que_vende:
  - termo: "frase literal ou template"
    porque_funciona: "razão psicológica baseada em insight da análise"
    tag: "#dor_X · #aspiracao_Y"  # links pra banco de citações
    contexto_de_uso: "pitch / landing / email / orgânico"

linguagem_que_afasta:
  - termo: "frase a evitar"
    porque_afasta: "qual arquétipo/segmento isso ativa negativamente"
    quando_pode_usar: "[se houver contexto onde funciona] ou 'nunca'"
```

**Como construir:**

1. **Vende** = vem das próprias respostas do avatar primário. Use suas palavras literais quando possível.

2. **Afasta** = vem dos céticos detectados (use citações tag `#ceticismo`) + clichês conhecidos do nicho.

3. **Mínimo:** 6-10 termos de cada lado.

4. **Anti-padrão:** Não escreva linguagem que vende "em geral" — escreva linguagem que vende **pra esse avatar específico**. "Liberdade financeira" vende pra avatar A e afasta avatar B.

### 2 · Banco de citações tageado

Estrutura:

```yaml
banco_citacoes:
  citacoes_ouro:
    # 5-8 com alto impacto narrativo - "ler em voz alta"
    - id: Q01
      texto: "Citação literal"
      tags: ["#dor_vendas", "#avatar_primario"]
      uso_recomendado: "Abertura / fechamento / desarmar cético"
  
  por_tag:
    "#dor_X":
      - "citação literal 1"
      - "citação literal 2"
      # 5-8 por tag
    "#aspiracao_Y":
      - "..."
    "#objecao_Z":
      - "..."
    "#linguagem_tecnica":
      - "..."
    # mínimo 6 tags, 5-8 citações cada
```

**Como construir:**

1. Citações **literais** das respostas abertas. Pode normalizar pontuação leve, não conteúdo.

2. Tags devem ser **semânticas, não categoriais.** Bom: `#dor_vendas`, `#exaustao`, `#liberdade_carreira`. Ruim: `#perfil_2`, `#problema_3`.

3. Citações ouro são as **5-8 melhores** — selecionadas por:
   - Especificidade (não genérica)
   - Emocionalidade (não data point)
   - Reconhecibilidade (gera "ele me vê" coletivo)
   - Brevidade (cabe em slide / Reels / WhatsApp)

4. **Algumas citações reaparecem em múltiplas tags.** OK. Reporte isso.

### 3 · Frase de abertura otimizada

**Fórmula provada:**

```
"Tem [N específico do avatar primário] pessoas aqui hoje que [característica X] —
e a maior dificuldade não é [skill aparente que ele acha que precisa].
É [skill real que falta, identificada na análise].
Você sabe [o que ele JÁ é bom em],
mas não sabe [o que falta concretamente].
Eu vou falar pra vocês primeiro.
Os outros [N restante] também vão aprender,
mas hoje a porta de entrada é a sua."
```

**Por que funciona (deconstrução):**

| Componente | Função psicológica |
|------------|-------------------|
| "Tem N pessoas" | Autoridade quantitativa + sensação de coletivo |
| "Que [característica]" | Reconhecimento (ele se identifica) |
| "Não é [aparente], é [real]" | Reframing — desinstala expectativa errada |
| "Você sabe X, não sabe Y" | Validação + dor nomeada |
| "Vou falar pra vocês primeiro" | Prioridade — diminui resistência |
| "Os outros também" | Inclusão dos demais sem perder foco |

**Variações por contexto:**

- **Masterclass de venda:** usar literal
- **Landing de produto:** transformar em headline + sub-headline
- **Vídeo curto:** apenas as 3 primeiras frases (hook + reframing)
- **Email pré-evento:** subject = "N pessoas estão na mesma situação que você"

### 4 · Anti-padrões explícitos

Lista do que **não** falar/escrever. Categorias:

```yaml
anti_padroes:
  evite_no_pitch:
    # 5-8 itens específicos do avatar
  
  evite_na_landing:
    # 4-6 itens visuais + textuais
  
  evite_no_email:
    # 3-5 itens de cadência/tom
  
  evite_no_organico:
    # 3-5 itens de redes sociais
```

**Critério:** Cada anti-padrão precisa de razão baseada na análise. Não escreva "evite ser genérico" — escreva "evite '100k/mês' como promessa direta porque ativa A04 (cético com radar de hype) detectado em 17 respostas".

### 5 · Prompts-template pra geração subsequente

Template canônico:

```markdown
PROMPT_TEMPLATE: {nome_do_caso_de_uso}

Considerando o briefing {NOME_DA_PESQUISA} anexo, gere {ENTREGÁVEL} 
seguindo essas regras:

AVATAR DE REFERÊNCIA: {AV_PRIMARIO | AV_X | AV_Y}

CONSTRAINTS:
- Use linguagem da seção {N} (que vende)
- Evite TODA linguagem da seção {N+1} (que afasta)
- Cada item endereça uma dor específica da seção {N+2}
- Tom: {especificar tom — direto, conversacional, técnico, etc}
- Comprimento: {especificar limite}

OUTPUT:
{especificar formato esperado}
```

**Prompts canônicos a sempre incluir:**

1. `gerar_copy_whatsapp_pos_evento` (sequência de 3-4 mensagens)
2. `gerar_headline_landing` (5 variações)
3. `gerar_sequencia_email_pre_evento` (5 emails D-7 a D-0)
4. `gerar_carrossel_instagram` (10 slides)
5. `gerar_script_video_curto` (Reels/Shorts)
6. `analisar_lead_individual` (classificação automática quando lead chega)

**Adapte conforme o uso real do usuário.** Não force prompts irrelevantes.

## Validação cruzada

Antes de entregar, valide:

- [ ] Linguagem que vende usa palavras das próprias respostas do avatar?
- [ ] Linguagem que afasta inclui clichês do nicho + termos rejeitados pelos céticos?
- [ ] Citações ouro são 5-8 selecionadas com critério, não as primeiras que encontrou?
- [ ] Tags são semânticas, não categoriais?
- [ ] Frase de abertura tem todos os 6 componentes da fórmula?
- [ ] Anti-padrões têm razão baseada na análise (não genérica)?
- [ ] Prompts-template referenciam seções específicas do briefing?

## Erros comuns

1. **Inventar citações.** Se uma frase é boa demais mas não está literal no dataset, marque como `[inferida - não usar literal]`.

2. **Genéricos.** "Use linguagem direta" não é regra — qual frase específica? Qual frase específica evitar?

3. **Linguagem aspiracional do analista, não do avatar.** Você pode achar "transformação" inspirador. O avatar pode achar genérico. Use o que o avatar escreveu, não o que você acharia bonito.

4. **Esquecer de versionar.** Quando uma segunda amostra chegar e a análise atualizar, a linguagem que vende pode mudar. Versione: `v1.0`, `v1.1`, `v2.0`.
