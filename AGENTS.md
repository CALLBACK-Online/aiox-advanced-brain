# Regras deste repositório

Este repositório é uma biblioteca educacional do curso, das skills e dos squads do AIOX Advanced.

- Preserve `.claude/skills/` como fonte canônica das skills.
- Preserve `squads/` como fonte canônica dos squads.
- Preserve `Cursos/AIOX Advanced/` como unidade compartilhável e autocontida para os alunos.
- Todos os links do curso devem resolver dentro de `Cursos`; não crie dependências documentais do curso para fora dessa pasta.
- Links e dependências documentais devem resolver dentro deste repositório.
- Não adicione `.env`, credenciais, outputs de execução, caches, artefatos temporários ou fontes integrais de livros/transcrições.
- Mudanças importadas do `sinkra-hub` ou do `mentelendaria` devem atualizar `catalog.json` e a documentação de proveniência correspondente.
- Execute `npm run validate` antes de concluir alterações; o comando valida a biblioteca e o curso.
- Não publique nem faça push sem solicitação explícita do usuário.
