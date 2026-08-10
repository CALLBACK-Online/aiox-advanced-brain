# Persona Construction · método pra construir avatar primário em L6

A persona narrativa não é ficção. É **destilação fiel de padrões agregados** num personagem único que o pitch consegue endereçar.

## Quando construir persona

**SIM:**
- L3 detectou célula quente (≥50% em uma linha + n absoluto ≥50)
- O uso final é comunicação/venda (não pesquisa descritiva)
- Há campos abertos substantivos com >40 chars (precisa de matéria-prima textual)

**NÃO:**
- Distribuição uniforme entre células (público é fragmentado por design)
- n absoluto <30 (subgrupo pequeno demais — risco de viés)
- Campos abertos vazios ou genéricos (sem matéria-prima pra fala canônica)

**Em caso de dúvida:** prefira **NÃO construir** persona a inventar uma. Persona inventada conecta com ninguém.

---

## Regra-mãe

**Persona = composto estatístico, não pessoa real.** Nome inventado, mas TODA característica baseada em dado agregado.

```
✅ "Rafael Costa, 34, analista de operações, interior de SP"
   ↑ nome inventado, mas:
   - 34 = mediana implícita do segmento (28-42 ocupando o pico)
   - analista de operações = setor "Outro" dominante + perfil "mudar carreira"
   - interior de SP = sem dado geográfico, mas inferência razoável pelo setor

❌ "Maria, 32, gerente de marketing em São Paulo"
   ↑ chutada — sem ancoragem nos dados
```

---

## Anatomia da persona canônica

### 1 · Nome próprio inventado

**Regras:**
- Use nome **regionalmente plausível** dado o setor dominante (não "Rafael" se 80% é Nordeste rural)
- Sem sobrenomes pomposos ("De Almeida Pinto" soa SP4)
- 2-3 sílabas no nome, 2 sílabas no sobrenome (memorabilidade)

**Exemplo de derivação:**
```
Setor dominante: agricultura (interior)
→ Nomes mais comuns: "João", "Antônio", "Carlos", "Maria"
→ Escolha: "Carlos Silva" (genérico, recognoscível)
```

### 2 · Idade

**Fonte de inferência (em ordem):**
1. Campo idade explícito → use a mediana do subgrupo
2. Sem idade explícita → infira do **setor + perfil**:
   - "Mudar de carreira" → 30-40 (pessoas em transição, não jovens iniciantes)
   - "Já tem negócio" → 35-50 (maturidade empreendedora)
   - "Estudante" → 18-25
   - "Aposentado" → 60+
3. Cite a fonte da inferência no documento

**Anti-padrão:** Chutar 28 anos sempre porque "soa young/aspiracional". Idade errada gera dissonância no pitch.

### 3 · Cidade

**Regras:**
- Se houver dado de cidade/estado → use a moda
- Se não houver → **infira do setor**:
  - Agricultura → interior (não capital)
  - Tech/SaaS → capital ou metro
  - Serviço público → capital regional
  - Comércio → interior ou periferia metro
- **NÃO** chute "São Paulo capital" como default. É preguiçoso e estatisticamente improvável (SP capital ≠ Brasil).

### 4 · Ocupação

**Regras:**
- Combine setor + perfil declarado
- Use linguagem **mundana**, não título de LinkedIn
  - ✅ "analista de operações"
  - ❌ "Senior Operations Analyst"
- Se o setor é "Outro" + perfil "mudar carreira" → "analista (transitando)" ou "atendente buscando mudar"

### 5 · Status emocional

**Fonte:** Análise temática de L4 + tom das respostas abertas.

**Tipologias comuns:**
- **Exausto** — vocabulário: "estou cansado", "não aguento mais", "preciso disso"
- **Esperançoso** — vocabulário: "vai mudar minha vida", "essa é minha chance"
- **Desconfiado** — vocabulário: "tá tudo tão fácil que parece mentira", "muito hype"
- **Impaciente** — vocabulário: "queria já", "preciso urgente", "agora"
- **Ansioso** — vocabulário: "será que vou conseguir", "tenho medo de"
- **Determinado** — vocabulário: "vou fazer", "já comecei", "tô estudando"

