"""Discord Reports View Tests"""
import pytest
from discord import Color
from src.formatters.discord_formatter import DiscordReportView
from src.models.coverage_report import CoverageReport, CoverageMetric, CoverageMetricType


@pytest.fixture
def sample_coverage_report():
    return CoverageReport(
        title="Test Coverage Report",
        description="This is a test description",
        author="Test Author",
        action_url="https://example.com",
        current=85.0,
        threshold=90.0,
        fields=[
            CoverageMetric(CoverageMetricType.LINE_COVERAGE, 85.0),
            CoverageMetric(CoverageMetricType.BRANCH_COVERAGE, 75.0),
        ],
    )


@pytest.fixture
def discord_report_view(sample_coverage_report):
    return DiscordReportView(sample_coverage_report)


def test_generate_message_empty_author(discord_report_view):
    discord_report_view.coverage_report.author = ""
    message = discord_report_view.generate_message()
    assert message.username == ""


def test_generate_embed_long_title(discord_report_view):
    discord_report_view.coverage_report.title = (
        "A" * 300
    )  # Discord embed title limit is 256 characters
    embed = discord_report_view.generate_embed()
    assert len(embed.title) <= 256


def test_generate_embed_no_description(discord_report_view):
    discord_report_view.coverage_report.description = None
    embed = discord_report_view.generate_embed()
    assert embed.description is None


def test_generate_embed_no_url(discord_report_view):
    discord_report_view.coverage_report.action_url = None
    embed = discord_report_view.generate_embed()
    assert embed.url is None


@pytest.mark.parametrize(
    "current,threshold,expected_color",
    [
        (100.0, 100.0, Color.dark_green()),
        (0.0, 0.0, Color.dark_green()),
        (50.0, 50.0, Color.dark_green()),
        (49.9, 50.0, Color.yellow()),
        (40.0, 50.0, Color.brand_red()),
        (None, 50.0, Color.brand_red()),
        (50.0, None, Color.dark_green()),
    ],
)
def test_threshold_color_edge_cases(
    discord_report_view, current, threshold, expected_color
):
    discord_report_view.coverage_report.current = current
    discord_report_view.coverage_report.threshold = threshold
    assert discord_report_view._threshold_color() == expected_color


def test_fields_empty(discord_report_view):
    discord_report_view.coverage_report.fields = []
    fields = discord_report_view._fields()
    assert len(fields) == 0


def test_fields_max_limit(discord_report_view):
    # Discord has a limit of 25 fields per embed
    discord_report_view.coverage_report.fields = [
        CoverageMetric(CoverageMetricType.LINE_COVERAGE, i) for i in range(30)
    ]
    fields = discord_report_view._fields()
    assert len(fields) <= 25


def test_fields_long_values(discord_report_view):
    discord_report_view.coverage_report.fields = [
        CoverageMetric(CoverageMetricType.LINE_COVERAGE, "A" * 1500)
    ]
    fields = discord_report_view._fields()
    assert len(fields[0].value) <= 1024  # Discord's field value limit


@pytest.mark.parametrize(
    "env_var,expected",
    [
        ("BOT_IMAGE", ""),
        ("BOT_IMAGE", None),
        ("ICON_URL", ""),
        ("ICON_URL", None),
    ],
)
def test_environment_variables_empty(
    discord_report_view, env_var, expected, monkeypatch
):
    monkeypatch.setenv(env_var, expected if expected is not None else "")
    embed = discord_report_view.generate_embed()
    if env_var == "BOT_IMAGE":
        assert embed.thumbnail is None or embed.thumbnail.url == ""
    elif env_var == "ICON_URL":
        assert embed.footer.icon_url is None or embed.footer.icon_url == ""


def test_generate_embed_all_fields(discord_report_view):
    embed = discord_report_view.generate_embed()
    assert embed.title is not None
    assert embed.description is not None
    assert embed.url is not None
    assert embed.color is not None
    assert embed.timestamp is not None
    assert embed.author is not None
    assert embed.footer is not None
    assert embed.thumbnail is not None
    assert len(embed.fields) > 0
