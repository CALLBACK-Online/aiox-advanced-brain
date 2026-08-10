# Findability — por que a turma se perde (e o que fazer)

## Sintoma (WhatsApp real)

- "Manda de novo o squad-creator"
- "Qual a última versão do design.zip?"
- "Cadê o guia de economia de tokens?"
- Aluno novo no meio do cohort: scroll infinito, 9 versões do mesmo zip

**Números T1 export:** 9× squad-creator, 8× design, 6× hormozi, dezenas de packs únicos.

## Causa

| Causa | Efeito |
|-------|--------|
| WhatsApp como CDN | Versões empilhadas sem LATEST |
| Nome de arquivo sem data/semver | Impossível ordenar na cabeça |
| Mensagem sem changelog | "É o mesmo de ontem?" |
| Zero índice | Busca = memória de quem estava online |
| Pack ≠ install ritual | Baixou e não valida/upgrade |

## Solução em camadas

### A. Agora (já no curso)
1. **`CATALOG.md`** — índice humano com LATEST
2. **`catalog.yaml`** — para tooling futuro
3. **Aula 75 FAQ** + seção findability
4. Mentores: responder com âncora no catálogo, não reenviar às cegas

### B. Operação do grupo (processo)
Pin no WhatsApp (ou mensagem fixa semanal):
```
📦 Materiais: veja CATALOG.md no curso / Notion / drive canônico
Regra: só LATEST. Histórico no catálogo.
Ao postar pack: nome-data + 1 linha do que mudou.
```

### C. Produto (médio prazo)
- Drive/Notion/Git `cohort-materials/` com pasta `latest/` espelhando catalog
- Bot ou comando `*where squad-creator` lendo `catalog.yaml`
- PRO installer puxa versões pinadas (não depende do grupo)

## Resposta-padrão do mentor

> "Não sobe o grupo — abre o **CATALOG.md** e busca `squad-creator`.
> LATEST está marcado. Se não tiver o arquivo local, pede reenvio **dessa** versão."

## Métrica de sucesso

- Queda de mensagens "manda de novo / qual última versão"
- Onboarding de aluno atrasado < 15 min para achar pack certo
