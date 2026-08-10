#!/usr/bin/env python3
"""
Domain Decoder — Pipeline Logger
Version: 1.0.0

Structured JSONL logging for the 6-phase extraction pipeline.
Logs are written to outputs/decoded/{slug}/logs/ for audit trail.

Events logged:
  - pipeline_start / pipeline_complete
  - phase_start / phase_complete / phase_skip / phase_fail
  - gate_check (E9 enforcement)
  - enforcement_violation (E1-E10)
  - validation (SBVR/quality checklist results)

Example output:
  {"ts":"2026-03-31T21:00:00Z","event":"pipeline_start","item":"forefy","level":"INFO"}
  {"ts":"2026-03-31T21:01:00Z","event":"phase_start","phase":0,"name":"discovery","agent":"eric-evans","level":"INFO"}
"""

__version__ = "1.0.0"

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Union


class PipelineLogger:
    """
    Structured JSONL logger for domain decoder pipeline execution.
    Writes to both stdout and file for persistent audit trail.
    """

    def __init__(
        self,
        item_id: str,
        log_dir: Optional[Path] = None,
        log_to_stdout: bool = False,
        log_to_file: bool = True,
    ):
        self.item_id = item_id
        self.log_to_stdout = log_to_stdout
        self.log_to_file = log_to_file
        self.events: list = []
        self.start_time: Optional[datetime] = None
        self._phase_starts: Dict[int, float] = {}

        if log_to_file:
            if log_dir is None:
                log_dir = Path(f"outputs/decoded/{item_id}/logs")
            log_dir.mkdir(parents=True, exist_ok=True)
            self.log_file = log_dir / "execution-log.jsonl"
            self.error_file = log_dir / "errors.jsonl"
        else:
            self.log_file = None
            self.error_file = None

    def _timestamp(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def _log(self, event: Dict[str, Any], level: str = "INFO") -> None:
        if "ts" not in event:
            event["ts"] = self._timestamp()
        event["level"] = level
        event["item"] = self.item_id

        self.events.append(event)

        log_line = json.dumps(event, ensure_ascii=False)

        if self.log_to_stdout:
            print(log_line, flush=True)

        if self.log_to_file and self.log_file:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_line + "\n")

        if level == "ERROR" and self.error_file:
            with open(self.error_file, "a", encoding="utf-8") as f:
                f.write(log_line + "\n")

    def info(self, event_name: str, **kwargs) -> None:
        self._log({"event": event_name, **kwargs}, level="INFO")

    def error(self, event_name: str, **kwargs) -> None:
        self._log({"event": event_name, **kwargs}, level="ERROR")

    def warn(self, event_name: str, **kwargs) -> None:
        self._log({"event": event_name, **kwargs}, level="WARN")

    # ==================== Pipeline Events ====================

    def pipeline_start(self, metadata: Optional[Dict[str, Any]] = None) -> None:
        self.start_time = datetime.now(timezone.utc)
        event = {"event": "pipeline_start"}
        if metadata:
            event["system_name"] = metadata.get("system_name", "")
            event["primary_domain"] = metadata.get("primary_domain", "")
        self._log(event)

    def pipeline_complete(
        self,
        success: bool = True,
        phases_completed: int = 0,
        total_rules: int = 0,
        total_cost_usd: float = 0.0,
        error: Optional[str] = None,
    ) -> None:
        duration = None
        if self.start_time:
            duration = (datetime.now(timezone.utc) - self.start_time).total_seconds()

        event: Dict[str, Any] = {
            "event": "pipeline_complete",
            "success": success,
            "phases_completed": phases_completed,
            "total_rules": total_rules,
            "total_cost_usd": round(total_cost_usd, 6),
        }
        if duration is not None:
            event["duration_seconds"] = round(duration, 2)
        if error:
            event["error"] = error
        self._log(event)

    # ==================== Phase Events ====================

    def phase_start(self, phase: int, name: str, agent: str) -> None:
        self._phase_starts[phase] = datetime.now(timezone.utc).timestamp()
        self._log({
            "event": "phase_start",
            "phase": phase,
            "name": name,
            "agent": agent,
        })

    def phase_complete(
        self,
        phase: int,
        name: str,
        success: bool = True,
        tokens_in: int = 0,
        tokens_out: int = 0,
        cost_usd: float = 0.0,
        rules_extracted: int = 0,
        validation_passed: Optional[bool] = None,
        validation_metrics: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
    ) -> None:
        duration = None
        if phase in self._phase_starts:
            duration = datetime.now(timezone.utc).timestamp() - self._phase_starts[phase]

        event: Dict[str, Any] = {
            "event": "phase_complete",
            "phase": phase,
            "name": name,
            "success": success,
            "tokens": {"in": tokens_in, "out": tokens_out, "total": tokens_in + tokens_out},
            "cost_usd": round(cost_usd, 6),
        }
        if duration is not None:
            event["duration_seconds"] = round(duration, 2)
        if rules_extracted:
            event["rules_extracted"] = rules_extracted
        if validation_passed is not None:
            event["validation_passed"] = validation_passed
        if validation_metrics:
            event["validation_metrics"] = validation_metrics
        if error:
            event["error"] = error

        level = "INFO" if success else "ERROR"
        self._log(event, level=level)

    def phase_skip(self, phase: int, name: str, reason: str) -> None:
        self._log({
            "event": "phase_skip",
            "phase": phase,
            "name": name,
            "reason": reason,
        })

    # ==================== Enforcement Events ====================

    def gate_check(
        self,
        phase: int,
        gate_passed: bool,
        checks: Dict[str, Any],
    ) -> None:
        """Log E9 phase gate validation result."""
        level = "INFO" if gate_passed else "WARN"
        self._log({
            "event": "gate_check",
            "phase": phase,
            "gate_passed": gate_passed,
            "checks": checks,
        }, level=level)

    def enforcement_violation(
        self,
        rule: str,
        phase: int,
        detail: str,
    ) -> None:
        """Log enforcement rule violation (E1-E10)."""
        self._log({
            "event": "enforcement_violation",
            "rule": rule,
            "phase": phase,
            "detail": detail,
        }, level="ERROR")

    # ==================== Validation Events ====================

    def validation_result(
        self,
        checklist: str,
        score_pct: float,
        items_passed: int,
        items_total: int,
        criticals_passed: Optional[int] = None,
        criticals_total: Optional[int] = None,
    ) -> None:
        """Log SBVR or quality checklist result."""
        self._log({
            "event": "validation_result",
            "checklist": checklist,
            "score_pct": round(score_pct, 1),
            "items_passed": items_passed,
            "items_total": items_total,
            "criticals_passed": criticals_passed,
            "criticals_total": criticals_total,
        })

    # ==================== Summary ====================

    def get_summary(self) -> Dict[str, Any]:
        return {
            "item": self.item_id,
            "total_events": len(self.events),
            "errors": sum(1 for e in self.events if e.get("level") == "ERROR"),
            "warnings": sum(1 for e in self.events if e.get("level") == "WARN"),
            "phases_completed": sum(1 for e in self.events if e.get("event") == "phase_complete" and e.get("success")),
            "log_file": str(self.log_file) if self.log_file else None,
        }


