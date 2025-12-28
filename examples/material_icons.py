"""Material Design Icons example.

  Note: This example requires downloading the Material Design Icons font separately.
  Download from: https://pictogrammers.com/

  Place the font files in a known location and update the paths below.
  """
import asyncio
from pathlib import Path
from drawcustom import generate_image


async def main():
    """Generate an image with Material Design Icons."""

    # Update these paths to your MDI font location
    # mdi_font_path = "/path/to/materialdesignicons-webfont.ttf"
    mdi_font_path = "/Users/gabriel/Developer/OEPL/drawcustom/src/drawcustom/assets/materialdesignicons-webfont.ttf"
    # mdi_metadata_path = "/path/to/materialdesignicons-webfont_meta.json"
    mdi_metadata_path = "/Users/gabriel/Developer/OEPL/drawcustom/src/drawcustom/assets/materialdesignicons-webfont_meta.json"

    # Check if font exists
    if not Path(mdi_font_path).exists():
        print(f"ERROR: Material Design Icons font not found at {mdi_font_path}")
        print("Download from: https://pictogrammers.com/")
        return

    image = await generate_image(
        width=296,
        height=128,
        elements=[
            # Home icon
            {
                "type": "icon",
                "value": "home",
                "x": 50,
                "y": 64,
                "size": 48,
                "font": mdi_font_path,
                "metadata": mdi_metadata_path,
                "color": "black",
                "anchor": "mm",
            },
            # Heart icon
            {
                "type": "icon",
                "value": "heart",
                "x": 150,
                "y": 64,
                "size": 48,
                "font": mdi_font_path,
                "metadata": mdi_metadata_path,
                "color": "red",
                "anchor": "mm",
            },
            # Star icon
            {
                "type": "icon",
                "value": "star",
                "x": 246,
                "y": 64,
                "size": 48,
                "font": mdi_font_path,
                "metadata": mdi_metadata_path,
                "color": "yellow",
                "anchor": "mm",
            },
        ],
        background="white",
    )

    image.save("icons_example.png")
    print("Icons saved to icons_example.png")


if __name__ == "__main__":
    asyncio.run(main())