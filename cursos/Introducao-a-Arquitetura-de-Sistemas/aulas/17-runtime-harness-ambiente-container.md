---
type: lesson
course: introducao-arquitetura-sistemas
lesson_id: runtime-harness-ambiente-container
lesson_position: 17
module: M6
sequence: M6.2
status: canonical
canonical_scope: cursos/Introducao-a-Arquitetura-de-Sistemas
difficulty: foundation
adapted_from: cursos/AIOX Advanced/lessons/67-harness-ambiente-execucao.md
source_refs: [docker-container, anthropic-trustworthy-agents]
---

# Runtime, harness, ambiente e container

## Resultado

Você explica por que o mesmo código ou agente se comporta diferente conforme runtime, configuração, permissões e dependências.

## Mapa visual

```text
Artefato executável
  + Runtime (motor que executa)
  + Ambiente (config, rede, dados, versão)
  + Harness (instruções, tools, permissões, gates)
  + Container opcional (processo + arquivos isolados)
  = comportamento observado
```

## Modelo mental

**Runtime** é o mecanismo concreto que carrega e executa: Node, Python, navegador, runner de CI ou runtime de agentes.

**Ambiente** inclui configurações, serviços acessíveis, identidade, rede e dados. Desenvolvimento, staging e produção podem executar o mesmo artefato com riscos diferentes.

**Harness** envolve a execução com instruções, ferramentas, permissões, limites, callbacks e evidência. Em agentes, ele é tão importante quanto o modelo.

**Container** é um processo isolado com arquivos e dependências empacotados. A imagem melhora reprodutibilidade; não inclui automaticamente dados persistentes, segurança ou observabilidade.

## Quando usar — e quando não usar

Descreva runtime e ambiente ao reproduzir bug. Use container quando consistência e isolamento compensarem. Em agentes, declare tools, diretórios, permissões e confirmações externas.

Não diga “funciona na minha máquina” como critério. Não coloque secrets na imagem. Não confunda container com máquina virtual nem com deploy completo. E não assuma que uma sintaxe de Claude Code existe no Codex ou em API própria.

## Caso rápido

Uma skill descreve `$comando`, mas o runtime destino não registra skills. O conteúdo ainda pode orientar o agente, porém a ativação muda. Da mesma forma, um script funciona localmente porque existe binário não declarado e falha no CI. O problema é contrato de ambiente.

Anti-padrão: harness com escrita externa irrestrita e nenhum gate humano.

## Prática

Crie uma ficha: artefato, versão do runtime, dependências, variáveis por nome, rede, storage, permissões, tools, timeout e comando de validação. Não copie valores secretos.

## Pergunte ao seu agente

```text
Produza um contrato reproduzível de execução para este artefato. Separe runtime, ambiente, harness e container. Liste dependências e nomes de variáveis sem revelar valores. Marque efeitos que exigem aprovação humana.
```

## Evidência de conclusão

Outra pessoa consegue reproduzir a execução ou apontar exatamente qual dependência está ausente, sem receber credenciais em texto.

Fontes: [Docker — What is a container?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/) e [Anthropic — Trustworthy agents](https://www.anthropic.com/research/trustworthy-agents). Proveniência: [mapeamento](../PROVENIENCIA.md).

[Anterior](16-logs-metricas-traces-health-checks.md) · [Próxima: CI/CD](18-cicd-deploy-rollback.md)
