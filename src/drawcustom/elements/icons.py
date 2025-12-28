from __future__ import annotations

import json
import logging
from pathlib import Path

from PIL import ImageDraw

from drawcustom.registry import element_handler
from drawcustom.types import DrawingContext, ElementType

_LOGGER = logging.getLogger(__name__)


def _load_mdi_metadata(metadata_path: str | Path) -> list[dict]:
    """Load Material Design Icons metadata JSON.

    Args:
        metadata_path: Path to materialdesignicons-webfont_meta.json

    Returns:
        List of icon metadata dictionaries

    Raises:
        ValueError: If metadata file cannot be loaded
    """
    try:
        with open(metadata_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as err:
        raise ValueError(
            f"Failed to load MDI metadata from {metadata_path}: {err}\n"
            f"Download from: https://pictogrammers.com/"
        ) from err


def _find_icon_codepoint(icon_name: str, mdi_data: list[dict]) -> str:
    """Find icon codepoint from metadata.

    Args:
        icon_name: Icon name (without mdi: prefix)
        mdi_data: MDI metadata

    Returns:
        Icon codepoint (hex string)

    Raises:
        ValueError: If icon not found
    """
    # Search direct matches
    for icon in mdi_data:
        if icon['name'] == icon_name:
            return icon['codepoint']

    # Search aliases
    for icon in mdi_data:
        if 'aliases' in icon and icon_name in icon['aliases']:
            return icon['codepoint']

    raise ValueError(
        f"Icon '{icon_name}' not found in Material Design Icons.\n"
        f"See available icons at: https://pictogrammers.com/"
    )


@element_handler(ElementType.ICON, requires=["x", "y", "value", "size", "font"])
async def draw_icon(ctx: DrawingContext, element: dict) -> None:
    """Draw Material Design Icons.

    Renders an icon from the Material Design Icons font at the specified
    position and size.

    Args:
        ctx: Drawing context
        element: Element dictionary with icon properties:
                - font: Path to materialdesignicons-webfont.ttf (REQUIRED)
                - metadata: Path to materialdesignicons-webfont_meta.json (optional, inferred from font path)
                - value: Icon name (e.g., "home" or "mdi:home")
                - x, y: Position
                - size: Icon size
                - color/fill: Icon color (default: black)
                - anchor: Text anchor (default: "la")
                - stroke_width: Stroke width (default: 0)
                - stroke_fill: Stroke color (default: white)

    Raises:
        ValueError: If font not provided, icon name invalid, or rendering fails

    Note:
        Material Design Icons font and metadata are NOT bundled.
        Download from: https://pictogrammers.com/
    """
    draw = ImageDraw.Draw(ctx.img)
    draw.fontmode = "1"

    # Coordinates
    x = ctx.coords.parse_x(element['x'])
    y = ctx.coords.parse_y(element['y'])

    # Font is required - user must provide path
    font_path = element['font']

    # Metadata path - try to infer from font path if not provided
    if 'metadata' in element:
        metadata_path = element['metadata']
    else:
        # Try to find metadata file next to font file
        font_path_obj = Path(font_path)
        metadata_path = font_path_obj.parent / "materialdesignicons-webfont_meta.json"
        if not metadata_path.exists():
            raise ValueError(
                f"MDI metadata file not found at {metadata_path}\n"
                f"Provide 'metadata' parameter or place metadata file next to font.\n"
                f"Download from: https://pictogrammers.com/"
            )

    # Load metadata
    mdi_data = _load_mdi_metadata(metadata_path)

    # Get icon name
    icon_name = element['value']
    if icon_name.startswith("mdi:"):
        icon_name = icon_name[4:]

    # Find icon codepoint
    chr_hex = _find_icon_codepoint(icon_name, mdi_data)

    # Load font using FontManager
    font = ctx.fonts.get_font(font_path, element['size'])

    # Get drawing properties
    anchor = element.get('anchor', "la")
    fill = ctx.colors.resolve(element.get('color') or element.get('fill', "black"))
    stroke_width = element.get('stroke_width', 0)
    stroke_fill = ctx.colors.resolve(element.get('stroke_fill', 'white'))

    # Draw icon
    try:
        draw.text(
            (x, y),
            chr(int(chr_hex, 16)),
            fill=fill,
            font=font,
            anchor=anchor,
            stroke_width=stroke_width,
            stroke_fill=stroke_fill
        )
    except ValueError as err:
        raise ValueError(f"Failed to draw icon '{icon_name}': {err}") from err

    # Update vertical position
    bbox = draw.textbbox((x, y), chr(int(chr_hex, 16)), font=font, anchor=anchor)
    ctx.pos_y = bbox[3]


@element_handler(ElementType.ICON_SEQUENCE, requires=["x", "y", "icons", "size", "font"])
async def draw_icon_sequence(ctx: DrawingContext, element: dict) -> None:
    """Draw a sequence of icons in a specified direction.

    Renders multiple icons in a sequence with consistent spacing,
    useful for creating icon-based status indicators or legends.

    Args:
        ctx: Drawing context
        element: Element dictionary with icon sequence properties:
                - font: Path to materialdesignicons-webfont.ttf (REQUIRED)
                - metadata: Path to materialdesignicons-webfont_meta.json (optional, inferred)
                - icons: List of icon names
                - x, y: Starting position
                - size: Icon size
                - spacing: Space between icons (default: size/4)
                - direction: "right", "left", "up", or "down" (default: "right")
                - fill: Icon color (default: black)
                - anchor: Text anchor (default: "la")
                - stroke_width: Stroke width (default: 0)
                - stroke_fill: Stroke color (default: white)

    Raises:
        ValueError: If font not provided, icon names invalid, or rendering fails
    """
    draw = ImageDraw.Draw(ctx.img)
    draw.fontmode = "1"

    # Get basic coordinates and properties
    x_start = ctx.coords.parse_x(element['x'])
    y_start = ctx.coords.parse_y(element['y'])
    size = element['size']
    spacing = element.get('spacing', size // 4)
    fill = ctx.colors.resolve(element.get('fill', "black"))
    anchor = element.get('anchor', "la")
    stroke_width = element.get('stroke_width', 0)
    stroke_fill = ctx.colors.resolve(element.get('stroke_fill', 'white'))
    direction = element.get('direction', 'right')

    # Font is required
    font_path = element['font']

    # Metadata path
    if 'metadata' in element:
        metadata_path = element['metadata']
    else:
        font_path_obj = Path(font_path)
        metadata_path = font_path_obj.parent / "materialdesignicons-webfont_meta.json"
        if not metadata_path.exists():
            raise ValueError(
                f"MDI metadata file not found at {metadata_path}\n"
                f"Provide 'metadata' parameter or place metadata file next to font."
            )

    # Load metadata and font
    mdi_data = _load_mdi_metadata(metadata_path)
    font = ctx.fonts.get_font(font_path, size)

    max_y = y_start
    max_x = x_start
    current_x = x_start
    current_y = y_start

    # Draw each icon in sequence
    for icon_name in element['icons']:
        if icon_name.startswith("mdi:"):
            icon_name = icon_name[4:]

        # Find icon codepoint
        try:
            chr_hex = _find_icon_codepoint(icon_name, mdi_data)
        except ValueError as err:
            _LOGGER.warning(f"Skipping invalid icon '{icon_name}': {err}")
            continue

        # Draw icon
        try:
            draw.text(
                (current_x, current_y),
                chr(int(chr_hex, 16)),
                fill=fill,
                font=font,
                anchor=anchor,
                stroke_width=stroke_width,
                stroke_fill=stroke_fill
            )

            # Calculate bounds
            bbox = draw.textbbox(
                (current_x, current_y),
                chr(int(chr_hex, 16)),
                font=font,
                anchor=anchor
            )
            max_y = max(max_y, bbox[3])
            max_x = max(max_x, bbox[2])

            # Move to next position
            if direction == 'right':
                current_x += size + spacing
            elif direction == 'left':
                current_x -= size + spacing
            elif direction == 'down':
                current_y += size + spacing
            elif direction == 'up':
                current_y -= size + spacing

        except ValueError as err:
            raise ValueError(f"Failed to draw icon '{icon_name}': {err}") from err

    ctx.pos_y = max(max_y, current_y)
