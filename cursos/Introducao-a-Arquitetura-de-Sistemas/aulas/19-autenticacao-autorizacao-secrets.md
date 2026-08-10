---
type: lesson
course: introducao-arquitetura-sistemas
lesson_id: autenticacao-autorizacao-secrets
lesson_position: 19
module: M7
sequence: M7.1
status: canonical
canonical_scope: cursos/Introducao-a-Arquitetura-de-Sistemas
difficulty: foundation
source_refs: [supabase-auth, owasp-secrets]
reading_minutes: 5
---

# Autenticação, autorização e secrets

## Resultado

Você separa identidade, permissão e credencial, aplicando menor privilégio no limite que executa a ação.

## Mapa visual

```text
Autenticação: quem é?  → identidade/token verificado
Autorização: pode quê? → ação + recurso + contexto
Secret: como o sistema prova acesso a outro sistema?
```

## Modelo mental

**Autenticação** verifica identidade. **Autorização** decide se aquela identidade pode executar uma ação sobre um recurso. Estar logado não significa poder ler qualquer pedido.

**Secret** é material sensível que concede acesso: API key, credencial, certificado, token. Precisa de armazenamento apropriado, escopo mínimo, rotação, expiração, revogação e auditoria.

O frontend pode apresentar opções, mas o servidor ou banco precisa reforçar autorização. Esconder botão não protege operação.

## Quando usar — e quando não usar

Modele toda ação sensível com sujeito, ação, recurso e condição. Use credenciais separadas por ambiente e serviço, com menor privilégio. Prefira tokens curtos e identidade de workload quando o runtime suporta.

Não commite secret, não envie em chat e não registre em log. Não use uma chave administrativa no cliente. Não confunda autenticação forte com autorização correta. E não crie uma única credencial compartilhada por todos os workers.

## Caso rápido

Usuário autenticado tenta editar projeto de outro tenant. O token prova quem ele é; a autorização precisa verificar associação e papel naquele projeto. Uma service key que ignora políticas só pode existir no backend estritamente controlado.

Anti-padrão: endpoint administrativo protegido apenas porque não aparece no menu.

## Prática

Crie matriz com cinco ações: identidade, papel, recurso, regra e decisão. Depois inventarie secrets apenas por nome: dono, escopo, ambiente, rotação e onde nunca pode aparecer.

## Pergunte ao seu agente

```text
Faça revisão de autenticação, autorização e secrets deste fluxo. Monte matriz sujeito-ação-recurso, procure confiança no frontend, privilégios amplos, credenciais compartilhadas e ausência de rotação. Nunca peça ou imprima valores secretos.
```

## Evidência de conclusão

Matriz de acesso aplicada no backend/banco e inventário de secrets sem valores, com owner, escopo e ciclo de vida.

Fontes: [Supabase Auth](https://supabase.com/docs/guides/auth) e [OWASP — Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html).

[Anterior](18-cicd-deploy-rollback.md) · [Próxima: isolamento](20-multitenancy-isolamento-rls.md)
