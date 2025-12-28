# drawcustom

Pure image rendering from drawing instructions.

**drawcustom** is a standalone Python library for generating images from structured drawing instructions. Originally extracted from the OpenEPaperLink Home Assistant integration, it provides a clean, async API for rendering text, shapes, icons, QR codes, and more to PIL images.

## Features

- **Pure Rendering**: No dependencies on Home Assistant or other frameworks
- **17 Element Types**: Text, shapes, icons, QR codes, images, progress bars, and more
- **Async/Await**: Modern async API for efficient image generation
- **Flexible Input**: Accepts fonts as PIL objects, file paths, or built-in names
- **Full Color Output**: Returns PIL Image objects in full RGB/RGBA (caller handles dithering)
- **Percentage-Based Coordinates**: Position elements using percentages or absolute pixels
- **Template-Ready**: All values are plain data (templates expanded by caller)

## Installation

```bash
pip install drawcustom
```

## Quickstart

```python
from drawcustom import generate_image

  # Generate a simple image
  image = await generate_image(
      width=296,
      height=128,
      elements=[
          {
              "type": "text",
              "value": "Hello World",
              "x": "50%",
              "y": 50,
              "font": "ppb",
              "size": 24,
              "color": "black",
              "anchor": "mm"
          },
          {
              "type": "rectangle",
              "x_start": 10,
              "y_start": 10,
              "x_end": 100,
              "y_end": 50,
              "fill": "red",
              "outline": "black",
              "width": 2
          },
      ],
      background="white",
      accent_color="red"
  )

  # Save the image
  image.save("output.png")
```

## Element Types

### Text Elements

#### Text

Single line or multi-line text with wrapping support.

```python
{
    "type": "text",
    "value": "Hello World",
    "x": "50%",
    "y": 50,
    "font": "ppb",     # Built-in font name, path, or PIL Font object
    "size": 24,
    "color": "black",
    "anchor": "mm",    # Anchor point (e.g., mm = middle-middle)
    "max_width": 200,  # Optional text wrapping
    "truncate": False, # Truncate with ellipsis instead of wrapping
    "align": "center", # left, center, right
}
```

#### multiline

Multi-line text with delimiter-based line breaks.

```python
{
    "type": "multiline",
    "value": "Line 1|Line 2|Line 3",
    "delimiter": "|",
    "x": 10,
    "y": 10,
    "offset_y": 20, # Pixels between lines
    "font": "ppb",
    "size": 16,
}
```

etc.