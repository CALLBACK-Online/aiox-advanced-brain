---
type: lesson
course: introducao-arquitetura-sistemas
lesson_id: banco-schema-indice-transacao
lesson_position: 5
module: M2
sequence: M2.2
status: canonical
canonical_scope: cursos/Introducao-a-Arquitetura-de-Sistemas
difficulty: foundation
source_refs: [postgresql-tutorial, postgresql-indexes]
reading_minutes: 5
---

# Banco, schema, índice e transação

## Resultado

Você consegue separar estrutura, integridade, acesso rápido e mudança atômica ao discutir persistência relacional.

## Mapa visual

```text
Banco
└── schema
    ├── tabela reservas
    │   ├── constraints: identidade e regras
    │   └── índices: caminhos de busca
    └── transação: ler horário + criar reserva como uma unidade
```

## Modelo mental

O **banco** guarda dados persistentes e oferece mecanismos de consulta e integridade. O **schema** define forma e restrições: tabelas, colunas, tipos, chaves e relações.

Um **índice** é como o índice remissivo de um livro: acelera perguntas específicas sem ler tudo. Em troca, ocupa espaço e precisa ser atualizado a cada escrita. “Criar índice em tudo” transfere o problema de leitura para escrita e manutenção.

Uma **transação** agrupa operações que precisam ser tratadas como unidade. Se duas pessoas tentam reservar o último horário, verificar disponibilidade e gravar a reserva precisam respeitar uma regra consistente; fazer as etapas sem proteção abre uma corrida.

## Quando usar — e quando não usar

Use schema e constraints para invariantes que devem valer independentemente do cliente. Use transação quando uma falha no meio deixaria estado inválido. Crie índices a partir de consultas e volume observados.

Não use banco como fila improvisada sem compreender concorrência e retry. Não coloque todos os dados em uma coluna genérica para “ganhar flexibilidade” se o sistema depende de relações e validação. E não otimize uma tabela minúscula por ansiedade.

## Caso rápido

Transferir saldo exige debitar uma conta e creditar outra. Se apenas uma mudança persistir, o sistema inventa ou perde dinheiro. Uma transação protege a unidade. Já buscar reservas por `profissional_id + horario` pode justificar índice quando a tabela e a frequência crescem.

Anti-padrão: validar unicidade apenas no backend. Duas requests concorrentes podem passar pela mesma verificação; uma constraint no banco mantém a regra na fonte de verdade.

## Prática

Para uma entidade, escreva:

1. chave primária;
2. três constraints de integridade;
3. duas consultas frequentes;
4. um índice candidato e seu custo;
5. uma operação que precisa de transação.

## Pergunte ao seu agente

```text
Analise este modelo de dados. Separe regras que pertencem ao schema, consultas que podem justificar índice e operações que precisam de transação. Questione volume e padrão de acesso antes de sugerir otimização.
```

## Evidência de conclusão

Modelo em que integridade não depende apenas da interface, cada índice responde a uma consulta e a fronteira transacional é justificável.

Fontes: [PostgreSQL Tutorial](https://www.postgresql.org/docs/current/tutorial.html) e [Indexes](https://www.postgresql.org/docs/current/indexes.html).


## Âncora no acervo

- [Glossário](../Glossario.md)
- [Mapa de termos](../Mapa-de-termos.md)

## Navegação

- Curso: [README](../README.md)
- Módulo: [M2](../modulos/M2-dados-e-estado.md)
- Anterior: [04-estado-entidade-ciclo-de-vida.md](04-estado-entidade-ciclo-de-vida.md)
- Próxima: [06-cache-arquivos-object-storage.md](06-cache-arquivos-object-storage.md)
