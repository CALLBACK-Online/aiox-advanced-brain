#!/usr/bin/env python3
"""
Domain Decoder — Phase Runner
Version: 1.0.0

Executes the 6-phase business rules extraction pipeline with:
- Phase definitions with handlers, timeouts, criticality
- Cache-aware execution (skip phases with existing output)
- Resume from any phase via PipelineStateManager
- Enforcement rules E1-E10 integrated into phase gates
- Agent-per-phase assignment

Dependencies:
- pipeline_state.py (required for state persistence)
- progress.py (optional for progress display)
"""

__version__ = "1.0.0"

import asyncio
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Coroutine, Dict, List, Optional

try:
    from .pipeline_state import PHASE_AGENTS, PHASE_DEFINITIONS, PHASE_OUTPUT_DIRS
except ImportError:
    from pipeline_state import PHASE_AGENTS, PHASE_DEFINITIONS, PHASE_OUTPUT_DIRS


# =============================================================================
# Phase Definition
# =============================================================================

@dataclass
class PhaseDefinition:
    """
    Definition of a pipeline phase.

    Attributes:
        num: Phase number (0-indexed, sequential)
        name: Human-readable name (used in logs and state)
        handler: Async function that executes the phase
        agent: Agent responsible for this phase
        timeout_seconds: Max execution time
        critical: If True, failure stops the entire pipeline
        cache_check: Optional function that returns True if output already exists
        description: Description for documentation
        output_dir: Subdirectory name under outputs/decoded/{slug}/
    """
    num: int
    name: str
    handler: Callable[..., Coroutine[Any, Any, "PhaseResult"]]
    agent: str = ""
    timeout_seconds: int = 600
    critical: bool = True
    cache_check: Optional[Callable[..., bool]] = None
    description: str = ""
    output_dir: str = ""


@dataclass
class PhaseResult:
    """
    Result of a phase execution.
    Every phase handler MUST return this.
    """
    success: bool
    output: str = ""
    output_file: Optional[str] = None
    output_dir: Optional[str] = None
    tokens_in: int = 0
    tokens_out: int = 0
    cost_usd: float = 0.0
    error: Optional[str] = None
    rules_extracted: int = 0
    contexts_covered: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PipelineResult:
    """Result of the entire pipeline execution."""
    success: bool
    item_id: str
    completed_phases: int
    total_phases: int
    failed_phase: Optional[int] = None
    failed_phase_name: Optional[str] = None
    total_tokens_in: int = 0
    total_tokens_out: int = 0
    total_cost_usd: float = 0.0
    total_rules_extracted: int = 0
    bounded_contexts: List[str] = field(default_factory=list)
    duration_seconds: float = 0.0
    error: Optional[str] = None
    skipped_phases: List[int] = field(default_factory=list)
    cached_phases: List[int] = field(default_factory=list)


# =============================================================================
# Phase Runner
# =============================================================================

