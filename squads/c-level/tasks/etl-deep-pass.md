# Task: ETL Deep Pass (Master Orchestrator)

task_id: etl-deep-pass
```yaml
task:
  task_id: etl-deep-pass
  id: etl-deep-pass
  name: ETL Deep Pass (Master Orchestrator)
  agent: coo-orchestrator
  responsavel_type: Agent
  elicit: false
  output_format: yaml
  workflow: etl-deep-pass-pipeline
  accountability_token: TK-CL-008
```
## SINKRA Contract

Domain: Operational
atomic_layer: Molecule
Input:
- workspace/businesses/{slug}/
- squads/c-level/data/imersao-business-map.yaml
Output:
- L4-operational/evidence/etl-run-envelope.yaml
pre_condition:
- Business slug valido e workspace bootstrapped com L0-L4 directories.
post_condition:
- 4 layers executadas sequencialmente com completeness >= 85% (ou >= 75% sem website).
performance:
- Executar layers sequencialmente, registrar metricas por layer no etl-run-envelope.
Error Handling:
- Escalar blockers estruturais imediatamente e interromper a execução quando o input canônico estiver inconsistente.
Completion Criteria:
- [ ] Layer 1 (local extract) completou com source-registry gerado.
- [ ] Layer 4 (generate artifacts) completou com narrative YAMLs gerados.
- [ ] Quality gate checklist executado com resultado registrado.
- [ ] etl-run-envelope.yaml contém métricas das 4 layers.

## Descricao

Master orchestrator que encadeia as 4 layers do ETL Deep Pass: Local Extract, Web Scrape, Web Research e Generate Artifacts. Enriquece o workspace de um business de ~55% para ~95% de completude, executando cada layer sequencialmente com gates de qualidade entre elas.

## Prerequisites

- Bootstrap executado (`workspace/user.md` existe).
- Negocio criado (`workspace/businesses/{slug}/` existe).
- Templates scaffolded (`*scaffold-templates` executado).
- Mapa de fontes configurado em `squads/c-level/data/imersao-business-map.yaml`.

## Usage

```
*etl-deep-pass {slug}
```

## Execution Flow

### Fase 1: Pre-flight

1. Validar que `{slug}` existe em `workspace/businesses/{slug}/`.
2. Ler `squads/c-level/data/imersao-business-map.yaml` e localizar entrada do slug.
3. Ler `workspace/businesses/{slug}/L4-operational/evidence/completeness-manifest.yaml` (se existir).
4. Registrar completude inicial como `baseline_completeness`.
5. **Gate:** Diretorio do business deve existir. Se ausente, HALT com instrucao para executar `*add-business`.

### Fase 2: Layer 1 — Local Extract

1. Executar `*etl-local-extract {slug}`.
2. Capturar outputs criticos: `website_url`, `company_name`.
3. Ler `completeness-manifest.yaml` atualizado.
4. **Gate:** Completude geral >= 70%. Se abaixo, reportar gaps e continuar com warning.

### Fase 3: Layer 2 — Web Scrape

1. Verificar se `website_url` foi extraido na Layer 1.
2. Se `website_url` for `null`: registrar `SKIPPED_NO_URL` no envelope e pular para Layer 3.
3. Se disponivel: executar `*etl-web-scrape {slug}`.
4. **Gate:** Nenhum erro critico. Se scrape falhou, registrar `FAILED` e continuar.

### Fase 4: Layer 3 — Web Research

1. Executar `*etl-web-research {slug}`.
2. Verificar outputs: `credentials.yaml`, `proof.yaml`, `testimonials.yaml`.
3. **Gate:** Ao menos 1 fonte verificada com URL. Se zero fontes, registrar warning.

### Fase 5: Layer 4 — Generate Artifacts

1. Executar `*etl-generate-artifacts {slug}`.
2. Verificar outputs: brandbook, positioning, proof, testimonials, narrative, movement.
3. Ler `completeness-manifest.yaml` final.
4. **Gate:** Completude geral >= 85% (com website) ou >= 75% (sem website).

### Fase 6: Final Report

1. Calcular delta: `final_completeness - baseline_completeness`.
2. Listar arquivos criados e atualizados durante o pipeline.
3. Avaliar squad readiness por squad (copy, design, etl-ops, etc.).
4. Listar campos que ainda requerem preenchimento manual.
5. Atualizar `L4-operational/evidence/etl-run-envelope.yaml` com resultado final do deep pass.
6. Exibir report formatado:
   - Delta de completude (ex: 55% -> 92% = +37pp).
   - Arquivos criados/atualizados.
   - Squad readiness (READY / PARTIAL / NOT_READY por squad).
   - Campos manuais restantes.

## Acceptance Criteria

1. Todas as 4 layers executadas ou puladas com razao documentada no envelope.
2. Completude final >= 85% (com website) ou >= 75% (sem website).
3. `completeness-manifest.yaml` preciso e atualizado com metricas de cada layer.
4. `source-registry.yaml` lista todas as fontes com status e confianca.
5. `etl-run-envelope.yaml` contem registro de cada layer executada.
6. Nenhum dado fabricado — compliance total com zero-invention.
7. Delta de completude reportado com valores exatos.

## Outputs

| Arquivo | Descricao |
|---------|-----------|
| `L4-operational/evidence/completeness-manifest.yaml` | Manifesto final de completude |
| `L4-operational/evidence/source-registry.yaml` | Registro consolidado de fontes |
| `L4-operational/evidence/etl-run-envelope.yaml` | Envelope com metricas de todas as layers |
| Arquivos de cada layer | Conforme outputs das tasks individuais |

---

*Task do Squad C-Level - COO Orchestrator*