# =============================================================================
# Global logger instance
# =============================================================================

_current_logger: Optional[PipelineLogger] = None


def get_logger(item_id: Optional[str] = None, **kwargs) -> PipelineLogger:
    """Get or create a pipeline logger."""
    global _current_logger
    if item_id:
        _current_logger = PipelineLogger(item_id, **kwargs)
    if _current_logger is None:
        raise ValueError("No logger initialized. Call get_logger(item_id) first.")
    return _current_logger


# =============================================================================
# Test
# =============================================================================

if __name__ == "__main__":
    print("=== Testing Domain Decoder Pipeline Logger ===\n")

    logger = PipelineLogger("test-system", log_to_file=False, log_to_stdout=True)

    logger.pipeline_start({"system_name": "Test System", "primary_domain": "E-Commerce"})
    logger.phase_start(0, "discovery", "eric-evans")
    logger.phase_complete(0, "discovery", rules_extracted=0,
                          validation_passed=True,
                          validation_metrics={"bounded_contexts": 3, "glossary_terms": 18})
    logger.gate_check(0, gate_passed=True, checks={"dir_exists": True, "has_files": True})
    logger.phase_start(2, "extraction", "ronald-ross")
    logger.enforcement_violation("E7", 2, "dedup-matrix.md not found")
    logger.phase_complete(2, "extraction", success=False, error="E7 violation")
    logger.validation_result("sbvr", 91.2, 41, 45, criticals_passed=5, criticals_total=5)
    logger.pipeline_complete(success=False, phases_completed=1, error="E7 violation in phase 2")

    print(f"\n=== Summary: {json.dumps(logger.get_summary(), indent=2)} ===")