class PhaseRunner:
    """
    Executes domain decoder phases in sequence with state persistence,
    progress tracking, enforcement rule gates, and error handling.

    Usage:
        runner = PhaseRunner(
            phases=get_phase_definitions(),
            state_manager=state_mgr,
            progress_tracker=tracker,
        )
        result = await runner.run(item_id, metadata)
    """

    def __init__(
        self,
        phases: List[PhaseDefinition],
        state_manager=None,
        progress_tracker=None,
        verbose: bool = True,
        force: bool = False,
    ):
        self.phases = sorted(phases, key=lambda p: p.num)
        self.state = state_manager
        self.progress = progress_tracker
        self.verbose = verbose
        self.force = force

    def _log(self, message: str) -> None:
        if self.verbose:
            print(message, flush=True)

    async def run(
        self,
        item_id: str,
        metadata: Optional[Dict[str, Any]] = None,
        start_phase: Optional[int] = None,
        output_base: Optional[Path] = None,
        **handler_kwargs,
    ) -> PipelineResult:
        """
        Execute the pipeline for a single system.

        Args:
            item_id: Slug identifier (e.g., "forefy_prep_ahead")
            metadata: system_name, source_location, primary_domain, etc.
            start_phase: Override resume logic, start from this phase
            output_base: Base path for outputs (outputs/decoded/{slug}/)
            **handler_kwargs: Extra kwargs passed to every phase handler
        """
        start_time = time.time()
        metadata = metadata or {}
        completed = 0
        skipped = []
        cached = []
        all_contexts: List[str] = []
        total_rules = 0

        # Determine start phase
        if start_phase is not None:
            resume_from = start_phase
        elif self.state and self.state.load_state():
            resume_from = self.state.get_resume_phase()
            self._log(f"[RESUME] {item_id}: Resuming from phase {resume_from} ({PHASE_DEFINITIONS.get(resume_from, '?')})")
        else:
            resume_from = 0
            if self.state:
                self.state.create_state(metadata)

        self._log(f"[START] {item_id}: {len(self.phases)} phases, starting at phase {resume_from}")

        # Collect previous outputs for feeding to handlers
        previous_outputs: Dict[int, str] = {}
        if self.state and self.state.state:
            previous_outputs = dict(self.state.state.phase_outputs)

        # Execute phases
        for phase_def in self.phases:
            if phase_def.num < resume_from:
                completed += 1
                continue

            # Cache check
            if not self.force and phase_def.cache_check:
                try:
                    if phase_def.cache_check(item_id):
                        self._log(f"  [CACHE] Phase {phase_def.num} ({phase_def.name}): cached, skipping")
                        cached.append(phase_def.num)
                        completed += 1
                        if self.state:
                            self.state.skip_phase(phase_def.num, "cached")
                        if self.progress:
                            self.progress.start_phase(phase_def.num, phase_def.name)
                            self.progress.complete_phase()
                        continue
                except Exception as e:
                    self._log(f"  [WARN] Cache check failed for phase {phase_def.num}: {e}")

            # Start phase
            agent = phase_def.agent or PHASE_AGENTS.get(phase_def.num, "unknown")
            self._log(f"  [PHASE {phase_def.num}] {phase_def.name} (agent: {agent})...")
            if self.state:
                self.state.start_phase(phase_def.num)
            if self.progress:
                self.progress.start_phase(phase_def.num, phase_def.name)

            # Execute handler with timeout
            try:
                result = await asyncio.wait_for(
                    phase_def.handler(
                        item_id=item_id,
                        metadata=metadata,
                        previous_outputs=previous_outputs,
                        output_base=output_base,
                        **handler_kwargs,
                    ),
                    timeout=phase_def.timeout_seconds,
                )
            except asyncio.TimeoutError:
                error_msg = f"Phase {phase_def.num} ({phase_def.name}) timed out after {phase_def.timeout_seconds}s"
                self._log(f"  [TIMEOUT] {error_msg}")
                result = PhaseResult(success=False, error=error_msg)
            except Exception as e:
                error_msg = f"Phase {phase_def.num} ({phase_def.name}) error: {e}"
                self._log(f"  [ERROR] {error_msg}")
                result = PhaseResult(success=False, error=str(e))

            # Handle result
            if result.success:
                self._log(f"  [OK] Phase {phase_def.num} ({phase_def.name}) complete")
                if result.rules_extracted:
                    self._log(f"       Rules extracted: {result.rules_extracted}")
                if result.contexts_covered:
                    self._log(f"       Contexts: {', '.join(result.contexts_covered)}")

                completed += 1
                total_rules += result.rules_extracted
                all_contexts.extend(c for c in result.contexts_covered if c not in all_contexts)
                previous_outputs[phase_def.num] = result.output

                if self.state:
                    self.state.complete_phase(
                        phase=phase_def.num,
                        output_content=result.output,
                        tokens_in=result.tokens_in,
                        tokens_out=result.tokens_out,
                        cost_usd=result.cost_usd,
                        output_file=result.output_file,
                        output_dir=result.output_dir,
                        rules_extracted=result.rules_extracted,
                        contexts_covered=result.contexts_covered,
                    )
                if self.progress:
                    self.progress.complete_phase(
                        tokens_in=result.tokens_in,
                        tokens_out=result.tokens_out,
                        cost_usd=result.cost_usd,
                    )

                # Enforcement rule E2: Verify output saved before advancing
                if output_base and phase_def.num < 5:
                    phase_out_dir = output_base / PHASE_OUTPUT_DIRS.get(phase_def.num, f"phase-{phase_def.num}")
                    if not phase_out_dir.exists() or not any(phase_out_dir.iterdir()):
                        self._log(f"  [E2 WARN] Output dir empty: {phase_out_dir}")
            else:
                # Phase failed
                if self.state:
                    self.state.fail_phase(phase_def.num, result.error or "Unknown error")

                if phase_def.critical:
                    self._log(f"  [FATAL] Critical phase {phase_def.num} ({phase_def.name}) failed")
                    if self.progress:
                        self.progress.complete_phase(success=False)

                    return PipelineResult(
                        success=False,
                        item_id=item_id,
                        completed_phases=completed,
                        total_phases=len(self.phases),
                        failed_phase=phase_def.num,
                        failed_phase_name=phase_def.name,
                        total_rules_extracted=total_rules,
                        bounded_contexts=all_contexts,
                        error=result.error,
                        duration_seconds=time.time() - start_time,
                        skipped_phases=skipped,
                        cached_phases=cached,
                    )
                else:
                    self._log(f"  [WARN] Non-critical phase {phase_def.num} ({phase_def.name}) failed — continuing")
                    skipped.append(phase_def.num)
                    if self.progress:
                        self.progress.complete_phase(success=False)

        # Pipeline complete
        if self.state:
            self.state.complete_pipeline()

        duration = time.time() - start_time
        self._log(f"[DONE] {item_id}: {completed}/{len(self.phases)} phases in {duration:.1f}s")
        self._log(f"       Total rules: {total_rules} | Contexts: {len(all_contexts)}")

        total_in = 0
        total_out = 0
        total_cost = 0.0
        if self.state and self.state.state:
            total_in = sum(p.tokens_in for p in self.state.state.phases.values())
            total_out = sum(p.tokens_out for p in self.state.state.phases.values())
            total_cost = self.state.state.total_cost_usd

        return PipelineResult(
            success=True,
            item_id=item_id,
            completed_phases=completed,
            total_phases=len(self.phases),
            total_tokens_in=total_in,
            total_tokens_out=total_out,
            total_cost_usd=total_cost,
            total_rules_extracted=total_rules,
            bounded_contexts=all_contexts,
            duration_seconds=duration,
            skipped_phases=skipped,
            cached_phases=cached,
        )


