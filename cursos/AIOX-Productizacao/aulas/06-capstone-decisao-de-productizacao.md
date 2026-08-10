---
type: lesson
course: aiox-productizacao
lesson_id: capstone-decisao-de-productizacao
title: "Capstone: decisão de productização"
lesson_position: 6
module: MC
reading_minutes: 45
status: canonical
canonical_scope: cursos/AIOX-Productizacao
curriculum_role: synthesis
source: synthesis
source_version: 1.0.0
---

# Capstone: decisão de productização

## Resultado

Integrar oferta, distribuição, formato e estágio em uma decisão que possa ser invalidada pelo mercado.

Esta aula não pede uma apresentação bonita. Ela pede coerência entre cinco decisões que normalmente são tomadas separadas: **qual problema recortar, por que alguém pagaria, como chegar até essa pessoa, qual formato entregar agora e qual prova autoriza avançar**. Se uma decisão depende de uma hipótese escondida, o pacote ainda não está pronto.

## Mapa da decisão

```text
capacidade comprovada
  → wedge único
  → dor + mecanismo + prova
  → experimento de distribuição
  → formato atual
  → estágio + próximo gate
```

## Prática

Monte o [Productization Decision Pack](../Projeto-Integrador.md). Para cada afirmação, marque `evidência`, `hipótese` ou `desconhecido`.

Depois responda:

1. Qual conversa pode invalidar o wedge?
2. O que você decidiu não construir?
3. Que prova autoriza o próximo estágio?

## Oficina de integração

### 1. Congele a capacidade observável

Descreva o que já funciona sem mencionar o produto desejado. Use o formato:

```text
Quando {entrada real} acontece, a capacidade produz {saída observável}
em {tempo/custo/qualidade conhecidos}, sob {limitações}.
```

Se você só consegue descrever telas, roadmap ou arquitetura futura, volte à engenharia. Productização começa depois que existe uma capacidade demonstrável.

### 2. Teste a cadeia de coerência

Leia o pacote de baixo para cima:

1. A métrica do experimento realmente mede a hipótese?
2. O canal alcança o cliente descrito no wedge?
3. A mensagem fala da dor e do resultado, não da tecnologia?
4. O formato escolhido reduz a principal incerteza ou cria novas?
5. O estágio declarado corresponde às provas que já existem?

Uma quebra invalida a cadeia. Corrija a decisão anterior em vez de compensar com mais construção.

### 3. Faça o teste do corte

Remova tudo que não seja necessário para entregar o wedge ao primeiro cliente candidato. O que sobrar é o escopo atual. O que sair vira veto explícito, não backlog disfarçado.

Exemplos de veto:

- não criar painel antes de validar a entrega assistida;
- não automatizar onboarding antes de repetir o serviço;
- não abrir um segundo canal antes de medir o primeiro;
- não publicar preço fechado enquanto custo e variância forem desconhecidos;
- não chamar piloto interno de demanda externa.

### 4. Calcule ROI como intervalo

Quando houver baseline, escreva fórmula, fonte e premissas. Quando não houver, transforme o desconhecido em medição. Um intervalo honesto é melhor que um número preciso inventado.

```text
valor potencial = frequência × impacto por ocorrência × período
ROI estimado = (valor potencial - custo total) / custo total
```

O cálculo apoia uma conversa; não prova causalidade nem garante compra.

### 5. Reduza para um experimento

O experimento deve caber em até 14 dias e terminar em uma decisão. Defina:

- hipótese;
- público e canal;
- ação e volume;
- métrica primária;
- limiar para perseverar;
- limiar para ajustar ou matar;
- dono e data;
- veto de construção durante o teste.

“Conversar com clientes” não basta. “Convidar 15 gestores de operações, obter 5 respostas e 2 reuniões sobre o job X até sexta” é executável e auditável.

## Revisão adversarial

Antes de aprovar, tente destruir a tese:

- **Wedge:** ainda comporta três clientes, três dores ou três jobs diferentes?
- **Dor:** existe comportamento observável ou só opinião favorável?
- **ROI:** alguma premissa foi tratada como fato?
- **Distribuição:** há acesso ao canal ou apenas esperança?
- **Formato:** consultoria, app ou SaaS foi escolhido por evidência ou identidade?
- **Estágio:** a prova é interna, de cliente ou de produto?
- **Próximo passo:** o teste pode produzir um “não” útil?

Se o pacote sobreviver sem esconder desconhecidos, ele está pronto para o mercado — não necessariamente pronto para escalar.

## Exemplo compacto

```text
Capacidade: classifica solicitações e prepara uma resposta revisável.
Wedge: reduzir o tempo de triagem de uma equipe específica.
Fato: 40 solicitações observadas; baseline medido em 18 min por item.
Hipótese: o gestor pagaria por reduzir o ciclo pela metade.
Formato atual: serviço assistido, porque exceções ainda exigem julgamento.
Experimento: 10 convites, 3 diagnósticos, 1 piloto pago em 14 dias.
Veto: não construir dashboard, billing ou multi-tenant antes do piloto.
Gate seguinte: repetição em dois clientes com margem e qualidade registradas.
```

Note o que o exemplo não afirma: tamanho de mercado, taxa de conversão futura, preço ideal ou prontidão de SaaS. Esses pontos continuam como hipóteses.

## Decisão final

Feche o Decision Pack com exatamente uma das saídas:

- **perseverar:** a evidência sustenta repetir o mesmo teste;
- **ajustar:** existe sinal, mas wedge, mensagem, canal ou formato precisa mudar;
- **matar:** a hipótese central falhou ou o custo de aprender não se justifica;
- **medir antes:** falta baseline para formular uma hipótese econômica honesta.

Não use “continuar construindo” como quinta saída.

## Evidência de conclusão

- O experimento cabe em 14 dias.
- ROI não contém números inventados.
- Formato e estágio possuem justificativa e veto.
- Cada afirmação relevante está marcada como fato, hipótese ou desconhecido.
- O Decision Pack termina em perseverar, ajustar, matar ou medir antes.
- A [Rubrica](../Rubrica.md) atinge a nota de corte.

## Pergunte ao seu agente

```text
Use AGENT-GUIDE.md e Rubrica.md para revisar meu Productization Decision Pack.
Dê nota por critério, cite a evidência usada, marque hipóteses escondidas e
recuse aprovação se o próximo passo for apenas construir mais. Termine com
um experimento de até 14 dias e um veto explícito.
```

## Navegação

[← Aula anterior](05-estagios-de-monetizacao.md) · [Capstone](../modulos/MC-capstone.md) · [Curso](../README.md) · [Projeto Integrador](../Projeto-Integrador.md)
