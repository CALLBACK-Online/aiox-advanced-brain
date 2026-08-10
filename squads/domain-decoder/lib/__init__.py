"""
Domain Decoder Pipeline Library

Pipeline scaffolding for the 6-phase business rules extraction pipeline.
Phases: discovery, characterization, extraction, modeling, expression, validation.
"""

from .pipeline_state import (
    PHASE_DEFINITIONS,
    PhaseStatus,
    PipelineStatus,
    PhaseState,
    PipelineState,
    PipelineStateManager,
    load_or_create_state,
)
from .pipeline_logger import PipelineLogger, get_logger
from .phase_runner import (
    PhaseDefinition,
    PhaseResult,
    PhaseRunner,
    PipelineResult,
    get_phase_definitions,
)
from .progress import create_progress_tracker
from .handlers import (
    handle_discovery,
    handle_characterization,
    handle_extraction,
    handle_modeling,
    handle_expression,
    handle_validation,
)

__version__ = "1.0.0"
