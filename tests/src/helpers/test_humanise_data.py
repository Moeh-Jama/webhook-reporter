from src.helpers.humanise_data import humanise_seconds


def test_humanise_seconds_basic():
    """Converts given times into human readable values"""
    assert humanise_seconds(90) == "1m 30s"
    assert humanise_seconds(60) == "1m"

def test_humanise_seconds_only_seconds():
    """Converts seconds to string ending in s for all under 60s"""
    assert humanise_seconds(45) == "45s"
    assert humanise_seconds(0) == "0s"

def test_humanise_seconds_edge_cases():
    """Humanise edge inputs"""
    # Large input
    assert humanise_seconds(3600) == "60m"  # 1 hour

    # Test with very large number
    assert humanise_seconds(123456) == "2057m 36s"

    # Test minimum valid input
    assert humanise_seconds(1) == "1s"

    assert humanise_seconds(-60) == "negative time"

    assert humanise_seconds(110.76) == "1m 51s"  # with rounding