import pytest

from odl_renderer import generate_image


@pytest.mark.asyncio
class TestDebugGridElement:
    async def test_basic_debug_grid(self):
        image = await generate_image(width=200, height=100, elements=[{"type": "debug_grid"}])
        assert image.size == (200, 100)

    async def test_debug_grid_custom_spacing(self):
        image = await generate_image(width=200, height=100, elements=[{"type": "debug_grid", "spacing": 10}])
        assert image.size == (200, 100)

    async def test_debug_grid_solid_lines(self):
        image = await generate_image(width=200, height=100, elements=[{"type": "debug_grid", "dashed": False}])
        assert image.size == (200, 100)

    async def test_debug_grid_no_labels(self):
        image = await generate_image(width=200, height=100, elements=[{"type": "debug_grid", "show_labels": False}])
        assert image.size == (200, 100)

    async def test_debug_grid_custom_colors(self):
        image = await generate_image(
            width=200,
            height=100,
            elements=[{"type": "debug_grid", "line_color": "red", "label_color": "blue"}],
        )
        assert image.size == (200, 100)