**Regra:** Cite a citação canônica que sustenta o status emocional.

### 6 · Fala canônica (a parte mais importante)

A fala canônica é **2-4 frases que sintetizam o que o avatar diria**. Quando o pitch funciona, o avatar deve sentir "essa pessoa me viu".

**Método de destilação:**

1. **Pegue 5-8 respostas abertas reais** do subgrupo (avatar primário)
2. Identifique padrões: que palavras se repetem? que estrutura emocional?
3. Crie uma fala que **mistura essas 5-8 respostas** preservando:
   - Vocabulário literal (não substitua por sinônimos sofisticados)
   - Tom (se eles escrevem em PT-BR informal, escreva em PT-BR informal)
   - Estrutura emocional (vai-e-volta entre esperança e medo, por exemplo)

**Exemplo:**

Respostas reais (mascaradas):
- "saí da CLT mês passado e tô tentando me virar com IA, mas não sei nem por onde começar a vender"
- "ja sei usar Claude Code mas falta o lado comercial sabe, não sei como prospectar"
- "quero parar de depender de patrão mas ainda não consigo previsibilidade"
- "tenho medo de não dar certo e ter que voltar pra carteira"

**Destilação:**
```yaml
fala_canonica: |
  "Saí da CLT pra trabalhar com IA, mas o lado comercial tá travando.
  Sei construir, ainda não sei vender. Quero previsibilidade,
  mas tenho medo de não conseguir e ter que voltar."
```

**Anti-padrões:**
- ❌ Inventar uma fala bonita ("Acredito que a IA vai transformar a sociedade")
- ❌ Traduzir pra "PT-BR formal" se as respostas eram informais
- ❌ Adicionar urgência fake ("Eu PRECISO disso AGORA!!")
- ❌ Misturar com fala de outros segmentos

### 7 · O que quer (ambições)

3-5 ambições ranqueadas, vindas das respostas abertas:

```yaml
o_que_quer:
  - "Primeiro cliente em 30 dias"
  - "Sair da CLT com previsibilidade"
  - "Saber o que vender e por quanto cobrar"
  - "Trabalhar de qualquer lugar"
```

**Regra:** Use vocabulário literal das respostas. Não "transformação", "evolução" se eles não usaram.

### 8 · O que trava (barreiras)

3-5 barreiras concretas:

```yaml
o_que_trava:
  - "Não sabe quem é o cliente ideal"
  - "Não sabe quanto cobrar"
  - "Tem medo de não dar certo e ter que voltar"
  - "Ainda usa só ChatGPT, não tem ferramenta avançada"
```

**Anti-padrão:** Listar "falta de conhecimento" como barreira. Muito genérico. Especifique **qual conhecimento concretamente**.

### 9 · Comportamento de compra

```yaml
comportamento_compra:
  preco_aceitavel: "{faixa baseada em campo financeiro ou setor}"
  objecao_principal: "{texto literal das respostas}"
  gatilho_principal: "{o que move ele a comprar}"
  ciclo_de_decisao: "{rápido | médio | longo}"
  canal_de_descoberta: "{Instagram | indicação | YouTube | etc, da UTM ou inferência}"
```

---

## 4 dores ranqueadas

**Estrutura:**
```yaml
dores_ranqueadas:
  - id: D1
    nome: "{nome curto da dor}"
    intensidade: critica | alta | media | baixa
    pct: "{% das respostas que mencionam}"
    citacao: "{citação literal canônica}"
```

**Regras:**
1. **4 dores, não mais.** Mais que isso dilui foco do pitch.
2. **Ranking por intensidade observada**, não por importância teórica.
3. Cada dor com **citação literal canônica** que melhor representa.
4. Dor #1 = a dor que abre o pitch.

---

## Jornada emocional (4-6 estágios)

**Quando incluir:**
- Contexto é venda ao vivo (masterclass, lançamento)
- Há matéria-prima suficiente nas respostas pra mapear estágios emocionais
- A jornada **diferencia** o pitch (não é "trivial → curioso → comprador")