# =============================================================================
# Phase Handlers — lazy import to avoid circular deps when run as script
# =============================================================================

def _load_handlers():
    """Import handlers lazily to avoid circular imports."""
    try:
        from .handlers.discovery import handle_discovery
        from .handlers.characterization import handle_characterization
        from .handlers.extraction import handle_extraction
        from .handlers.modeling import handle_modeling
        from .handlers.expression import handle_expression
        from .handlers.validation import handle_validation
    except ImportError:
        from handlers.discovery import handle_discovery
        from handlers.characterization import handle_characterization
        from handlers.extraction import handle_extraction
        from handlers.modeling import handle_modeling
        from handlers.expression import handle_expression
        from handlers.validation import handle_validation
    return {
        0: handle_discovery,
        1: handle_characterization,
        2: handle_extraction,
        3: handle_modeling,
        4: handle_expression,
        5: handle_validation,
    }


# =============================================================================
# Phase Definitions Factory
# =============================================================================

def get_phase_definitions(
    output_base: Optional[Path] = None,
) -> List[PhaseDefinition]:
    """
    Return the 6 domain decoder phase definitions with real handlers.
    Handlers are loaded lazily to avoid circular imports.
    """
    handlers = _load_handlers()

    def _cache_check_factory(phase_num: int):
        """Create a cache check function for a given phase."""
        if output_base is None:
            return None

        def check(item_id: str) -> bool:
            phase_dir = PHASE_OUTPUT_DIRS.get(phase_num, f"phase-{phase_num}")
            path = output_base / phase_dir
            if not path.exists():
                return False
            files = list(path.glob("*.md")) + list(path.glob("*.yaml"))
            return len(files) > 0 and all(f.stat().st_size > 500 for f in files)

        return check

    return [
        PhaseDefinition(
            num=0,
            name="discovery",
            handler=handlers[0],
            agent="eric-evans",
            timeout_seconds=900,
            critical=True,
            cache_check=_cache_check_factory(0),
            description="Domain mapping, bounded contexts, ubiquitous language glossary",
            output_dir="discovery",
        ),
        PhaseDefinition(
            num=1,
            name="characterization",
            handler=handlers[1],
            agent="michael-feathers",
            timeout_seconds=900,
            critical=True,
            cache_check=_cache_check_factory(1),
            description="Legacy code characterization, seam mapping, characterization tests",
            output_dir="characterization",
        ),
        PhaseDefinition(
            num=2,
            name="extraction",
            handler=handlers[2],
            agent="ronald-ross",
            timeout_seconds=1200,
            critical=True,
            cache_check=_cache_check_factory(2),
            description="Rule extraction from seams, Ross taxonomy classification, fact model",
            output_dir="extraction",
        ),
        PhaseDefinition(
            num=3,
            name="modeling",
            handler=handlers[3],
            agent="barbara-von-halle",
            timeout_seconds=1200,
            critical=True,
            cache_check=_cache_check_factory(3),
            description="Decision Model, DMN tables, Decision Requirements Diagrams",
            output_dir="modeling",
        ),
        PhaseDefinition(
            num=4,
            name="expression",
            handler=handlers[4],
            agent="graham-witt",
            timeout_seconds=900,
            critical=True,
            cache_check=_cache_check_factory(4),
            description="RuleSpeak expression, ambiguity elimination, glossary cross-reference",
            output_dir="expression",
        ),
        PhaseDefinition(
            num=5,
            name="validation",
            handler=handlers[5],
            agent="decoder-chief",
            timeout_seconds=600,
            critical=True,
            cache_check=None,  # Validation always runs
            description="SBVR validation (45 items), extraction quality (54 items), packaging",
            output_dir="validation",
        ),
    ]


# =============================================================================
# Test
# =============================================================================

if __name__ == "__main__":
    print("=== Domain Decoder Phase Runner ===\n")
    print("  Phase definitions (without handler import):")
    for num, name in PHASE_DEFINITIONS.items():
        agent = PHASE_AGENTS.get(num, "?")
        print(f"  Phase {num}: {name} (agent: {agent})")
    print(f"\n  Total phases: {len(PHASE_DEFINITIONS)}")

    # Test handler import
    try:
        phases = get_phase_definitions()
        print("\n  Handler wiring:")
        for p in phases:
            print(f"  Phase {p.num}: {p.name} -> {p.handler.__module__}.{p.handler.__name__}")
        print("\n=== All handlers wired successfully ===")
    except Exception as e:
        print(f"\n  Handler import failed (expected when running as script): {e}")
        print("  Use 'python -c \"from lib.phase_runner import get_phase_definitions\"' from squad root")
        print("\n=== Phase definitions OK, handlers need package context ===")
