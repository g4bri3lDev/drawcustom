from hypothesis import given
from hypothesis import strategies as st

from drawcustom.colors import ColorResolver


class TestColorProperties:
    """Property-based tests for color resolution."""

    @given(st.integers(min_value=0, max_value=255))
    def test_hex_6digit_produces_valid_rgba(self, value):
        """Any valid 6-digit hex color produces valid RGBA."""
        resolver = ColorResolver()
        hex_color = f"#{value:02x}{value:02x}{value:02x}"
        result = resolver.resolve(hex_color)

        assert isinstance(result, tuple)
        assert len(result) == 4
        assert all(0 <= v <= 255 for v in result)
        assert result[3] == 255  # Alpha always 255

    @given(st.integers(min_value=0, max_value=15))
    def test_hex_3digit_produces_valid_rgba(self, value):
        """Any valid 3-digit hex color produces valid RGBA."""
        resolver = ColorResolver()
        hex_color = f"#{value:x}{value:x}{value:x}"
        result = resolver.resolve(hex_color)

        assert isinstance(result, tuple)
        assert len(result) == 4
        assert all(0 <= v <= 255 for v in result)

    @given(st.text(min_size=1, max_size=20))
    def test_any_string_returns_valid_rgba_or_none(self, color_string):
        """Any string input returns valid RGBA tuple or None."""
        resolver = ColorResolver()
        result = resolver.resolve(color_string)

        if result is not None:
            assert isinstance(result, tuple)
            assert len(result) == 4
            assert all(isinstance(v, int) for v in result)
            assert all(0 <= v <= 255 for v in result)

    @given(st.sampled_from(["red", "yellow"]))
    def test_accent_color_always_valid(self, accent_color):
        """Accent color parameter always produces valid results."""
        resolver = ColorResolver(accent_color=accent_color)

        # Test accent resolution
        result = resolver.resolve("accent")
        assert isinstance(result, tuple)
        assert len(result) == 4

        # Test half_accent resolution
        result_half = resolver.resolve("half_accent")
        assert isinstance(result_half, tuple)
        assert len(result_half) == 4

    @given(
        st.integers(min_value=0, max_value=255),
        st.integers(min_value=0, max_value=255),
        st.integers(min_value=0, max_value=255),
    )
    def test_hex_color_components_match(self, r, g, b):
        """Hex color components are correctly parsed."""
        resolver = ColorResolver()
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        result = resolver.resolve(hex_color)

        assert result[0] == r
        assert result[1] == g
        assert result[2] == b
        assert result[3] == 255

    def test_none_input_returns_none(self):
        """None input always returns None."""
        resolver = ColorResolver()
        assert resolver.resolve(None) is None