**Estrutura típica de 5 estágios:**
```yaml
jornada_emocional:
  - estagio: 1
    nome: "Sufocamento"
    emocao_dominante: "exaustão"
    descricao: "Avatar percebe que o emprego/situação atual não sustenta mais o que quer"
  - estagio: 2
    nome: "Descoberta caótica"
    emocao_dominante: "esperança + confusão"
    descricao: "Encontra IA como possibilidade, começa a explorar sem método"
  - estagio: 3
    nome: "Frustração"
    emocao_dominante: "frustração + dúvida"
    descricao: "Não consegue traduzir em resultado concreto — momento de inscrição na masterclass"
  - estagio: 4
    nome: "Decisão"
    emocao_dominante: "determinação"
    descricao: "Decide investir em método estruturado"
  - estagio: 5
    nome: "Compromisso"
    emocao_dominante: "foco"
    descricao: "Compra produto, entra na cohort"
```

**Anti-padrões:**
- Inventar estágios genéricos sem evidência ("encantamento", "transformação")
- Forçar 7+ estágios — fica fragmentado
- Pular o estágio crítico (geralmente o estágio do **momento da inscrição** — é o momento de máxima dor + máxima abertura)

---

## Gatilhos × objeções

Estrutura paralela: o que **traz** o avatar pra compra vs o que **trava**.

```yaml
gatilhos_de_compra:
  - "Conexão com a citação canônica (sentir-se visto)"
  - "Resultado concreto de outra pessoa do mesmo perfil"
  - "Método/estrutura (não 'conteúdo')"
  - "Limite de vagas/janela temporal"

objecoes_esperadas:
  - "Será que vai funcionar pra mim que não programo?"
  - "Tenho tempo de fazer com {X}h por semana?"
  - "Não tenho dinheiro pra investir agora"
  - "Tem muito hypezinho — esse é mais um?"
```

**Regra:** Objeções vêm das **respostas abertas + perfis céticos**, não da imaginação.

---

## Validação cruzada (antes de entregar a persona)

- [ ] Nome próprio é **inventado** e plausível pro setor dominante?
- [ ] Idade tem **fonte de inferência** documentada?
- [ ] Cidade não é "São Paulo capital" por default?
- [ ] Ocupação é **mundana**, não título de LinkedIn?
- [ ] Status emocional tem **citação canônica** que sustenta?
- [ ] Fala canônica é **destilação de respostas reais**, não invenção?
- [ ] Cada dor tem **citação literal**, não paráfrase?
- [ ] Jornada emocional **diferencia** o pitch (não é trivial)?
- [ ] Gatilhos e objeções vêm das **respostas abertas**, não da imaginação?
- [ ] Persona está marcada como **"construção interpretativa, não pessoa real"** em nivel_de_confianca?

---

## Erros comuns

1. **Persona muito sexy aspiracionalmente.** "Influenciador digital, 28, viaja o mundo" — não é o avatar real da maioria das pesquisas. Aterre nos dados.

2. **Idade default 28-32.** Mediana real de público adulto Brasil é 35-45. Persona muito jovem distorce pitch.

3. **Cidade "São Paulo capital".** Default preguiçoso. Brasil é interior + metropolitano + Nordeste + capital. Aterre no setor.

4. **Fala canônica em PT formal.** Se respostas são informais ("tô tentando", "queria muito"), a fala precisa preservar o tom. Senão soa de outra pessoa.

5. **Mais de 4 dores.** Pitch perde foco. Mantenha 4 ranqueadas.

6. **Jornada emocional decorativa.** Se não muda o pitch, retira.

7. **Não citar nivel_de_confianca.** Persona é **media_baixa** sempre (construção interpretativa). Sem isso, leitor pode tratar como dado factual.

---

## Versionamento

Quando uma nova amostra chega:
- **Recalcule** subdistribuições demográficas do avatar
- **Mantenha** o nome próprio (Rafael Costa permanece Rafael Costa)
- **Mantenha** a estrutura narrativa (idade pode mudar levemente)
- **Atualize** a fala canônica se nova matéria-prima de respostas refinou o tom
- **Documente** mudanças no changelog do briefing

---

*Survey Intel · persona-construction v1.0*
