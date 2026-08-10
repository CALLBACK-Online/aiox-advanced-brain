<!-- AIOX_TASK_METADATA:START -->
```yaml
framework_task_metadata:
  task_id: an-design-clone-contexts
  task_name: Design Clone -- Contexts
  status: pending
  responsible_executor: '@oalanicolas'
  execution_type: Agent
  estimated_time: 10m
  domain: Operational
  action_items:
    - Identify Usage Contexts
    - Map User Profiles
    - Define Transformational Scope
  acceptance_criteria:
    - contextos de uso são explícitos
    - perfis de usuário ficam definidos
    - escopo transformador é documentado
  output_persistence: transient_output
  accountable_id: Human:Squad_Operator
  accountability_scope: review_only
  escalation_priority: medium
```
<!-- AIOX_TASK_METADATA:END -->

<!-- AIOX_CONTRACT:START -->
```yaml
aiox_contract:
  Domain: Tactical
  atomic_layer: Atom
  executor: Agent
  pre_condition: "mind alvo e intenção do clone já existem."
  post_condition: "context map pronto para decidir arquitetura."
  performance: "bloquear design se contexto de uso continuar implícito."
```
<!-- AIOX_CONTRACT:END -->

# Task: Design Clone -- Contexts

## Output Contract

```yaml
output:
  context_map:
    contexts: []
    user_profiles: []
    transformational_scope: ""
```
