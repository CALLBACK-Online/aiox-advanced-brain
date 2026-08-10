# ETL-Ops Squad — Production Examples

Outputs reais de execução do squad `etl-ops` em cenários de produção (transcrição, extração, diarização).

## Samples incluídos

| Arquivo | Tipo de output | Caso de uso |
|---|---|---|
| `sample-etl-run.yaml` | Run metadata YAML | Pipeline ETL completo (Viktor Oddy nano-banana) |
| `sample-etl-index.json` | Index de execução | Batch ETL (Thiago ROAS interviews) |
| `sample-diarized-transcript-excerpt.md` | Trecho de transcript diarized | ETL run 20260311-qj04 (primeiras 100 linhas) |

## Outputs históricos adicionais

72 arquivos de outputs de produção estão arquivados em:

```
../aiox-stage/outputs/etl-ops/
```

Inclui: transcripts com diarização (Whisper + speaker attribution), índices de pipeline, logs stderr, runs completos de batch. Transcripts completos não são copiados para o repo por tamanho (~200KB+ cada).

## Provenance

Outputs gerados antes da migração para SINKRA v3.1+. Mantidos como evidência de uso real do pipeline ETL em transcrição de interviews e extração de conteúdo de vídeo/áudio.
