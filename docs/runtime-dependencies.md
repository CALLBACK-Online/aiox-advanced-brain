# Dependências de runtime

Este repositório preserva os assets encontrados, mas não replica o monorepo inteiro.

O conteúdo pedagógico em `Cursos/AIOX Advanced/` é autocontido: aulas, módulos, quizzes e materiais navegáveis permanecem dentro de `Cursos`, sem links para outras áreas do vault `mentelendaria`.

Alguns pacotes esperam componentes externos do runtime AIOX/SINKRA, incluindo:

- `.aiox-core/` e seus agentes, schemas e scripts;
- `workspace/` e contratos por negócio;
- `apps/`, `packages/` ou `services/` do produto em execução;
- stories e documentos sob `docs/`;
- ferramentas instaladas no host, como Node.js, Python, Git, Playwright ou CLIs de terceiros;
- variáveis locais que devem permanecer em `.env` e nunca são distribuídas aqui.

Portanto, há dois modos de uso:

1. **Curso e estudo:** compartilhar `Cursos/` com os alunos e ler anatomia, agentes, tasks, workflows, templates e checklists diretamente neste repositório.
2. **Execução:** instalar o asset em um projeto AIOX/SINKRA compatível e resolver as dependências declaradas pelo pacote.

Uma futura etapa de empacotamento pode transformar cada asset em unidade realmente portátil. Isso exige auditoria individual de referências e não deve ser inferido apenas porque a pasta foi copiada.
