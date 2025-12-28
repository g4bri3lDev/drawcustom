"""Drawcustom - Pure image rendering from drawing instructions."""
from .core import generate_image, should_show_element
from .types import ElementType, DrawingContext, TextSegment
from .colors import ColorResolver, WHITE, BLACK, RED, YELLOW, HALF_BLACK, HALF_RED, HALF_YELLOW
from .coordinates import CoordinateParser
from .fonts import FontManager

__version__ = "0.1.1"

__all__ = [
    "generate_image",
    "should_show_element",
    "ElementType",
    "DrawingContext",
    "TextSegment",
    "ColorResolver",
    "CoordinateParser",
    "FontManager",
    "WHITE",
    "BLACK",
    "RED",
    "YELLOW",
    "HALF_BLACK",
    "HALF_RED",
    "HALF_YELLOW",
]