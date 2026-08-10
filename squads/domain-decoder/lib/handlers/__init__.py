"""
Domain Decoder — Phase Handlers

Each handler implements one phase of the 6-phase extraction pipeline.

Phase → Handler → Agent:
  0: discovery.py         → eric-evans
  1: characterization.py  → michael-feathers
  2: extraction.py        → ronald-ross
  3: modeling.py           → barbara-von-halle
  4: expression.py        → graham-witt
  5: validation.py        → decoder-chief
"""

from .discovery import handle_discovery, build_prompt as discovery_prompt
from .characterization import handle_characterization, build_prompt as characterization_prompt
from .extraction import handle_extraction, build_prompt as extraction_prompt
from .modeling import handle_modeling, build_prompt as modeling_prompt
from .expression import handle_expression, build_prompt as expression_prompt
from .validation import handle_validation, build_prompt as validation_prompt

__all__ = [
    "handle_discovery",
    "handle_characterization",
    "handle_extraction",
    "handle_modeling",
    "handle_expression",
    "handle_validation",
    "discovery_prompt",
    "characterization_prompt",
    "extraction_prompt",
    "modeling_prompt",
    "expression_prompt",
    "validation_prompt",
]
