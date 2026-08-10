# Tool Integration Plan - Domain Decoder Squad

## Objective
Extrair modelo de negocio de codigo legado com rastreabilidade completa e abordagem internal-first.

## Wave 1 (Immediate)
1. Reusar workflow canonical de extração:
   - `squads/code-anatomist/workflows/wf-extract-rules.yaml`
2. Padronizar pipeline base:
   - mapeamento de contexto (`map-domain`)
   - classificação de regras (`classify-rules`)
   - caracterização legado (`characterize-legacy`)
   - modelagem de decisão (`model-decisions`)
   - expressão de regras (`express-rules`)
3. Integrar scripts internos de apoio:
   - `.aiox-core/infrastructure/scripts/codebase-mapper.js`
   - `.aiox-core/infrastructure/scripts/pattern-extractor.js`
   - `.aiox-core/infrastructure/scripts/dependency-analyzer.js`
   - `.aiox-core/infrastructure/scripts/framework-analyzer.js`
4. Adicionar `ast-grep` para structural search nos hotspots de regras.
5. Executar scanner AST interno para baseline determinístico:
   - `npm run ast:scan:code-anatomist`
   - output: `.aiox/ast/code-anatomist-structural-model.json`

## Wave 2 (Short-Term)
1. Adicionar `Semgrep` para detecção de padrões de regras de negócio.
2. Consolidar matriz de rastreabilidade:
   - contexto
   - regra
   - decisão
   - arquivo
   - linha
3. Definir scorecard de qualidade de extração (completude, ambiguidade, rastreabilidade).

## Wave 3 (Medium-Term)
1. Adicionar `Joern` para cenários de alto acoplamento e fluxos complexos.
2. Criar consultas específicas em `tree-sitter` para linguagens-alvo mais frequentes.
3. Formalizar export padrão para catálogo de regras e artefatos de decisão.

## Capability Wiring
- `bounded-context-mapping`:
  - primary: `map-domain` + `codebase-mapper`
  - fallback: leitura manual por módulos
- `rule-taxonomy-classification`:
  - primary: `classify-rules`
  - fallback: classificação manual com checklist
- `legacy-characterization`:
  - primary: `characterize-legacy`
  - fallback: revisão estática + testes existentes
- `decision-modeling`:
  - primary: `model-decisions`
  - fallback: tabelas manuais por decisão
- `rule-expression`:
  - primary: `express-rules`
  - fallback: guideline textual sem padronização completa
- `structural-rule-mining`:
  - primary: `ast-grep` + `Semgrep`
  - fallback: grep/regex

## Success Metrics

### Traceability
- 100% das regras extraídas têm rastreabilidade source -> rule -> decision table -> RuleSpeak.
- 100% das decisões relevantes possuem rule family associada.

### Quality
- SBVR compliance >= 85% (validado contra standard OMG SBVR 1.5).
- Zero ambiguous qualifiers na output final (eliminação completa de termos vagos).
- Redução de ambiguidade lexical nas regras finais.

### Coverage
- Coverage rate against Rule Location Index >= 80%.
- Nenhuma recomendação fora do escopo de extração de modelo de negócio.

## Validation Checklist
- [ ] Internal-first preservado em todas as capacidades cobertas internamente
- [ ] Ferramentas externas mapeadas apenas para gaps reais
- [ ] Matriz de rastreabilidade gerada
- [ ] Decision model consistente (sem órfãos críticos)
- [ ] Artefatos sincronizados com `tool-discovery-report.md`
- [ ] SBVR compliance >= 85%
- [ ] Zero ambiguous qualifiers in final output
- [ ] Coverage rate against Rule Location Index >= 80%
