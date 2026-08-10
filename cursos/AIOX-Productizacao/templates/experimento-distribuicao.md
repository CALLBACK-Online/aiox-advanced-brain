---
type: template
course: aiox-productizacao
template: experimento-distribuicao
status: canonical
canonical_scope: cursos/AIOX-Productizacao
---

# Template — Experimento de distribuição

```yaml
hipótese:
  público: ""
  dor: ""
  mensagem: ""
  canal: ""
  ação_esperada: ""

janela:
  início: ""
  fim: "" # máximo 14 dias

execução:
  volume_de_contatos: 0
  cadência: ""
  responsável: ""
  tempo_reservado: ""

métricas:
  alcance: 0
  respostas: 0
  conversas: 0
  demos: 0
  pilotos: 0
  pagamentos: 0

decisão:
  kill_threshold: ""
  sinal_para_iterar: ""
  sinal_para_escalar: ""
  o_que_não_construir_durante_o_teste: ""
```

## Portão

- Um canal, um público e uma mensagem.
- Prazo máximo de 14 dias.
- Volume e cadência definidos.
- Kill threshold antes da execução.
- Nenhuma feature nova necessária para começar.

[Aula correspondente](../aulas/03-distribuicao-vs-produto.md) · [Templates](README.md)
