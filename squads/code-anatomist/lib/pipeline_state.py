#!/usr/bin/env python3
"""
Domain Decoder — Pipeline State Manager
Version: 1.0.0

Manages persistent state for the 6-phase business rules extraction pipeline.
Enables resume from any phase after interruption, cost tracking, and audit trail.

Phases:
  0: discovery         — Domain mapping & bounded context identification (eric-evans)
  1: characterization  — Legacy code characterization & safety net (michael-feathers)
  2: extraction        — Rule extraction & classification (ronald-ross)
  3: modeling          — Decision modeling & DMN tables (barbara-von-halle)
  4: expression        — Rule expression in structured natural language (graham-witt)
  5: validation        — Final validation & delivery (decoder-chief)
"""

__version__ = "1.1.0"

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


# =============================================================================
# Status Enums (Gap 1 — parity with books pipeline)
# =============================================================================

class PhaseStatus(str, Enum):
    """Status of a pipeline phase. Prevents typos in status strings."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class PipelineStatus(str, Enum):
    """Overall pipeline status."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


# =============================================================================
# Phase Definitions — Domain Decoder Pipeline
# =============================================================================

PHASE_DEFINITIONS = {
    0: "discovery",
    1: "characterization",
    2: "extraction",
    3: "modeling",
    4: "expression",
    5: "validation",
}

# Agent assignment per phase (for reference and auto-assignment)
PHASE_AGENTS = {
    0: "eric-evans",
    1: "michael-feathers",
    2: "ronald-ross",
    3: "barbara-von-halle",
    4: "graham-witt",
    5: "decoder-chief",
}

# Output directories per phase (enforcement rule E8)
PHASE_OUTPUT_DIRS = {
    0: "discovery",
    1: "characterization",
    2: "extraction",
    3: "modeling",
    4: "expression",
    5: "validation",
}


# =============================================================================
# Core Data Classes
# =============================================================================

@dataclass
class PhaseState:
    """State of a single pipeline phase."""
    phase: int
    name: str
    status: PhaseStatus
    executor: str = ""
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    duration_seconds: Optional[float] = None
    tokens_in: int = 0
    tokens_out: int = 0
    cost_usd: float = 0.0
    output_file: Optional[str] = None
    output_dir: Optional[str] = None
    error: Optional[str] = None
    rules_extracted: int = 0
    contexts_covered: List[str] = field(default_factory=list)
    # Gap 3: Granular validation metrics per phase
    validation_passed: Optional[bool] = None
    validation_metrics: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "phase": self.phase,
            "name": self.name,
            "status": self.status.value if isinstance(self.status, PhaseStatus) else self.status,
            "executor": self.executor,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "duration_seconds": self.duration_seconds,
            "tokens_in": self.tokens_in,
            "tokens_out": self.tokens_out,
            "cost_usd": self.cost_usd,
            "output_file": self.output_file,
            "output_dir": self.output_dir,
            "error": self.error,
            "rules_extracted": self.rules_extracted,
            "contexts_covered": self.contexts_covered,
            "validation_passed": self.validation_passed,
            "validation_metrics": self.validation_metrics,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PhaseState":
        return cls(
            phase=data["phase"],
            name=data["name"],
            status=PhaseStatus(data["status"]),
            executor=data.get("executor", ""),
            started_at=data.get("started_at"),
            completed_at=data.get("completed_at"),
            duration_seconds=data.get("duration_seconds"),
            tokens_in=data.get("tokens_in", 0),
            tokens_out=data.get("tokens_out", 0),
            cost_usd=data.get("cost_usd", 0.0),
            output_file=data.get("output_file"),
            output_dir=data.get("output_dir"),
            error=data.get("error"),
            rules_extracted=data.get("rules_extracted", 0),
            contexts_covered=data.get("contexts_covered", []),
            validation_passed=data.get("validation_passed"),
            validation_metrics=data.get("validation_metrics"),
        )


@dataclass
class PipelineState:
    """Complete pipeline state for a system being decoded."""
    item_id: str
    metadata: Dict[str, Any]
    status: PipelineStatus
    current_phase: int
    started_at: str
    last_updated: str
    phases: Dict[int, PhaseState] = field(default_factory=dict)
    phase_outputs: Dict[int, str] = field(default_factory=dict)
    total_tokens_in: int = 0
    total_tokens_out: int = 0
    total_cost_usd: float = 0.0
    total_rules_extracted: int = 0
    bounded_contexts: List[str] = field(default_factory=list)
    last_error: Optional[str] = None
    error_phase: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "item_id": self.item_id,
            "metadata": self.metadata,
            "status": self.status.value if isinstance(self.status, PipelineStatus) else self.status,
            "current_phase": self.current_phase,
            "started_at": self.started_at,
            "last_updated": self.last_updated,
            "phases": {str(k): v.to_dict() for k, v in self.phases.items()},
            "phase_outputs": {str(k): v for k, v in self.phase_outputs.items()},
            "total_tokens_in": self.total_tokens_in,
            "total_tokens_out": self.total_tokens_out,
            "total_cost_usd": self.total_cost_usd,
            "total_rules_extracted": self.total_rules_extracted,
            "bounded_contexts": self.bounded_contexts,
            "last_error": self.last_error,
            "error_phase": self.error_phase,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PipelineState":
        phases = {int(k): PhaseState.from_dict(v) for k, v in data.get("phases", {}).items()}
        phase_outputs = {int(k): v for k, v in data.get("phase_outputs", {}).items()}
        return cls(
            item_id=data["item_id"],
            metadata=data.get("metadata", {}),
            status=PipelineStatus(data["status"]),
            current_phase=data["current_phase"],
            started_at=data["started_at"],
            last_updated=data["last_updated"],
            phases=phases,
            phase_outputs=phase_outputs,
            total_tokens_in=data.get("total_tokens_in", 0),
            total_tokens_out=data.get("total_tokens_out", 0),
            total_cost_usd=data.get("total_cost_usd", 0.0),
            total_rules_extracted=data.get("total_rules_extracted", 0),
            bounded_contexts=data.get("bounded_contexts", []),
            last_error=data.get("last_error"),
            error_phase=data.get("error_phase"),
        )


# =============================================================================
# State Manager
# =============================================================================

class PipelineStateManager:
    """
    Manages persistent state for domain decoder pipeline execution.
    Enables resume from any phase after interruption.

    State file: outputs/decoded/{slug}/pipeline-state.json
    """

    def __init__(
        self,
        item_id: str,
        state_dir: Path,
        phase_definitions: Optional[Dict[int, str]] = None,
    ):
        self.item_id = item_id
        self.state_dir = state_dir
        self.state_file = state_dir / "pipeline-state.json"
        self.phase_definitions = phase_definitions or PHASE_DEFINITIONS

        state_dir.mkdir(parents=True, exist_ok=True)
        self.state: Optional[PipelineState] = None

    def _timestamp(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def load_state(self) -> Optional[PipelineState]:
        """Load existing state from disk."""
        if self.state_file.exists():
            try:
                data = json.loads(self.state_file.read_text(encoding="utf-8"))
                self.state = PipelineState.from_dict(data)
                return self.state
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Warning: Failed to load state: {e}")
                return None
        return None

    def save_state(self) -> None:
        """Save current state to disk."""
        if self.state:
            self.state.last_updated = self._timestamp()
            self.state_file.write_text(
                json.dumps(self.state.to_dict(), indent=2, ensure_ascii=False),
                encoding="utf-8",
            )

    def create_state(self, metadata: Dict[str, Any]) -> PipelineState:
        """Create new pipeline state with all phases as pending."""
        now = self._timestamp()
        phases = {}
        for phase_num, phase_name in self.phase_definitions.items():
            phases[phase_num] = PhaseState(
                phase=phase_num,
                name=phase_name,
                status=PhaseStatus.PENDING,
                executor=PHASE_AGENTS.get(phase_num, ""),
            )

        self.state = PipelineState(
            item_id=self.item_id,
            metadata=metadata,
            status=PipelineStatus.NOT_STARTED,
            current_phase=0,
            started_at=now,
            last_updated=now,
            phases=phases,
        )
        self.save_state()
        return self.state

    def start_phase(self, phase: int) -> None:
        """Mark a phase as started."""
        if self.state and phase in self.state.phases:
            self.state.phases[phase].status = PhaseStatus.IN_PROGRESS
            self.state.phases[phase].started_at = self._timestamp()
            self.state.current_phase = phase
            self.state.status = PipelineStatus.IN_PROGRESS
            self.save_state()

    def complete_phase(
        self,
        phase: int,
        output_content: str = "",
        tokens_in: int = 0,
        tokens_out: int = 0,
        cost_usd: float = 0.0,
        output_file: Optional[str] = None,
        output_dir: Optional[str] = None,
        rules_extracted: int = 0,
        contexts_covered: Optional[List[str]] = None,
        validation_passed: Optional[bool] = None,
        validation_metrics: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Mark a phase as completed and accumulate totals."""
        if self.state and phase in self.state.phases:
            ps = self.state.phases[phase]
            ps.status = PhaseStatus.COMPLETED
            ps.completed_at = self._timestamp()
            ps.tokens_in = tokens_in
            ps.tokens_out = tokens_out
            ps.cost_usd = cost_usd
            ps.output_file = output_file
            ps.output_dir = output_dir
            ps.rules_extracted = rules_extracted
            ps.validation_passed = validation_passed
            ps.validation_metrics = validation_metrics
            if contexts_covered:
                ps.contexts_covered = contexts_covered

            if ps.started_at:
                start = datetime.fromisoformat(ps.started_at.replace("Z", "+00:00"))
                ps.duration_seconds = (datetime.now(timezone.utc) - start).total_seconds()

            self.state.total_tokens_in += tokens_in
            self.state.total_tokens_out += tokens_out
            self.state.total_cost_usd += cost_usd
            self.state.total_rules_extracted += rules_extracted

            if contexts_covered:
                for ctx in contexts_covered:
                    if ctx not in self.state.bounded_contexts:
                        self.state.bounded_contexts.append(ctx)

            if output_content:
                self.state.phase_outputs[phase] = output_content

            self.save_state()

    def fail_phase(self, phase: int, error: str) -> None:
        """Mark a phase as failed."""
        if self.state and phase in self.state.phases:
            self.state.phases[phase].status = PhaseStatus.FAILED
            self.state.phases[phase].error = error
            self.state.phases[phase].completed_at = self._timestamp()
            self.state.status = PipelineStatus.FAILED
            self.state.last_error = error
            self.state.error_phase = phase
            self.save_state()

    def skip_phase(self, phase: int, reason: str) -> None:
        """Mark a phase as skipped."""
        if self.state and phase in self.state.phases:
            self.state.phases[phase].status = PhaseStatus.SKIPPED
            self.state.phases[phase].error = f"Skipped: {reason}"
            self.save_state()

    def reset_phase(self, phase: int) -> None:
        """Reset a phase to pending for reprocessing."""
        if self.state and phase in self.state.phases:
            ps = self.state.phases[phase]
            ps.status = PhaseStatus.PENDING
            ps.started_at = None
            ps.completed_at = None
            ps.duration_seconds = None
            ps.error = None
            ps.tokens_in = 0
            ps.tokens_out = 0
            ps.cost_usd = 0.0
            ps.rules_extracted = 0
            ps.contexts_covered = []
            ps.validation_passed = None
            ps.validation_metrics = None
            if phase in self.state.phase_outputs:
                del self.state.phase_outputs[phase]
            self.save_state()

    def get_next_pending_phase(self) -> Optional[int]:
        """Get the next phase that needs to be executed."""
        if not self.state:
            return None
        for phase in sorted(self.state.phases.keys()):
            if self.state.phases[phase].status == PhaseStatus.PENDING:
                return phase
        return None

    def get_resume_phase(self) -> int:
        """Return phase to resume from (last completed + 1)."""
        if not self.state:
            return 0
        max_phase = max(self.state.phases.keys())
        for i in range(max_phase, -1, -1):
            if i in self.state.phases and self.state.phases[i].status == PhaseStatus.COMPLETED:
                return min(i + 1, max_phase)
        return 0

    def can_resume(self) -> bool:
        """Check if pipeline can be resumed."""
        if not self.state:
            return False
        return self.state.status in [PipelineStatus.IN_PROGRESS, PipelineStatus.FAILED, PipelineStatus.PAUSED]

    def complete_pipeline(self) -> None:
        """Mark the pipeline as completed."""
        if self.state:
            self.state.status = PipelineStatus.COMPLETED
            self.save_state()

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the pipeline state."""
        if not self.state:
            return {"exists": False}

        completed = sum(1 for p in self.state.phases.values() if p.status == PhaseStatus.COMPLETED)
        failed = sum(1 for p in self.state.phases.values() if p.status == PhaseStatus.FAILED)

        return {
            "exists": True,
            "item_id": self.state.item_id,
            "system_name": self.state.metadata.get("system_name", "unknown"),
            "status": self.state.status.value if isinstance(self.state.status, PipelineStatus) else self.state.status,
            "current_phase": self.state.current_phase,
            "current_phase_name": PHASE_DEFINITIONS.get(self.state.current_phase, "unknown"),
            "phases_completed": completed,
            "phases_failed": failed,
            "phases_total": len(self.state.phases),
            "total_rules_extracted": self.state.total_rules_extracted,
            "bounded_contexts": self.state.bounded_contexts,
            "total_tokens": self.state.total_tokens_in + self.state.total_tokens_out,
            "total_cost_usd": self.state.total_cost_usd,
            "started_at": self.state.started_at,
            "last_updated": self.state.last_updated,
            "can_resume": self.can_resume(),
        }

    def validate_phase_gate(self, phase: int, output_base: Path) -> Dict[str, Any]:
        """
        Enforcement rule E9: Phase Gate validation with actual commands.
        Checks that output files exist and are non-trivial.
        """
        phase_dir = PHASE_OUTPUT_DIRS.get(phase, f"phase-{phase}")
        phase_path = output_base / phase_dir
        result = {
            "phase": phase,
            "phase_name": PHASE_DEFINITIONS.get(phase, "unknown"),
            "gate_passed": False,
            "checks": {},
        }

        # Check 1: Directory exists with files
        if not phase_path.exists():
            result["checks"]["dir_exists"] = False
            result["error"] = f"Output directory not found: {phase_path}"
            return result
        result["checks"]["dir_exists"] = True

        # Check 2: Files exist and are non-trivial (>500 bytes)
        files = list(phase_path.glob("*.md")) + list(phase_path.glob("*.yaml"))
        if not files:
            result["checks"]["has_files"] = False
            result["error"] = "No .md or .yaml files in output directory"
            return result
        result["checks"]["has_files"] = True

        small_files = [f for f in files if f.stat().st_size < 500]
        result["checks"]["files_substantial"] = len(small_files) == 0
        if small_files:
            result["checks"]["small_files"] = [f.name for f in small_files]

        # Check 3: No status-level VETO/BLOCKED/FAILED markers
        # Match only status markers, not descriptive text like "Veto Conditions"
        import re
        status_pattern = re.compile(
            r"^(VETO|BLOCKED|FAILED)"           # Start of line
            r"|status:\s*(VETO|BLOCKED|FAILED)"  # YAML status field
            r"|<promise>PHASE_VETO",             # Pipeline signal
            re.MULTILINE,
        )
        blocked = []
        for f in files:
            content = f.read_text(encoding="utf-8", errors="replace")
            if status_pattern.search(content):
                blocked.append(f"{f.name}: contains status marker")
        result["checks"]["no_blockers"] = len(blocked) == 0
        if blocked:
            result["checks"]["blocker_details"] = blocked

        result["gate_passed"] = (
            result["checks"]["dir_exists"]
            and result["checks"]["has_files"]
            and result["checks"].get("files_substantial", True)
            and result["checks"]["no_blockers"]
        )
        return result


# =============================================================================
# Convenience function
# =============================================================================

def load_or_create_state(
    item_id: str,
    state_dir: Path,
    metadata: Optional[Dict[str, Any]] = None,
    phase_definitions: Optional[Dict[int, str]] = None,
) -> tuple:
    """
    Load existing state or create new one.

    Returns:
        Tuple of (PipelineStateManager, is_resume: bool)
    """
    manager = PipelineStateManager(item_id, state_dir, phase_definitions)

    if manager.load_state():
        return manager, True

    if metadata is not None:
        manager.create_state(metadata)
        return manager, False

    raise ValueError("metadata required when creating new state")


# =============================================================================
# Test
# =============================================================================

if __name__ == "__main__":
    import tempfile

    print("=== Testing Domain Decoder Pipeline State ===\n")

    with tempfile.TemporaryDirectory() as tmpdir:
        manager = PipelineStateManager("forefy-prep-ahead", Path(tmpdir))

        state = manager.create_state({
            "system_name": "Forefy Prep Ahead",
            "source_location": "https://github.com/example/forefy",
            "primary_domain": "Meal Planning & Grocery",
        })
        print(f"Created state for: {state.item_id}")
        print(f"Status: {state.status}")
        print(f"Phases: {len(state.phases)}")

        # Simulate running discovery phase
        manager.start_phase(0)
        manager.complete_phase(
            0,
            output_content="Context map with 3 bounded contexts",
            tokens_in=5000,
            tokens_out=3000,
            cost_usd=0.05,
            rules_extracted=0,
            contexts_covered=["MealPlanning", "GroceryList", "UserProfile"],
        )

        print(f"\nResume phase: {manager.get_resume_phase()}")
        print(f"Next pending: {manager.get_next_pending_phase()}")
        print(f"Bounded contexts: {state.bounded_contexts}")
        print(f"\nSummary: {json.dumps(manager.get_summary(), indent=2)}")

    print("\n=== Test Complete ===")
